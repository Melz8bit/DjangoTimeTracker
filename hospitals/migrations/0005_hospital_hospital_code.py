# Generated by Django 3.2.7 on 2021-10-06 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0004_hospital_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='hospital_code',
            field=models.CharField(default=None, max_length=4),
        ),
    ]