# Generated by Django 4.2.11 on 2024-07-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0011_alter_country_name_alter_country_short_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='short_name',
            field=models.CharField(max_length=50),
        ),
    ]