# Generated by Django 4.1.1 on 2022-09-30 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RestrauntApp', '0006_restrauntmenu_is_customisable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_total', models.FloatField(default=0)),
                ('restraunt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restraunt_cart', to='RestrauntApp.restrauntbranch')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
