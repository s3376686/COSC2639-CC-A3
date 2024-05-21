from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Course(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user

    def __str__(self):
        return self.name

class StudyMaterial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_materials')
    tags = TaggableManager()
    file_url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True, null=True)