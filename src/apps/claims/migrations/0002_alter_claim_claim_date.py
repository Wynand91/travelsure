# Generated by Django 4.2 on 2025-05-28 15:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='claim_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
