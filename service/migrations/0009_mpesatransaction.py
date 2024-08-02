# Generated by Django 5.0.6 on 2024-05-26 01:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_roomavailability_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MPesaTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('payment not made', 'Not Payed')], max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mpesa_transactions', to='service.booking')),
            ],
        ),
    ]
