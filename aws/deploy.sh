#!/bin/bash

# AWS Lambda deployment script for Insurance Prediction Model

echo "🚀 Deploying Insurance Prediction Model to AWS Lambda..."

# Create deployment package
mkdir -p deployment
cd deployment

# Copy Lambda function
cp ../lambda_function.py .

# Copy trained model
cp ../../app/app/model.joblib .

# Install dependencies
pip install -r ../requirements.txt -t .

# Create deployment zip
zip -r insurance-prediction-lambda.zip .

# Deploy to AWS Lambda (requires AWS CLI configured)
aws lambda create-function \
  --function-name insurance-prediction \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://insurance-prediction-lambda.zip \
  --timeout 30 \
  --memory-size 512

echo "✅ Deployment complete!"
echo "📝 Next steps:"
echo "1. Create API Gateway endpoint"
echo "2. Update frontend to use AWS endpoint"