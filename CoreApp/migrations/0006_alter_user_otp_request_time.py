# Generated by Django 4.1.1 on 2022-09-27 06:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0005_user_current_otp_user_otp_request_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_request_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 12, 14, 37, 11873)),
        ),
    ]
