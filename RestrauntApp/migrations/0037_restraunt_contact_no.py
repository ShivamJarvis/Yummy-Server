# Generated by Django 4.1.1 on 2023-02-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0036_customerfavouritesrestraunt'),
    ]

    operations = [
        migrations.AddField(
            model_name='restraunt',
            name='contact_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]