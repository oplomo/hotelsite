# Generated by Django 5.0.6 on 2024-05-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='entry',
            field=models.CharField(default='to be communicated', max_length=200),
        ),
    ]
