# Generated by Django 4.1.1 on 2022-10-15 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0023_remove_order_latitude_remove_order_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='additional_items',
            field=models.TextField(blank=True, null=True),
        ),
    ]
