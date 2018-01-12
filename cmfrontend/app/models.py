# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

#新增元组用于设置消息类型枚举项
KIND_CHOICES = (
	('0','其他'),
	('1','硬件故障'),
	('2','网络故障'),
	('3','服务型故障'),
	('4','数据库故障'),
)

#Create your models here.
class Moment(models.Model):
   fault_type = models.CharField(max_length=20,choices = KIND_CHOICES,default = KIND_CHOICES[0])
   fault_title =  models.CharField(max_length=20)
   fault_describe = models.CharField(max_length=200)
   fault_address = models.CharField(max_length=30)
   pub_date = models.DateTimeField(default=timezone.now)
  
   class Meta:
      ordering = ('-pub_date',) 
   def __unicode__(self):
      return self.fault_title


LAN_CHOICES = (
	('Python','Python'),
	('Java','Java'),
	('C','C'),
	('C++','C++'),
	('Php','Php'),
)
HOSTNUM_CHOICES=(
        ('0','单个'),
        ('1','多个'),
        )
class Diagonos(models.Model):
	moment = models.OneToOneField(
		Moment,
		on_delete=models.CASCADE,
		primary_key = True,
	)
	dgs_hosttype = models.IntegerField(choices=HOSTNUM_CHOICES,default=HOSTNUM_CHOICES[0])
	dgs_host = models.GenericIPAddressField(max_length=50)
	dgs_hostrange = models.CharField(max_length=50,blank=True)
	dgs_codeN = models.IntegerField(default=1)
	dgs_codeP = models.IntegerField(default=1,blank=True,null=True)
	dgs_codeL = models.CharField(max_length=20,choices=LAN_CHOICES,default=LAN_CHOICES[0])
	dgs_codeA = models.CharField(max_length=30)
	pub_date = models.DateTimeField(default=timezone.now)
   
	def __unicode__(self):
		return "%s,%s" % (self.moment.fault_address,self.dgs_hosttype)
