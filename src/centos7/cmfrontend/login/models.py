#encoding:utf-8
from __future__ import unicode_literals

from django.db import models

class Admin(models.Model):
    user = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    # 返回相应的值
    def __unicode__(self):
         return self.user