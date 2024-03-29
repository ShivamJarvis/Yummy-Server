# Generated by Django 4.1.1 on 2022-10-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestrauntApp', '0015_restrauntsectionhead'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestrauntSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('restraunts', models.ManyToManyField(blank=True, related_name='section_restraunt', to='RestrauntApp.restraunt')),
            ],
        ),
        migrations.DeleteModel(
            name='RestrauntSectionHead',
        ),
    ]
