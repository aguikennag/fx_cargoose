# Generated by Django 3.0.5 on 2022-07-10 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0008_auto_20220709_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='receiver_address',
            field=models.CharField(default='23 ubong street', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment',
            name='receiver_email',
            field=models.EmailField(default='hopper', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment',
            name='receiver_name',
            field=models.CharField(default='santa', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment',
            name='receiver_phone_number',
            field=models.CharField(default='08146843994', max_length=20),
            preserve_default=False,
        ),
    ]