# Generated by Django 4.1.1 on 2022-10-10 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0013_remove_cartcustomiseditem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='restrauntmenu',
            name='preparation_time',
            field=models.IntegerField(default=0),
        ),
    ]
