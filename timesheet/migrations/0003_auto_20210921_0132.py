# Generated by Django 3.2.7 on 2021-09-21 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0002_auto_20210921_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='gross_total',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='invoice_number',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='net_total',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='tax_estimate',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='total_hours_worked',
        ),
    ]