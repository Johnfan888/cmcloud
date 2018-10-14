#!/usr/bin/env python
# -*- encoding: utf8 -*-
#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code,MySQLport,MySQLuser,MySQLpasswd
import MySQLdb
triggerName=["httpnetnet"]
conn = MySQLdb.connect(
            host='localhost',
            port=MySQLport,
            user=MySQLuser,
            passwd=MySQLpasswd,
            db='cmc',
            charset='utf8',
        )
cur = conn.cursor()
sql = "select `condition` from main_ctrigger where triggerName=%s"
cur.execute(sql,triggerName)
condition = cur.fetchone()#取到eventId,
print condition[0]

conn.commit()
cur.close()
conn.close()

t_condition=condition[0]+" and "+ "{%s:get.http.last()}=%s"



#request json //create host
# json_data = {
#                 "jsonrpc": "2.0",
#                 "method": "trigger.update",
#                 "params": {
#                     "triggerid": 14599,
#                     # "description": triggersname,
#                     "expression": condition,
#                     # "comments": description,
#                     # "priority": severity
#                 },
#                 "auth": auth_code,
#                 "id": 1
#             }
#
#
# #用得到的SESSIONID去验证，获取主机的信息(用http.get方法)
#
# if len(auth_code) == 0:
#         sys.exit(1)
# if len(auth_code) != 0:
#         host_create_data = json.dumps(json_data)
#
#         #create request object
#         request = urllib2.Request(zabbix_url,host_create_data)
#         for key in zabbix_header:
#                 request.add_header(key,zabbix_header[key])
#
# #get host list
#         try:
#                 result = urllib2.urlopen(request)
#         except URLError as e:
#                 if hasattr(e,'reason'):
#                         print 'We failed to reach a server.'
#                         print 'Reason: ',e.reason
#                 elif hasattr(e,'code'):
#                         print 'The server could not fulfill the request.'
#                         print 'Error code: ',e.code
#         else:
#                 response = json.loads(result.read())
#                 result.close()
#                 print response


