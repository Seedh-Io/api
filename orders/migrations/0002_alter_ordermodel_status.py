# Generated by Django 4.0.6 on 2022-08-10 20:45

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(10, 'Created'), (20, 'Payment Processing'), (30, 'Payment Completed'), (40, 'Refunded'), (50, 'Payment Processed'), (60, 'Issue')], default=10),
        ),
    ]