# Generated by Django 4.1.1 on 2022-10-06 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0009_alter_cart_restraunt'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
