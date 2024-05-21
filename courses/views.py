import requests
from django.shortcuts import render, get_object_or_404
from .models import Course
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CourseForm, StudyMaterialForm
import urllib.parse
import boto3
import environ

env = environ.Env()
environ.Env.read_env()

@login_required  # Ensure the user is logged in
def list_courses(request):
    # Retrieve only Course objects belonging to the logged-in user
    courses = Course.objects.filter(user=request.user)

    # Pass the courses to the template
    context = {'courses': courses}
    return render(request, 'courses.html', context=context)



@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # Create a new course but don't save it yet
            new_course = form.save(commit=False)
            # Set the user of the course to the current user
            new_course.user = request.user
            # Now save the course with the user set
            new_course.save()
            return redirect('courses')  # Adjust as needed
    else:
        form = CourseForm()
    return render(request, 'add-course.html', {'form': form})


@login_required
def add_study_material(request, course_id):
    course = get_object_or_404(Course, id=course_id, user=request.user)

    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            study_material = form.save(commit=False)
            study_material.user = request.user  # Associate the material with the user
            study_material.course = course

            # Handle the file upload to S3
            file = request.FILES.get('file')
            if file:
                s3 = boto3.client('s3', region_name=settings.AWS_REGION) 
                bucket_name = env('AWS_STORAGE_BUCKET_NAME')
                sanitized_file_name = urllib.parse.quote_plus(file.name.replace(" ", "_"))
                user_name = urllib.parse.quote_plus(request.user.username.replace(" ", "_"))
                course_name = urllib.parse.quote_plus(course.name.replace(" ", "_"))
                object_key = f'study_materials/{user_name}/{course_name}/{sanitized_file_name}'

                # Upload the file to S3
                s3.upload_fileobj(
                    file.file,
                    bucket_name,
                    object_key,
                    ExtraArgs={'ContentType': file.content_type}
                )

                s3_url = f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
                # print(s3_url)
                study_material.file_url = s3_url
                study_material.save()
                api_url = f"https://usk0jqxm3l.execute-api.ap-southeast-2.amazonaws.com/default/extract_keywords?bucket={bucket_name}&key={object_key}"
                print(api_url)
                try:
                    response = requests.get(api_url)
                    if response.status_code == 200:
                        tags_data = response.json()
                        tags = tags_data.get('keywords', [])
                    else:
                        tags = []
                except Exception as e:
                    print(f"Failed to get tags from API: {str(e)}")
                    tags = []

                # Set the tags to the study material
                study_material.tags.set(tags)
            study_material.save()
            if 'tags' in form.cleaned_data:
                study_material.tags.set(*form.cleaned_data['tags'])
            study_materials = course.study_materials.all()
            return redirect('course-details', course_id=course.id)
    else:
        form = StudyMaterialForm(initial={'course_name': course.name})

    return render(request, 'add-material.html', {'form': form,'course': course})


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    study_materials = course.study_materials.all()
    return render(request, 'course-details.html', {'course': course, 'study_materials': study_materials})