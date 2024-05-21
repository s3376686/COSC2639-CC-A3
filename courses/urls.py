
from django.urls import path

from . import views

urlpatterns = [
    path('courses', views.list_courses, name='courses'),
    path('add-course', views.add_course, name='add-course'),
    path('course/<int:course_id>/', views.course_details, name='course-details'),
    path('add-material/<int:course_id>/', views.add_study_material, name='add-material'),
]