# Generated by Django 4.1.1 on 2022-10-15 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0025_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='qty',
            field=models.IntegerField(default=0),
        ),
    ]
