# Generated by Django 5.0.6 on 2024-05-26 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_alter_mpesatransaction_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesatransaction',
            name='transaction_id',
            field=models.CharField(max_length=100),
        ),
    ]
