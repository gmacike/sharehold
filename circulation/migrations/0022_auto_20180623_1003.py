# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-23 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0021_auto_20180619_2159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='initials',
            new_name='nick',
        ),
    ]
