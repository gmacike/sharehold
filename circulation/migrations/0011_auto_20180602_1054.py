# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-02 08:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0010_auto_20180414_1304'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ClientHasBoardGame',
            new_name='BoardGameLending',
        ),
    ]