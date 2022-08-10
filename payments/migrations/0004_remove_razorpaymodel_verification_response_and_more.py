# Generated by Django 4.0.6 on 2022-08-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_razorpaymodel_amount_in_cents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='razorpaymodel',
            name='verification_response',
        ),
        migrations.AlterField(
            model_name='razorpaymodel',
            name='request_response',
            field=models.JSONField(default={}),
        ),
    ]
