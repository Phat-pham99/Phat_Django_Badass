# Generated by Django 5.2.1 on 2025-05-16 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("phat_fitness", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gymtrack",
            name="duration",
            field=models.DurationField(
                default=datetime.timedelta(seconds=3600), editable=False
            ),
        ),
    ]
