import requests
import json
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from courses.models import StudyMaterial 
from user_settings.models import UserSetting
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def material_detail(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    
    cloudfront_base_url = settings.CLOUDFRONT_BASE_URL
    s3_base_url = "https://mentat-bucket.s3.amazonaws.com/"
    file_url = material.file_url.replace(s3_base_url, cloudfront_base_url + "/")

    # Initialize variables for both API keys
    open_api_key, claude_api_key = None, None

    # Try to fetch the OpenAI and Claude API keys from user settings
    try:
        user_settings = UserSetting.objects.get(user=request.user)
        open_api_key = user_settings.openai_api_key
        claude_api_key = user_settings.claude_api_key
    except UserSetting.DoesNotExist:
        pass  # If settings don't exist, keys remain None

    # If POST request, determine which key to use based on the button pressed
    if request.method == 'POST':
        # Determine which API to call based on the user's choice in the form
        if 'generate_openai' in request.POST and open_api_key:
            api_key = open_api_key
            api_gateway_url = 'https://qch7wed2s0.execute-api.ap-southeast-2.amazonaws.com/default/openai_quiz'
        elif 'generate_claude' in request.POST and claude_api_key:
            api_key = claude_api_key
            api_gateway_url = 'https://qch7wed2s0.execute-api.ap-southeast-2.amazonaws.com/default/claude_quiz'
        else:
            return render(request, 'material-detail.html', {
                'material': material,
                'file_url': file_url,
                'open_api_key': open_api_key,
                'claude_api_key': claude_api_key,
                'error_message': "API key not available or incorrect button pressed."
            })

        # Prepare the payload with the user's API key and the URL of the document
        payload = {
            'api_key': api_key,
            'document_url': file_url
        }

        # Send a POST request to the API Gateway endpoint
        response = requests.post(api_gateway_url, json=payload)
        # Process the Lambda response if the status code is 200
        if response.status_code == 200:
            result = response.json()
            quiz_questions = result.get('questions', "No quiz questions available.")
        else:
            quiz_questions = "Failed to generate questions. Please try again later."

        return render(request, 'material-detail.html', {
            'material': material,
            'file_url': file_url,
            'open_api_key': open_api_key,
            'claude_api_key': claude_api_key,
            'quiz_questions': quiz_questions
        })

    # Render the template with material, file URL, and keys without quiz questions
    return render(request, 'material-detail.html', {
        'material': material,
        'file_url': file_url,
        'open_api_key': open_api_key,
        'claude_api_key': claude_api_key
    })