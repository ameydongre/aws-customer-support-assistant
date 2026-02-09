import json
import boto3
import os
from datetime import datetime

# Initialize AWS clients
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Get environment variables
GUARDRAIL_ID = os.environ.get('GUARDRAIL_ID', '')
GUARDRAIL_VERSION = os.environ.get('GUARDRAIL_VERSION', 'DRAFT')
TABLE_NAME = os.environ.get('TABLE_NAME', 'customer-support-conversations')

# Initialize DynamoDB table
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """Main handler for customer support AI assistant"""
    try:
        body = json.loads(event.get('body', '{}'))
        user_query = body.get('query', '')
        session_id = body.get('session_id', 'default-session')

        if not user_query:
            return create_response(400, {'error': 'Query is required'})

        conversation_history = get_conversation_history(session_id)
        prompt = build_prompt(user_query, conversation_history)
        ai_response = invoke_bedrock_with_guardrails(prompt)
        store_conversation(session_id, user_query, ai_response)

        return create_response(200, {
            'response': ai_response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        return create_response(500, {
            'error': 'Internal server error',
            'details': str(e)
        })


def get_conversation_history(session_id, limit=5):
    """Retrieve recent conversation history"""
    try:
        response = table.query(
            KeyConditionExpression='session_id = :sid',
            ExpressionAttributeValues={':sid': session_id},
            ScanIndexForward=False,
            Limit=limit * 2
        )

        items = response.get('Items', [])
        history = []
        for item in reversed(items):
            history.append({
                'role': item.get('role'),
                'content': item.get('content')
            })

        return history

    except Exception as e:
        print(f"Error retrieving history: {str(e)}")
        return []


def build_prompt(user_query, conversation_history):
    """Construct prompt with context"""
    system_lines = [
        "You are a helpful AWS customer support assistant. Your role is to:",
        "- Help users troubleshoot AWS service issues",
        "- Provide clear, step-by-step guidance",
        "- Be professional, patient, and empathetic",
        "- Never share security credentials or access keys",
        "- Never make commitments about future AWS features",
        "- Focus on documented AWS best practices",
        "",
        "Important guidelines:",
        "- If you don't know something, admit it and suggest contacting AWS Support",
        "- Always prioritize security and best practices",
        "- Keep responses concise but thorough",
        "- Ask clarifying questions when the issue is unclear"
    ]
    system_prompt = "\n".join(system_lines)

    context_parts = []
    if conversation_history:
        context_parts.append("Previous conversation:")
        for msg in conversation_history[-10:]:
            role = "User" if msg['role'] == 'user' else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")
    
    context = "\n".join(context_parts)
    full_prompt = f"{system_prompt}\n\n{context}\n\nUser: {user_query}\n\nA:"
    return full_prompt


def invoke_bedrock_with_guardrails(prompt):
    """Call Bedrock with Claude model"""
    try:
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9
        }

        if GUARDRAIL_ID:
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307-v1:0',
                body=json.dumps(request_body),
                guardrailIdentifier=GUARDRAIL_ID,
                guardrailVersion=GUARDRAIL_VERSION
            )
        else:
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307-v1:0',
                body=json.dumps(request_body)
            )

        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text']

        return ai_response

    except Exception as e:
        print(f"Bedrock error: {str(e)}")
        raise


def store_conversation(session_id, user_query, ai_response):
    """Store conversation in DynamoDB"""
    try:
        timestamp = int(datetime.now().timestamp() * 1000)

        table.put_item(Item={
            'session_id': session_id,
            'timestamp': timestamp,
            'role': 'user',
            'content': user_query
        })

        table.put_item(Item={
            'session_id': session_id,
            'timestamp': timestamp + 1,
            'role': 'assistant',
            'content': ai_response
        })

    except Exception as e:
        print(f"DynamoDB error: {str(e)}")


def create_response(status_code, body):
    """Create API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps(body)
    }
