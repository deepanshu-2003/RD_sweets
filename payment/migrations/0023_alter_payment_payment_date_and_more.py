# Generated by Django 5.0.2 on 2024-03-20 10:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0022_alter_payment_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 20, 16, 26, 33, 697487)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_time',
            field=models.TimeField(default=datetime.time(16, 26, 33, 697487)),
        ),
    ]