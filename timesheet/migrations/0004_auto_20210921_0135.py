# Generated by Django 3.2.7 on 2021-09-21 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0003_auto_20210921_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='clock_in_lunch',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='clock_out_lunch',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
