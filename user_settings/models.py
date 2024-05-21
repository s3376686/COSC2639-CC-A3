from django.db import models
from django.contrib.auth.models import User

class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    openai_api_key = models.CharField(max_length=255, blank=True)
    claude_api_key = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Settings for {self.user.username}"
