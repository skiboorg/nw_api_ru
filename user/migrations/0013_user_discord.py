# Generated by Django 3.2.4 on 2021-06-24 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_is_guild_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='discord',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Дискорд'),
        ),
    ]
