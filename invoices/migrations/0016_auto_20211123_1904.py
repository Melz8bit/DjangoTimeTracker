# Generated by Django 3.2.7 on 2021-11-24 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0015_alter_invoice_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='created_date',
            field=models.DateField(default=0.00023664565540089925),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status_date',
            field=models.DateField(),
        ),
    ]