# Generated by Django 5.2 on 2025-05-09 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("phat_finance", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debts",
            name="due_date",
            field=models.DateField(
                blank=True,
                default=datetime.datetime(
                    2025, 5, 9, 15, 14, 0, 383861, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="expenses",
            name="category",
            field=models.CharField(
                choices=[
                    ("food&drinks", "food&drinks"),
                    ("gas", "gas"),
                    ("dating", "dating"),
                    ("grocery", "grocery"),
                    ("medical", "medical"),
                    ("subscriptions", "subscriptions"),
                    ("utility", "utility"),
                    ("others", "others"),
                    ("pleasure", "pleasure"),
                    ("inbody", "inbody"),
                    ("bikecare", "bikecare"),
                    ("insurance", "insurance"),
                    ("gift", "gift"),
                    ("donation", "donation"),
                ],
                max_length=50,
            ),
        ),
    ]
