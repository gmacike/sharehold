# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-23 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0022_auto_20180623_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgamelending',
            name='issued',
            field=models.DateTimeField(),
        ),
    ]
