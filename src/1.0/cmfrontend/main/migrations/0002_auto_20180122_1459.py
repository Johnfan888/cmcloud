# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-22 14:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chostgroups',
            old_name='hostgrouspName',
            new_name='hostgroupsName',
        ),
    ]
