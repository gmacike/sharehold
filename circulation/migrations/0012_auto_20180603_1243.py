# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-03 10:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0011_auto_20180602_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientid',
            name='rentalClient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clientIDs', to='circulation.RentalClient'),
        ),
    ]
