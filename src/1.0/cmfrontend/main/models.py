#-*-coding:utf-8-*-
from __future__ import unicode_literals

from django.db import models


#主机表
class chost(models.Model):
    hostId = models.IntegerField(primary_key=True, max_length=8)
    hostName = models.CharField(max_length=255)
    hostStatus = models.IntegerField(max_length=2)
    hostgroupsId = models.IntegerField(max_length=8)
    templatesId = models.IntegerField(null=True,max_length=10)
    hostIp = models.CharField(max_length=255)


    # 返回相应的值
    def __unicode__(self):
         # return self.hostName
            return str(self.hostName)
#主机组表
class chostgroups(models.Model):
    hostgroupsId = models.IntegerField(primary_key=True, max_length=8)
    hostgroupsName = models.CharField(max_length=255)
    # 返回相应的值
    def __unicode__(self):
        return self.hostgroupsId

#模板表
class ctemplates(models.Model):
    templatesId = models.IntegerField(primary_key=True, max_length=8)
    templatesName = models.CharField(max_length=255)
    hostgroupsId = models.IntegerField(max_length=8)
    # 返回相应的值
    def __unicode__(self):
         # return self.templatesId
        return self.templatesId
#主机接口表
class cinterface(models.Model):
    interfaceId = models.IntegerField(primary_key=True, max_length=8)
    hostId = models.IntegerField(max_length=10)
    hostIp = models.CharField(max_length=255)

    # 返回相应的值
    def __unicode__(self):
         return self.interfaceId

#监控组表
class citemgroups(models.Model):
    itemgroupsId = models.IntegerField(primary_key=True, max_length=10)
    itemgroupsName = models.CharField(max_length=255)
    hostId = models.IntegerField(max_length=10)

    # 返回相应的值
    def __unicode__(self):
         # return str(self.itemgroupsId)
        return self.itemgroupsId
#监控表
class citem(models.Model):
    itemId = models.IntegerField(primary_key=True, max_length=10)
    itemName = models.CharField(max_length=255)
    itemKey = models.CharField(max_length=255)
    itemStatus = models.IntegerField(max_length=1)
    # templateId = models.IntegerField(null=True,max_length=10)
    hostId = models.IntegerField(max_length=10)
    interfaceId = models.IntegerField(max_length=8)
    valuetype = models.IntegerField(null=True,max_length=2)
    datatype = models.IntegerField(null=True,max_length=2)
    units = models.CharField(null=True,max_length=255)
    applicationId = models.IntegerField(null=True,max_length=10)
    description = models.CharField(null=True,max_length=255)

    # 返回相应的值
    def __unicode__(self):
         return self.itemId

#触发器表
class ctrigger(models.Model):
    triggerId = models.IntegerField(primary_key=True,max_length=10)
    triggerName = models.CharField(max_length=255)
    triggerValue = models.IntegerField(max_length=10)
    triggerPriority = models.IntegerField(max_length=10)
    itemId = models.IntegerField(max_length=10)
    triggerDescription = models.CharField(null=True,max_length=255)
    condition = models.CharField(max_length=255)
    # 返回相应的值
    def __unicode__(self):
         return self.triggerId

#恢复表
class crecovery(models.Model):
    recoveryTime = models.CharField(max_length=255)
    recoveryDate = models.CharField(max_length=255)
    actionName = models.CharField(max_length=255)
    triggerStatus = models.CharField(max_length=50)
    itemValues = models.CharField(max_length=50)
    triggerSeverity = models.CharField(max_length=50)
    eventId = models.IntegerField(primary_key=True)
    eventStatus= models.CharField(max_length=10)
    eventValue = models.IntegerField(max_length=10)
    originaleventID = models.IntegerField(max_length=10)
    triggerName = models.CharField(max_length=255)
    returnValue = models.CharField(null=True,max_length=255)
    # 返回相应的值
    def __unicode__(self):
         return self.eventId
#恢复表-旧
class crecovery_old(models.Model):
    recoveryTime = models.CharField(max_length=255)
    recoveryDate = models.CharField(max_length=255)
    actionName = models.CharField(max_length=255)
    triggerStatus = models.CharField(max_length=50)
    itemValues = models.CharField(max_length=50)
    triggerSeverity = models.CharField(max_length=50)
    eventId = models.IntegerField(primary_key=True)
    eventStatus= models.CharField(max_length=10)
    eventValue = models.IntegerField(max_length=10)
    originaleventID = models.IntegerField(max_length=10)
    triggerName = models.CharField(max_length=255)
    returnValue = models.CharField(null=True,max_length=255)

    # 返回相应的值
    def __unicode__(self):
         return self.eventId
#恢复表—新
class crecovery_new(models.Model):
    recoveryTime = models.CharField(max_length=255)
    recoveryDate = models.CharField(max_length=255)
    actionName = models.CharField(max_length=255)
    triggerStatus = models.CharField(max_length=50)
    itemValues = models.CharField(max_length=50)
    triggerSeverity = models.CharField(max_length=50)
    eventId = models.IntegerField(primary_key=True)
    eventStatus= models.CharField(max_length=10)
    eventValue = models.IntegerField(max_length=10)
    originaleventID = models.IntegerField(max_length=10)
    triggerName = models.CharField(max_length=255)
    returnValue = models.CharField(null=True,max_length=255)
    # 返回相应的值
    def __unicode__(self):
         return self.eventId
#动作表
class caction(models.Model):
    actionId = models.IntegerField(primary_key=True, max_length=8)
    actionName = models.CharField(max_length=255)
    actionStatus = models.IntegerField( max_length=8)
    actionStepPeriod = models.CharField(max_length=255)
    triggerId = models.IntegerField(null=True,max_length=8)
    actionCommand = models.CharField(null=True,max_length=255)
    actionMessage = models.CharField(null=True, max_length=255)



    # 返回相应的值
    def __unicode__(self):
         # return self.hostName
            return str(self.actionId)