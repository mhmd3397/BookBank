# Generated by Django 2.2.4 on 2023-07-26 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='employee',
        ),
    ]
