# Generated by Django 4.0.6 on 2022-08-06 10:57

import backend_api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessmodel',
            name='available_credits',
            field=models.IntegerField(default=0, validators=[backend_api.validators.Validators.min_0_validator]),
        ),
    ]