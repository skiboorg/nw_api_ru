# Generated by Django 3.2.4 on 2021-06-16 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0014_skilltree_checked_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название ')),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('checked_skills', models.JSONField(blank=True, null=True)),
                ('weapon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='skill.weapon', verbose_name='Оружие')),
            ],
        ),
    ]
