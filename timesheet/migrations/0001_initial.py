# Generated by Django 3.2.7 on 2021-09-21 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_worked', models.DateField()),
                ('clock_in', models.TimeField()),
                ('clock_out_lunch', models.TimeField()),
                ('clock_in_lunch', models.TimeField()),
                ('clock_out', models.TimeField()),
                ('total_hours_worked', models.IntegerField()),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=6)),
                ('bonus_amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('gross_total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('net_total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('tax_estimate', models.DecimalField(decimal_places=2, max_digits=7)),
                ('hospital_name', models.CharField(max_length=70)),
                ('invoice_number', models.CharField(max_length=20)),
            ],
        ),
    ]