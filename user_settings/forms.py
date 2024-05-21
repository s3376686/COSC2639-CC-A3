from django import forms
from .models import UserSetting

class UserSettingForm(forms.ModelForm):
    class Meta:
        model = UserSetting
        fields = ['openai_api_key', 'claude_api_key']
