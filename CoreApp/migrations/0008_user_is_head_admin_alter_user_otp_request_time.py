# Generated by Django 4.1.1 on 2022-09-30 07:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0007_alter_user_otp_request_time_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_head_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_request_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 30, 13, 5, 17, 211104)),
        ),
    ]