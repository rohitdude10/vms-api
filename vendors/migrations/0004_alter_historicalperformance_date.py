# Generated by Django 5.0.4 on 2024-04-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "vendors",
            "0003_rename_delivery_date_purchaseorder_actual_delivery_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalperformance",
            name="date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]