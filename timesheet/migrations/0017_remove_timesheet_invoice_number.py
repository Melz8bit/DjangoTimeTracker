# Generated by Django 3.2.7 on 2021-10-06 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0016_timesheet_invoice_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='invoice_number',
        ),
    ]
