from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserSetting
from .forms import UserSettingForm

@login_required
def update_settings(request):
    user = request.user
    try:
        user_setting = UserSetting.objects.get(user=user)
    except UserSetting.DoesNotExist:
        user_setting = UserSetting(user=user)

    if request.method == 'POST':
        form = UserSettingForm(request.POST, instance=user_setting)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = UserSettingForm(instance=user_setting)

    return render(request, 'user-settings.html', {'form': form})
