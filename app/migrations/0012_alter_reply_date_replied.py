# Generated by Django 5.0.4 on 2024-06-04 04:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='date_replied',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]