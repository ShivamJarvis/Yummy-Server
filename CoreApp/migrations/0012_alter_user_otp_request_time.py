# Generated by Django 4.1.1 on 2022-10-06 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0011_alter_user_otp_request_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_request_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 12, 50, 46, 426249)),
        ),
    ]
