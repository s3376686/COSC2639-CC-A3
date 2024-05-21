import json
import boto3
import openai
import os

def lambda_handler(event, context):
    # API Gateway passes data as a JSON string in the 'body' for POST requests
    body = json.loads(event.get('body', '{}'))
    
    # Extract the OpenAI API key and document URL from the incoming request
    openai_api_key = body.get('openai_api_key')
    document_url = body.get('document_url')
    
    # Initialize OpenAI with the provided API key
    openai.api_key = openai_api_key

    # Fetch the document content using the URL
    s3_client = boto3.client('s3')
    bucket_name, object_key = parse_s3_url(document_url)

    # Get the object from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    document_content = response['Body'].read().decode('utf-8')

    # Use OpenAI to generate quiz questions based on the document
    openai_response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Generate quiz questions based on the following document: {document_content}",
        max_tokens=500
    )

    # Extract the generated questions
    questions = openai_response.get('choices')[0].get('text', '')

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
