# Generated by Django 5.0.2 on 2024-04-18 08:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0012_activity_alter_cancelled_order_cancelled_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(default='profiles/default_profile_pic_128491.jpg', upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 4, 18, 13, 56, 25, 581162)),
        ),
        migrations.AlterField(
            model_name='activity',
            name='time',
            field=models.TimeField(default=datetime.time(13, 56, 25, 581161)),
        ),
        migrations.AlterField(
            model_name='cancelled_order',
            name='cancelled_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 18, 13, 56, 25, 580160)),
        ),
        migrations.AlterField(
            model_name='cancelled_order',
            name='cancelled_time',
            field=models.TimeField(default=datetime.time(13, 56, 25, 580160)),
        ),
        migrations.AlterField(
            model_name='dilivered_order',
            name='dilivery_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 18, 13, 56, 25, 580160)),
        ),
        migrations.AlterField(
            model_name='dilivered_order',
            name='dilivery_time',
            field=models.TimeField(default=datetime.time(13, 56, 25, 580160)),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected',
            field=models.TimeField(default=datetime.time(14, 41, 25, 578161)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 18, 13, 56, 25, 559174)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.TimeField(default=datetime.time(13, 56, 25, 559174)),
        ),
    ]
