# Generated by Django 5.0.6 on 2024-05-21 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_room_image_roomtype_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='is_available',
        ),
    ]
