# Generated by Django 3.2.7 on 2021-11-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_invoice_hospital_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status_date',
            field=models.DateField(auto_now=True),
        ),
    ]
