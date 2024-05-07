import boto3
import json
import secrets

# Dummy user data (replace with database integration)
users = {
    'Abhishek': 'Admin@123',
    'Yash': 'Admin@123'
}

def lambda_handler(event, context):
    # Assuming the event comes from API Gateway, and the body is a JSON string
    data = json.loads(event['body']) if 'body' in event else None

    # Check if the JSON data contains 'username' and 'password'
    if not data or 'username' not in data or 'password' not in data:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Username or password missing'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    username = data['username']
    password = data['password']

    # Verify username and password
    if username in users and users[username] == password:
        # In an AWS Lambda function, you can't directly manage session as in web frameworks.
        # You would typically use JWT or similar for API authentication.
        return {
            'statusCode': 200,
            'body': json.dumps({'success': 'Logged in successfully'}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST",
            },
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid username or password'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
