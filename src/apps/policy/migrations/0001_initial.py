# Generated by Django 4.2 on 2025-05-27 12:46

import apps.fields
import apps.policy.enums
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('destination', apps.fields.EnumSmallIntegerField(enum_class=apps.policy.enums.Destination)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('policy_type', apps.fields.EnumSmallIntegerField(enum_class=apps.policy.enums.PolicyType)),
                ('paid', models.BooleanField(default=False)),
                ('status', apps.fields.EnumSmallIntegerField(enum_class=apps.policy.enums.PolicyStatus)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Policies',
            },
        ),
    ]
