# Generated by Django 3.2.7 on 2021-10-06 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0014_remove_hospital_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='hospital_code',
            field=models.CharField(default='Code', max_length=4),
        ),
    ]