# Generated by Django 5.0.3 on 2024-05-29 16:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bus_ticketing_app", "0004_schedule_seat_number"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ticket",
            old_name="passenger_id",
            new_name="passenger",
        ),
    ]