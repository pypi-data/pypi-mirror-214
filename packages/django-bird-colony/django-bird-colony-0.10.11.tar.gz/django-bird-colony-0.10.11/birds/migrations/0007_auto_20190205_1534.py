# Generated by Django 2.1.5 on 2019-02-05 20:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0006_auto_20190125_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, help_text='date of sample collection (blank if not known)', null=True),
        ),
    ]
