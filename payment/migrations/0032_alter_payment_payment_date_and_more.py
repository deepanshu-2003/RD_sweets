# Generated by Django 5.0.2 on 2024-04-10 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0031_alter_payment_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 10, 11, 52, 12, 107799)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_time',
            field=models.TimeField(default=datetime.time(11, 52, 12, 107799)),
        ),
    ]
