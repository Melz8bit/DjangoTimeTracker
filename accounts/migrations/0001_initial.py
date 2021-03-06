# Generated by Django 3.2.7 on 2021-11-28 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=70)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(choices=[('FL', 'Florida'), ('GA', 'Georgia')], max_length=2)),
                ('zip_code', models.CharField(max_length=5)),
                ('email', models.EmailField(default='N/A', max_length=254)),
                ('telephone', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
