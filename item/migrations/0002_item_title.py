# Generated by Django 3.2.4 on 2021-06-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название предмета'),
        ),
    ]
