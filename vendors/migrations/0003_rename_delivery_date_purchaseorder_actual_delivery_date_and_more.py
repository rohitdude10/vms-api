# Generated by Django 5.0.4 on 2024-04-27 18:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vendors", "0002_alter_historicalperformance_average_response_time_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="purchaseorder",
            old_name="delivery_date",
            new_name="actual_delivery_date",
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="expected_delivery_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
