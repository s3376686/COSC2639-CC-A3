# Generated by Django 5.0.6 on 2024-05-17 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_studymaterial_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="studymaterial",
            name="file_url",
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
