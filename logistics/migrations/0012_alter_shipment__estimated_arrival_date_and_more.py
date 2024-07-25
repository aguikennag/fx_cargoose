# Generated by Django 4.2.14 on 2024-07-25 12:45

from django.db import migrations, models
import logistics.models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0011_shipment__estimated_departure_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='_estimated_arrival_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='_estimated_departure_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='package_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='receiver_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipment_fee',
            field=models.DecimalField(decimal_places=2, help_text='in dollars($)', max_digits=100),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='tracking_number',
            field=models.CharField(blank=True, default=logistics.models.Shipment.get_tracking_number, max_length=20),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='status',
            field=models.CharField(choices=[('registered', 'registered'), ('received', 'received'), ('processing', 'processing'), ('in transit', 'in transit')], max_length=20),
        ),
        migrations.AlterField(
            model_name='transitlog',
            name='station',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='transitlog',
            name='status',
            field=models.CharField(choices=[('arrived', 'arrived'), ('processing', 'processing'), ('dispatched', 'dispatched')], max_length=20),
        ),
    ]