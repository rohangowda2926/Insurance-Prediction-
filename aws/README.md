# AWS Deployment Guide 🚀

Deploy your Insurance Prediction Model to AWS Lambda for **FREE** using AWS Free Tier.

## Quick Deploy (5 minutes)

### Option 1: CloudFormation (Recommended)
```bash
# Deploy infrastructure
aws cloudformation create-stack \
  --stack-name insurance-prediction \
  --template-body file://cloudformation.yaml \
  --capabilities CAPABILITY_IAM

# Package and deploy code
./deploy.sh
```

### Option 2: Manual Setup
```bash
# 1. Create Lambda function
aws lambda create-function \
  --function-name insurance-prediction \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://deployment/insurance-prediction-lambda.zip

# 2. Create API Gateway (via AWS Console)
```

## Free Tier Limits
- **Lambda**: 1M requests/month + 400,000 GB-seconds compute
- **API Gateway**: 1M API calls/month
- **CloudFormation**: Free

## Cost Estimate
- **Monthly**: $0 (within free tier)
- **Per prediction**: ~$0.0000002

## Update Frontend
Replace Render URL with AWS endpoint:
```javascript
const API_URL = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/predict';
```