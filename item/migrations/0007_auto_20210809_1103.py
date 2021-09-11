# Generated by Django 3.2.4 on 2021-08-09 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_auto_20210809_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='staggerDamage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='critChance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='critDamageMultiplier',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.itemsubcategory', verbose_name='Подкатегория '),
        ),
    ]
