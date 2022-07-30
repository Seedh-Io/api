# Generated by Django 4.0.6 on 2022-07-30 22:44

import backend_api.fields.base_fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            bases=(models.Model, backend_api.fields.base_fields.BaseFields),
        ),
        migrations.CreateModel(
            name='BusinessUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.UUIDField()),
                ('role', models.IntegerField(choices=[('Owner', 1), ('Admin', 10), ('Reporter', 20)])),
                ('status', models.IntegerField(choices=[('Active', 1), ('Disabled', 2), ('Blocked', 3), ('Deleted', 4)], default=1)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='business.businessmodel')),
            ],
            options={
                'db_table': 'business_user',
                'managed': True,
            },
            bases=(models.Model, backend_api.fields.base_fields.BaseFields),
        ),
        migrations.CreateModel(
            name='BusinessConfigurationsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_ads_config', models.JSONField(default=dict)),
                ('google_ads_config', models.JSONField(default=dict)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.businessmodel')),
            ],
            options={
                'db_table': 'business_configurations',
                'managed': True,
            },
            bases=(models.Model, backend_api.fields.base_fields.BaseFields),
        ),
    ]
