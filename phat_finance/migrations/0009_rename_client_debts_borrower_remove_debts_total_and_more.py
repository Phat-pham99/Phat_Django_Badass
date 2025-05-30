# Generated by Django 5.2.1 on 2025-05-30 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "phat_finance",
            "0008_rename_bought_price_assets_price_assets_transac_type_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="debts",
            old_name="client",
            new_name="borrower",
        ),
        migrations.RemoveField(
            model_name="debts",
            name="total",
        ),
        migrations.AddField(
            model_name="debts",
            name="lender",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="debts",
            name="type",
            field=models.CharField(
                choices=[("debt", "debt"), ("lend", "lend"), ("pay", "pay")],
                default="lend",
            ),
        ),
    ]
