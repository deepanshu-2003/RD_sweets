# Generated by Django 5.0.2 on 2024-03-20 09:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_time',
            field=models.TimeField(default=datetime.time(9, 44, 54, 284246)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 20, 15, 14, 54, 284246)),
        ),
    ]
