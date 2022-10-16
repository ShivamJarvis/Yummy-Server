# Generated by Django 4.1.1 on 2022-10-15 12:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0025_alter_user_otp_request_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_request_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 12, 58, 45, 151118)),
        ),
        migrations.CreateModel(
            name='DeliveryPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_orders_count', models.IntegerField(default=0)),
                ('total_cancellation_count', models.IntegerField(default=0)),
                ('is_cod_applicable', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_partner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]