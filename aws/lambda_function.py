import json
import joblib
import numpy as np
import pandas as pd

# Load model (will be packaged with deployment)
model = joblib.load('model.joblib')

def lambda_handler(event, context):
    try:
        # Parse input from API Gateway
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
        # Extract features
        age = body.get('age')
        sex = body.get('sex')
        bmi = body.get('bmi')
        children = body.get('children')
        smoker = body.get('smoker')
        region = body.get('region')
        
        # Prepare features for prediction
        features = pd.DataFrame({
            'age': [age],
            'sex': [sex],
            'bmi': [bmi],
            'children': [children],
            'smoker': [smoker],
            'region': [region]
        })
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'predicted_charge': round(prediction, 2)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }