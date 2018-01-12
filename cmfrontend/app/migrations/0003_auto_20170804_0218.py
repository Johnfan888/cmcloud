# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-04 02:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170728_0322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moment',
            name='content',
        ),
        migrations.RemoveField(
            model_name='moment',
            name='kind',
        ),
        migrations.RemoveField(
            model_name='moment',
            name='user_name',
        ),
        migrations.AddField(
            model_name='moment',
            name='fault_address',
            field=models.CharField(default='192.168.18.22', max_length=30),
        ),
        migrations.AddField(
            model_name='moment',
            name='fault_describe',
            field=models.CharField(default='zabbix server httpd down', max_length=200),
        ),
        migrations.AddField(
            model_name='moment',
            name='fault_title',
            field=models.CharField(default='httpddown', max_length=20),
        ),
        migrations.AddField(
            model_name='moment',
            name='fault_type',
            field=models.CharField(choices=[('0', '\u5176\u4ed6'), ('1', '\u786c\u4ef6\u6545\u969c'), ('2', '\u7f51\u7edc\u6545\u969c'), ('3', '\u670d\u52a1\u578b\u6545\u969c'), ('4', '\u6570\u636e\u5e93\u6545\u969c')], default=('0', '\u5176\u4ed6'), max_length=20),
        ),
        migrations.AddField(
            model_name='moment',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
