# Generated by Django 3.2.4 on 2021-06-14 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20210606_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='fio',
            new_name='nickname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bonuses',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_ok',
        ),
        migrations.RemoveField(
            model_name='user',
            name='promo',
        ),
        migrations.RemoveField(
            model_name='user',
            name='session',
        ),
    ]