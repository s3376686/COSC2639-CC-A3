# Generated by Django 5.0.6 on 2024-05-20 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0006_alter_studymaterial_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="studymaterial",
            name="upload_date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
