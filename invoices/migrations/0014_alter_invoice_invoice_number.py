# Generated by Django 3.2.7 on 2021-11-23 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0013_remove_invoice_invoice_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
    ]
