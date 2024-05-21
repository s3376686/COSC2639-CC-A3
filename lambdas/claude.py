import json
import boto3
import requests
import os

def lambda_handler(event, context):
    # API Gateway passes data as a JSON string in the 'body' for POST requests
    body = json.loads(event.get('body', '{}'))

    # Extract the Claude API key and document URL from the incoming request
    claude_api_key = body.get('claude_api_key')
    document_url = body.get('document_url')

    # Fetch the document content using the URL
    s3_client = boto3.client('s3')
    bucket_name, object_key = parse_s3_url(document_url)

    # Get the object from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    document_content = response['Body'].read().decode('utf-8')

    # Use Claude API to generate quiz questions based on the document
    claude_url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": claude_api_key
    }
    data = {
        "prompt": f"Generate quiz questions based on the following document:\n\n{document_content}",
        "model": "claude-v1",
        "max_tokens_to_sample": 500
    }

    claude_response = requests.post(claude_url, headers=headers, json=data)
    claude_response_json = claude_response.json()

    # Extract the generated questions
    questions = claude_response_json.get('completion', '')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'questions': questions
        })
    }

def parse_s3_url(url):
    """
    Helper function to extract bucket and object key from S3 URL
    """
    if url.startswith("s3://"):
        url = url[5:]
        parts = url.split("/", 1)
        return parts[0], parts[1]
    elif url.startswith("https://"):
        url = url.split("amazonaws.com/")[1]
        parts = url.split("/", 1)
        return parts[0], parts[1]
    else:
        raise ValueError("Invalid S3 URL format")