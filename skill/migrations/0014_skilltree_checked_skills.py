# Generated by Django 3.2.4 on 2021-06-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0013_skill_is_has_left_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilltree',
            name='checked_skills',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
