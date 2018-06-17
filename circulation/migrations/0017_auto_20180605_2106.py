# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-05 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0016_auto_20180605_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDlabel', models.CharField(max_length=12, unique=True, verbose_name='Identyfikator')),
                ('IDstatus', models.IntegerField(default=0, verbose_name='Status identyfikatora')),
            ],
        ),
        migrations.RenameModel(
            old_name='RentalClient',
            new_name='Customer',
        ),
        migrations.RemoveField(
            model_name='clientid',
            name='rentalClient',
        ),
        migrations.DeleteModel(
            name='ClientID',
        ),
        migrations.AddField(
            model_name='customerid',
            name='Customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CustomerIDs', to='circulation.Customer'),
        ),
    ]