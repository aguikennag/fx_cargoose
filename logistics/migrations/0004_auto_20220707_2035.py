# Generated by Django 3.0.5 on 2022-07-07 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0003_auto_20220707_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='weight',
            field=models.FloatField(help_text='in kg'),
        ),
    ]