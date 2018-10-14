# -*- encoding: utf8 -*-
import yaml
import MySQLdb
import commands
fr= open('/etc/zabbix/aa/shiyan.yaml',"r")
aa= yaml.load(fr)
mm='http'
# print aa,type(aa)
bb=[]
for i in aa:
    if '%s'%(mm) in i:
        # print type(i)
        # print type(aa[i])
        cc={'actionStepName':i,'returnValue':aa[i]['value']}

        bb.append(cc)

print bb




# 连接数据库

# fr.close()

