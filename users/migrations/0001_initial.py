# Generated by Django 4.0.6 on 2022-08-07 20:26

import backend_api.validators
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100, null=True)),
                ('email_id', models.EmailField(max_length=100, unique=True, validators=[backend_api.validators.Validators.email_validator])),
                ('mobile', models.CharField(max_length=10, unique=True, validators=[backend_api.validators.Validators.mobile_validator])),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('password', models.CharField(max_length=128, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('verified_on', models.DateTimeField(default=None, null=True)),
                ('last_verification_request', models.DateTimeField(null=True)),
                ('verification_count', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
