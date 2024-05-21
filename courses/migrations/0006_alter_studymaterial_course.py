# Generated by Django 5.0.6 on 2024-05-20 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_remove_studymaterial_file_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studymaterial",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="study_materials",
                to="courses.course",
            ),
        ),
    ]