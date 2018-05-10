# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-31 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_cinterface'),
    ]

    operations = [
        migrations.CreateModel(
            name='citem',
            fields=[
                ('itemId', models.SmallIntegerField(max_length=8, primary_key=True, serialize=False)),
                ('itemName', models.CharField(max_length=255)),
                ('itemKey', models.CharField(max_length=255)),
                ('itemStatus', models.IntegerField(max_length=1)),
                ('templateId', models.IntegerField(max_length=8)),
                ('hostId', models.IntegerField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='citemgroups',
            fields=[
                ('itemgroupsId', models.IntegerField(max_length=8, primary_key=True, serialize=False)),
                ('itemgroupsName', models.CharField(max_length=50)),
                ('hostId', models.IntegerField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='ctrigger',
            fields=[
                ('triggerId', models.IntegerField(max_length=8, primary_key=True, serialize=False)),
                ('triggerName', models.CharField(max_length=255)),
                ('triggerValue', models.IntegerField(max_length=8)),
                ('triggerPriority', models.IntegerField(max_length=8)),
                ('itemId', models.IntegerField(max_length=8)),
            ],
        ),
    ]