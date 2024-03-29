# Generated by Django 4.1.1 on 2022-10-20 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RestrauntApp', '0034_restraunt_is_new'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerSearches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('restraunt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recent_search_restraunt', to='RestrauntApp.restraunt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recent_search_restraunt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
