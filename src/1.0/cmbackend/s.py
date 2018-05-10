#!/usr/bin/env python
# -*- encoding: utf8 -*-

#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
# import MySQLdb
# from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code
#url and url header
#zabbix的API地址、用户名、密码、这里修改为实际的参数
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code,auth_data

name="text2123"
osc=120
trigger="14368"
stepduration="120"
from1=3
to1=3
host="10166"
command="12"
from2=[1,2]
to2=[1,2]
mediatype=[4,4]
i=len(from2)
# ---------执行命令------------
json_command1={
                "operationtype": 1,
            ##Possible values: 0 - send message; 1 - remote command; 2 - add host; 3 - remove host; 4 - add to host group; 5 - remove from host group;
                # 6 - link to template; 7 - unlink from template; 8 - enable host; 9 - disable host; 10 - set host inventory mode.
                "esc_period": stepduration,
                # Duration of an escalation step in seconds. Must be greater than 60 seconds. If set to 0, the default action escalation period will be used.

                # Default: 0.
                "esc_step_from": from1,
                "esc_step_to": to1,
                "evaltype": 0,
                "opconditions": [
                    {
                        "conditiontype": 14,  # Type of condition. Possible values: 14 - event acknowledged.
                        "operator": 0,  #
                        "value": "0"
                    }
                ],
                # "opcommand_grp": [
                #   {
                #      "groupid": "2"#Host groups to run remote commands on.
                # }
                # ],
                "opcommand_hst": [
                    {
                        "hostid": host
                        # Host to run remote commands on. ID of the host; if set to 0 the command will be run on the current host.
                    }
                ],
                "opcommand": {
                    "type": 0,  # Possible values: 0 - custom script; 1 - IPMI; 2 - SSH; 3 - Telnet; 4 - global script.
                    "command": command,  # Command to run.
                    "execute_on": 0,  # Possible values: 0 - Zabbix agent; 1 - Zabbix server.

                }
            }
json_command = json.dumps(json_command1)#dict转json
#----------发邮件------------
json_mail2=[]
for j in range(i):
    json_mail1 ={
                            "operationtype": 0,
                            "esc_period": 0,
                            "esc_step_from": from2[j],
                            "esc_step_to": to2[j],
                            "evaltype": 0,
                            "opmessage_grp": [
                                {
                                    "usrgrpid": "7"
                                }
                            ],
                            "opmessage": {
                                "default_msg": 1,
                                "mediatypeid":mediatype[j],
                            }
                        }
    json_mail1 = json.dumps(json_mail1)#dict转json
    json_mail2.append(json_mail1)#加入[]
json_mail3=','.join(str(n) for n in json_mail2)#将数组的[]去掉
b=eval(json_mail3)
dictMerged=b.copy()
dictMerged.update(json_command)
print dictMerged
#
#
#                     # ---------------------
# json_html=[
#                     # -------------------------------------第一步命令------------------------------------------------
#                    json_command,json_mail3
#                     # -------------------------第二步发邮件-------------------------------------
#
#         ]



    # -----------------
#     #request json //create host
# json_data1 ={
#             "jsonrpc": "2.0",
#             "method": "action.create",
#             "params": {
#                 "name":name,  # action名字
#                 "eventsource": 0,  # 0 - event created by a trigger;
#                 # 1 - event created by a discovery rule;
#                 # 2 - event created by active agent auto-registration;
#                 # 3 - internal event.
#                 "status": 0,  # Whether the action is enabled or disabled.  0 - (default) enabled; 1 - disabled.
#                 "esc_period": osc,
#                 "def_shortdata": "{TRIGGER.STATUS}: {TRIGGER.NAME}",
#                 "def_longdata": "{TRIGGER.NAME}: {TRIGGER.STATUS}\r\nLast value: {ITEM.LASTVALUE}\r\n\r\n{TRIGGER.URL}",
#                 "recovery_msg": 1,
#                 "r_longdata": "{TRIGGER.NAME}: {TRIGGER.STATUS}\r\nLast value: {ITEM.LASTVALUE}\r\n\r\n{TRIGGER.URL}",
#                 "r_shortdata": "{TRIGGER.STATUS}: {TRIGGER.NAME}",
#                 "filter": {
#                     "evaltype": 0,  # 0 - and/or; 1 - and; 2 - or; 3 - custom expression.
#                     "conditions": [
#                         {
#                             "conditiontype": 2,
#                             # Possible values for trigger actions: 0 - host group; 1 - host; 2 - trigger; 3 - trigger name;
#                             # 4 - trigger severity; 5 - trigger value; 6 - time period; 13 - host template; 15 - application; 16 - maintenance status.
#                             "operator": 0,
#                             # Possible values: 0 - (default) =; 1 - <>; 2 - like; 3 - not like; 4 - in; 5 - >=; 6 - <=; 7 - not in.
#                             "value": trigger # triggerid
#                         },
#                         # {
#                             # "conditiontype": 1,
#                             # Possible values for trigger actions: 0 - host group; 1 - host; 2 - trigger; 3 - trigger name;
#                             # 4 - trigger severity; 5 - trigger value; 6 - time period; 13 - host template; 15 - application; 16 - maintenance status.
#                             # "operator": 0,
#                             # Possible values: 0 - (default) =; 1 - <>; 2 - like; 3 - not like; 4 - in; 5 - >=; 6 - <=; 7 - not in.
#                             # "value": "10124"  # hostid
#                         # },
#                     ],
#
#
#                 },
#                 "operations": json_html,
#
#
#         },
#             "auth": auth_code,
#             "id": 1
#         }
# json_data2 = json.dumps(json_data1)#dict转json
# json_data = json.loads(json_data2)#去除斜杠，去完s又成单引号了
#
# print json_data
#
#          #用得到的SESSIONID去验证，获取主机的信息(用http.get方法)
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
#                 # print response

















