# Generated by Django 5.1.7 on 2025-03-23 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_carbooking_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='carbooking',
            name='destination',
            field=models.CharField(default='Default Destination', max_length=100),
        ),
    ]
