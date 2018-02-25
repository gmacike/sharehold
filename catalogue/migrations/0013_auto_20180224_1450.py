# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-24 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0012_auto_20180224_1357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardgamecommodity',
            old_name='frontImage',
            new_name='boxFrontImage',
        ),
        migrations.RenameField(
            model_name='boardgamecommodity',
            old_name='topImage',
            new_name='boxTopImage',
        ),
        migrations.RemoveField(
            model_name='boardgamecommodity',
            name='sideImage',
        ),
        migrations.AddField(
            model_name='boardgamecommodity',
            name='boxSideImage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
