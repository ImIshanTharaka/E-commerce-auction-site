# Generated by Django 4.1 on 2022-08-25 18:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_active_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
