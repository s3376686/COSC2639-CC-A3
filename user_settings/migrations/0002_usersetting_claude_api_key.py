# Generated by Django 5.0.6 on 2024-05-21 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_settings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersetting",
            name="claude_api_key",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
