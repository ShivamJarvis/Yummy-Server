# Generated by Django 4.1.1 on 2022-10-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0026_orderitem_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Recieved', 'Order Recieved'), ('Order Confirmed', 'Order Confirmed'), ('Preparing Order', 'Preparing Order'), ('Delivery Partner at Restraunt', 'Delivery Partner at Restraunt'), ('Order Picked Up', 'Order Picked Up'), ('Order Delivery', 'Order Delivery')], default='Order Recieved', max_length=50),
        ),
    ]
