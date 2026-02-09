
# Architecture Documentation

## System Overview

The AWS Customer Support Assistant is a serverless application that provides AI-powered customer support using Amazon Bedrock's Claude 3 Haiku model.

## Components

### 1. API Gateway
- **Purpose**: HTTP endpoint for client requests
- **Configuration**: REST API with CORS enabled
- **Endpoint**: `/chat` (POST method)
- **Integration**: Lambda proxy integration

### 2. Lambda Function (customer-support-processor)
- **Runtime**: Python 3.12
- **Memory**: 1024 MB
- **Timeout**: 2 minutes
- **Responsibilities**:
  - Parse incoming requests
  - Retrieve conversation history from DynamoDB
  - Build prompts with context
  - Call Bedrock with guardrails
  - Store conversation in DynamoDB
  - Return formatted responses

### 3. Amazon Bedrock
- **Model**: Claude 3 Haiku (anthropic.claude-3-haiku-20240307-v1:0)
- **Configuration**:
  - Max tokens: 2000
  - Temperature: 0.7
  - Top P: 0.9
- **Guardrails**: Custom guardrail preventing credential exposure and false commitments

### 4. DynamoDB Table
- **Table Name**: customer-support-conversations
- **Partition Key**: session_id (String)
- **Sort Key**: timestamp (Number)
- **Billing Mode**: On-demand
- **Purpose**: Store conversation history for context

### 5. IAM Roles
- **Lambda Execution Role**: Permissions for Bedrock, DynamoDB, CloudWatch, Comprehend

## Data Flow

1. User sends query via web interface
2. Request hits API Gateway `/chat` endpoint
3. API Gateway triggers Lambda function
4. Lambda retrieves conversation history from DynamoDB
5. Lambda builds prompt with system instructions and context
6. Lambda calls Bedrock with guardrails
7. Bedrock returns AI response
8. Lambda stores conversation in DynamoDB
9. Lambda returns response to API Gateway
10. API Gateway returns response to user

## Security

- **Authentication**: None (public demo)
- **Authorization**: IAM roles with least privilege
- **Data Protection**: Guardrails prevent sensitive data exposure
- **Encryption**: DynamoDB encryption at rest enabled by default

## Scalability

- **Lambda**: Auto-scales based on requests
- **DynamoDB**: On-demand capacity scales automatically
- **API Gateway**: Handles thousands of concurrent requests
- **Bedrock**: Managed service with automatic scaling

## Cost Optimization

- On-demand pricing for DynamoDB (pay per request)
- Lambda with appropriate memory allocation
- Bedrock with cost-effective Haiku model
- No idle costs (serverless architecture)

## Monitoring

- CloudWatch Logs for Lambda execution
- CloudWatch Metrics for performance tracking
- X-Ray for distributed tracing (optional)
