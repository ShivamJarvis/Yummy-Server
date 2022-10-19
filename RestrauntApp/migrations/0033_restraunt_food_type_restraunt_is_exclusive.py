# Generated by Django 4.1.1 on 2022-10-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0032_restraunt_cost_of_two'),
    ]

    operations = [
        migrations.AddField(
            model_name='restraunt',
            name='food_type',
            field=models.CharField(choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg'), ('Both', 'Both')], default='Veg', max_length=40),
        ),
        migrations.AddField(
            model_name='restraunt',
            name='is_exclusive',
            field=models.BooleanField(default=False),
        ),
    ]
