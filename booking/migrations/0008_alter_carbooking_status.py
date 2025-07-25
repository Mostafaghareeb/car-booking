# Generated by Django 5.1.7 on 2025-06-11 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_alter_carbooking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carbooking',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('pending', 'Pending'), ('canceled', 'Canceled'), ('completed', 'Completed')], default='pending', max_length=10),
        ),
    ]
