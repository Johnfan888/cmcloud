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

name="text1950"
osc=120
trigger="14505"
stepduration1=[60,60]
stepduration2=[60,60]
from1=[1,2]
to1=[1,2]
host=[10167,10167]
command=[12,12]
from2=[1,2]
to2=[1,2]
mediatype=[4,4]

# ---------执行命令------------
json_command=[]
n=len(from1)
for m in range(n):
    json_command1={
                    "operationtype": 1,
                ##Possible values: 0 - send message; 1 - remote command; 2 - add host; 3 - remove host; 4 - add to host group; 5 - remove from host group;
                    # 6 - link to template; 7 - unlink from template; 8 - enable host; 9 - disable host; 10 - set host inventory mode.
                    "esc_period": stepduration1[m],
                    # Duration of an escalation step in seconds. Must be greater than 60 seconds. If set to 0, the default action escalation period will be used.

                    # Default: 0.
                    "esc_step_from": from1[m],
                    "esc_step_to": to1[m],
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
                            "hostid": host[m],
                            # Host to run remote commands on. ID of the host; if set to 0 the command will be run on the current host.
                        }
                    ],
                    "opcommand": {
                        "type": 0,  # Possible values: 0 - custom script; 1 - IPMI; 2 - SSH; 3 - Telnet; 4 - global script.
                        "command": command[m],  # Command to run.
                        "execute_on": 0,  # Possible values: 0 - Zabbix agent; 1 - Zabbix server.

                    }
                }
    json_command.append(json_command1)  # 加入[]
# json_command = ','.join(str(l) for l in json_command)  # 将数组的[]去掉
#----------发邮件------------
json_mail=[]
i=len(from2)
for j in range(i):
    json_mail1 ={
                            "operationtype": 0,
                            "esc_period": stepduration2[j],
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

    json_mail.append(json_mail1)#加入[]
# json_mail=','.join(str(k) for k in json_mail)#将数组的[]去掉
#--------------------拼接直接相加list------

json_html= json_command + json_mail
#类型list三者均是
# print type(json_command)
# print type(json_mail)
# print type(json_html)
# print json_html
#     #request json //create host
json_data ={
            "jsonrpc": "2.0",
            "method": "action.create",
            "params": {
                "name":name,  # action名字
                "eventsource": 0,  # 0 - event created by a trigger;
                # 1 - event created by a discovery rule;
                # 2 - event created by active agent auto-registration;
                # 3 - internal event.
                "status": 0,  # Whether the action is enabled or disabled.  0 - (default) enabled; 1 - disabled.
                "esc_period": osc,
                "def_shortdata": "{TRIGGER.STATUS}: {TRIGGER.NAME}",
                "def_longdata": "{\r\n\"Trigger status\": \"{TRIGGER.STATUS}\",\r\n\"Trigger name\": \"{TRIGGER.NAME}\",\r\n\"Trigger severity\": \"{TRIGGER.SEVERITY}\",\r\n\"Action name\": \"{ACTION.NAME}\",\r\n\"Event ID\": \"{EVENT.ID}\",\r\n\"Event value\": \"{EVENT.VALUE}\",\r\n\"Event status\": \"{EVENT.STATUS}\", \r\n\"Event time\": \"{EVENT.TIME}\",\r\n\"Event date\": \"{EVENT.DATE}\",\r\n\"Event age\": \"{EVENT.AGE}\",\r\n\"Event acknowledgement\": \"{EVENT.ACK.STATUS}\",\r\n\"Event acknowledgement history\": \"{EVENT.ACK.HISTORY}\",\r\n\"Item values\": \"{ITEM.NAME1} ({HOST.NAME1}:{ITEM.KEY1}): {ITEM.VALUE1}\",\r\n\"Original event ID\": \"{EVENT.ID}}\"",
                "r_longdata": "{\r\n\"Trigger status\": \"{TRIGGER.STATUS}\",\r\n\"Trigger name\": \"{TRIGGER.NAME}\",\r\n\"Trigger severity\": \"{TRIGGER.SEVERITY}\",\r\n\"Action name\": \"{ACTION.NAME}\",\r\n\"Event ID\": \"{EVENT.ID}\",\r\n\"Event value\": \"{EVENT.VALUE}\",\r\n\"Event status\": \"{EVENT.STATUS}\", \r\n\"Event time\": \"{EVENT.TIME}\",\r\n\"Event date\": \"{EVENT.DATE}\",\r\n\"Event age\": \"{EVENT.AGE}\",\r\n\"Event acknowledgement\": \"{EVENT.ACK.STATUS}\",\r\n\"Event acknowledgement history\": \"{EVENT.ACK.HISTORY}\",\r\n\"Item values\": \"{ITEM.NAME1} ({HOST.NAME1}:{ITEM.KEY1}): {ITEM.VALUE1}\",\r\n\"Original event ID\": \"{EVENT.ID}}\"",
                "r_shortdata": "{TRIGGER.STATUS}: {TRIGGER.NAME}",
                "filter": {
                    "evaltype": 0,  # 0 - and/or; 1 - and; 2 - or; 3 - custom expression.
                    "conditions": [
                        {
                            "conditiontype": 2,
                            # Possible values for trigger actions: 0 - host group; 1 - host; 2 - trigger; 3 - trigger name;
                            # 4 - trigger severity; 5 - trigger value; 6 - time period; 13 - host template; 15 - application; 16 - maintenance status.
                            "operator": 0,
                            # Possible values: 0 - (default) =; 1 - <>; 2 - like; 3 - not like; 4 - in; 5 - >=; 6 - <=; 7 - not in.
                            "value": trigger # triggerid
                        },
                        # {
                            # "conditiontype": 1,
                            # Possible values for trigger actions: 0 - host group; 1 - host; 2 - trigger; 3 - trigger name;
                            # 4 - trigger severity; 5 - trigger value; 6 - time period; 13 - host template; 15 - application; 16 - maintenance status.
                            # "operator": 0,
                            # Possible values: 0 - (default) =; 1 - <>; 2 - like; 3 - not like; 4 - in; 5 - >=; 6 - <=; 7 - not in.
                            # "value": "10124"  # hostid
                        # },
                    ],


                },
                "operations": json_html,
                "recovery_operations":json_html,

        },
            "auth": auth_code,
            "id": 1
        }

# print type(json_data)
# print json_data
#
         #用得到的SESSIONID去验证，获取主机的信息(用http.get方法)
if len(auth_code) == 0:
        sys.exit(1)
if len(auth_code) != 0:
        host_create_data = json.dumps(json_data)

        #create request object
        request = urllib2.Request(zabbix_url,host_create_data)
        for key in zabbix_header:
                request.add_header(key,zabbix_header[key])

#get host list
        try:
                result = urllib2.urlopen(request)
        except URLError as e:
                if hasattr(e,'reason'):
                        print 'We failed to reach a server.'
                        print 'Reason: ',e.reason
                elif hasattr(e,'code'):
                        print 'The server could not fulfill the request.'
                        print 'Error code: ',e.code
        else:
                response = json.loads(result.read())
                result.close()
                print response

















