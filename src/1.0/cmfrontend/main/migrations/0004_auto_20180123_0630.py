# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-23 06:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_ctemplates'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ctemplates',
            old_name='templateId',
            new_name='templatesId',
        ),
        migrations.RenameField(
            model_name='ctemplates',
            old_name='templateName',
            new_name='templatesName',
        ),
    ]
