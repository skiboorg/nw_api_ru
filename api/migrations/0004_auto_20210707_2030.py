# Generated by Django 3.2.4 on 2021-07-07 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210705_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='socialitem',
            options={'ordering': ('order',)},
        ),
    ]
