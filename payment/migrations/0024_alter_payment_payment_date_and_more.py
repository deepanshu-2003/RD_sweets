# Generated by Django 5.0.2 on 2024-03-20 10:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0023_alter_payment_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 20, 16, 29, 10, 599656)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_time',
            field=models.TimeField(default=datetime.time(16, 29, 10, 599655)),
        ),
    ]
