# Generated by Django 5.0.6 on 2024-05-26 02:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesatransaction',
            name='phone_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.phonenumber'),
        ),
    ]
