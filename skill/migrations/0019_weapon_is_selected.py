# Generated by Django 3.2.4 on 2021-06-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0018_alter_build_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapon',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]
