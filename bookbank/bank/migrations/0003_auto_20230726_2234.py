# Generated by Django 2.2.4 on 2023-07-26 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_remove_appointment_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='bank.User'),
        ),
    ]
