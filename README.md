
# AWS Customer Support AI Assistant

A serverless AI-powered customer support assistant built with AWS Bedrock, Lambda, DynamoDB, and API Gateway. This project demonstrates prompt engineering, AI governance, and serverless architecture best practices.

## 🎯 Project Overview

This assistant provides intelligent AWS customer support using Claude 3 Haiku through Amazon Bedrock, with built-in safety guardrails and conversation memory.

## 🏗️ Architecture

- **Amazon Bedrock**: Claude 3 Haiku for AI responses
- **AWS Lambda**: Request processing (Python 3.12)
- **Amazon DynamoDB**: Conversation history storage
- **API Gateway**: REST API endpoint
- **Bedrock Guardrails**: Content safety and governance
- **Amazon Comprehend**: Intent detection

## ✨ Features

- Natural language customer support for AWS services
- Conversation history and context awareness
- Content safety with Bedrock Guardrails (prevents credential exposure, false commitments)
- Intent detection for better understanding
- Automatic escalation for complex issues
- Web-based chat interface

## 💰 Cost Estimate

Monthly cost for moderate usage (~1000 queries):
- Bedrock (Claude 3 Haiku): ~$2
- Lambda: ~$0.50
- DynamoDB: ~$0.25
- API Gateway: ~$0.35
- **Total: ~$3.50/month**

Stays well within AWS Free Tier for learning projects.

## 🚀 Deployment Guide

### Prerequisites
- AWS Account
- AWS CLI configured
- Python 3.12+

### Step 1: Enable Bedrock Model Access
1. Go to Amazon Bedrock console
2. Navigate to Model access
3. Enable Claude 3 Haiku model

### Step 2: Create DynamoDB Table
```bash
aws dynamodb create-table \
  --table-name customer-support-conversations \
  --attribute-definitions \
    AttributeName=session_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=session_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### Step 3: Create Bedrock Guardrails
1. Go to Bedrock console → Guardrails
2. Create guardrail with denied topics:
   - Security Credentials
   - Future AWS Features
   - Competitor Comparisons
3. Note the Guardrail ID

### Step 4: Deploy Lambda Function
1. Create IAM role with policies:
   - AmazonBedrockFullAccess
   - AmazonDynamoDBFullAccess
   - CloudWatchLogsFullAccess
   - ComprehendReadOnly

2. Create Lambda function:
   - Runtime: Python 3.12
   - Handler: lambda_function.lambda_handler
   - Upload code from `lambda/customer-support-processor.py`

3. Set environment variables:
   - `GUARDRAIL_ID`: Your Bedrock Guardrail ID
   - `GUARDRAIL_VERSION`: DRAFT
   - `TABLE_NAME`: customer-support-conversations

### Step 5: Create API Gateway
1. Create REST API
2. Create `/chat` resource
3. Create POST method linked to Lambda
4. Enable CORS
5. Deploy to `prod` stage

### Step 6: Update Web Interface
1. Open `web/index.html`
2. Replace `API_URL` with your API Gateway endpoint
3. Open in browser to test

## 🧪 Testing

Test with curl:
```bash
curl -X POST YOUR_API_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "My EC2 instance is not responding. How do I troubleshoot?", "session_id": "test-001"}'
```

Or use the web interface at `web/index.html`

## 📊 Monitoring

View metrics in CloudWatch:
- Lambda invocations and errors
- DynamoDB read/write capacity
- API Gateway requests

## 🔒 Security

- All credentials stored in AWS Secrets Manager
- Guardrails prevent credential exposure
- IAM roles follow least privilege principle
- API Gateway with throttling enabled

## 🎓 Learning Outcomes

This project demonstrates:
- Prompt engineering with Amazon Bedrock
- Serverless architecture design
- AI governance and safety controls
- RESTful API development
- Conversation state management

## 📝 Future Enhancements

- [ ] Add Amazon Kendra for knowledge base integration
- [ ] Implement user feedback collection
- [ ] Add multi-language support
- [ ] Create Slack/Teams integration
- [ ] Add response caching with ElastiCache

## 📄 License

MIT License

## 👤 Author

Built as part of AWS Bedrock learning project.

**Connect with me:**
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]

---

**Tags:** #AWS #Bedrock #Serverless #AI #MachineLearning #CloudComputing
