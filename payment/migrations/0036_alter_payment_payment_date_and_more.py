# Generated by Django 5.0.2 on 2024-04-18 08:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0035_alter_payment_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 18, 13, 56, 25, 613142)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_time',
            field=models.TimeField(default=datetime.time(13, 56, 25, 613142)),
        ),
    ]
