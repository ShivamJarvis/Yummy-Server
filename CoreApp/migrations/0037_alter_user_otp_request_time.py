# Generated by Django 4.1.1 on 2022-10-16 17:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0036_deliverypartner_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_request_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 16, 17, 26, 16, 994194)),
        ),
    ]