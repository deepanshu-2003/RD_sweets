# Generated by Django 5.0.2 on 2024-04-11 06:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0033_alter_payment_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 11, 11, 35, 5, 621561)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_time',
            field=models.TimeField(default=datetime.time(11, 35, 5, 621561)),
        ),
    ]
