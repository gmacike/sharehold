# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-24 09:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_rentalclient'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RentalClient',
        ),
    ]