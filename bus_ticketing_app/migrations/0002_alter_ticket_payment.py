# Generated by Django 5.0.3 on 2024-04-22 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bus_ticketing_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="payment",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="bus_ticketing_app.payment",
            ),
        ),
    ]