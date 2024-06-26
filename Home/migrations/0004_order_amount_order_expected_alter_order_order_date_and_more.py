# Generated by Django 5.0.2 on 2024-03-21 10:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_order_order_time_alter_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='expected',
            field=models.TimeField(default=datetime.time(16, 21, 39, 179441)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 21, 15, 36, 39, 148194)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.TimeField(default=datetime.time(15, 36, 39, 148194)),
        ),
    ]
