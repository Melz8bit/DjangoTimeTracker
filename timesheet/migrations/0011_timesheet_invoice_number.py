# Generated by Django 3.2.7 on 2021-10-06 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0010_timesheet_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='invoice_number',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
