# Generated by Django 5.0.2 on 2025-06-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_driver_carbooking_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carbooking',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='carbooking',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
