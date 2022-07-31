# Generated by Django 4.0.6 on 2022-07-31 14:16

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('gst_details', models.JSONField(default=dict)),
                ('business_owner', models.UUIDField()),
                ('image_id', models.UUIDField(null=True)),
                ('status', models.IntegerField(choices=[('Active', 1), ('Disabled', 2), ('Blocked', 3), ('Deleted', 4)], default=1)),
                ('business_verified', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'business',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BusinessUserModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user_id', models.UUIDField()),
                ('role', models.IntegerField(choices=[('Owner', 1), ('Admin', 10), ('Reporter', 20)])),
                ('status', models.IntegerField(choices=[('Active', 1), ('Disabled', 2), ('Blocked', 3), ('Deleted', 4)], default=1)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='business.businessmodel')),
            ],
            options={
                'db_table': 'business_user',
                'managed': True,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='BusinessConfigurationsModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('facebook_ads_config', models.JSONField(default=dict)),
                ('google_ads_config', models.JSONField(default=dict)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.businessmodel')),
            ],
            options={
                'db_table': 'business_configurations',
                'managed': True,
            },
        ),
    ]
