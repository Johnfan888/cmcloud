#!/usr/bin/env python
# -*- encoding: utf8 -*-

#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError

#url and url header
#zabbix的API地址、用户名、密码、这里修改为实际的参数
zabbix_url="http://192.168.18.25/zabbix/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user = "Admin"
zabbix_pass = "zabbix"
auth_code = ""

#auth user and password
#用户认证信息的部分，最终的目的是得到一个SESSIONID
#下面是生成一个JSON格式的数据：用户名和密码
auth_data = json.dumps(
        {
                "jsonrpc" : "2.0",
                "method" : "user.login",
                "params" :
                                {
                                        "user":zabbix_user,
                                        "password":zabbix_pass
                                },
                "id":0
        })

# create request object
request = urllib2.Request(zabbix_url,auth_data)
for key in zabbix_header:
        request.add_header(key,zabbix_header[key])

#认证和获取SESSION ID
try:
        result = urllib2.urlopen(request)
#对于认证出错的处理
except HTTPError,e:
        print 'The server couldn\'t fulfill the request, Error code: ',e.code
except URLError,e:
        print 'We failed to reach a server.Reason: ',e.reason
else:
        response = json.loads(result.read())

'''
#如果访问成功或者失败，这里的数据会显示如下
sucess result:
        {"jsonrpc":"2.0",
         "result": "182395ea90c1c983a6154dbe0b5bdb40",
         "id":0
        }
error result:
        {'code': -32602
         'data': 'Login name or password is incorrect.',
         'message':'Invalid params.'
        }
'''
#判断SESSIONID是否在返回的数据中
if 'result' in response:
        auth_code = response['result']
else:
        print response['error']['data']

#request json //create host
json_data ={
    "jsonrpc": "2.0",
    "method": "action.create",
    "params": {
        "name": "restart server2.httpd",  # action名字
        "eventsource": 0,  # 0 - event created by a trigger;
        # 1 - event created by a discovery rule;
        # 2 - event created by active agent auto-registration;
        # 3 - internal event.
        "status": 0,  # Whether the action is enabled or disabled.  0 - (default) enabled; 1 - disabled.
        "esc_period": 120,
        "def_shortdata": "{TRIGGER.STATUS}: {TRIGGER.NAME}",
        "def_longdata": "{TRIGGER.NAME}: {TRIGGER.STATUS}\r\nLast value: {ITEM.LASTVALUE}\r\n\r\n{TRIGGER.URL}",
        "recovery_msg": 1,
        "r_longdata": "{TRIGGER.NAME}: {TRIGGER.STATUS}\r\nLast value: {ITEM.LASTVALUE}\r\n\r\n{TRIGGER.URL}",
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
                    "value": "13701"  # triggerid
                },
                {
                    "conditiontype": 1,
                    # Possible values for trigger actions: 0 - host group; 1 - host; 2 - trigger; 3 - trigger name;
                    # 4 - trigger severity; 5 - trigger value; 6 - time period; 13 - host template; 15 - application; 16 - maintenance status.
                    "operator": 0,
                    # Possible values: 0 - (default) =; 1 - <>; 2 - like; 3 - not like; 4 - in; 5 - >=; 6 - <=; 7 - not in.
                    "value": "10109"  # hostid
                },
            ]
        },
        "operations":[
            {
                "operationtype": 1,
            ##Possible values: 0 - send message; 1 - remote command; 2 - add host; 3 - remove host; 4 - add to host group; 5 - remove from host group;
                # 6 - link to template; 7 - unlink from template; 8 - enable host; 9 - disable host; 10 - set host inventory mode.
                "esc_period": 120,
                # Duration of an escalation step in seconds. Must be greater than 60 seconds. If set to 0, the default action escalation period will be used.

                # Default: 0.
                "esc_step_from": 1,
                "esc_step_to": 1,
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
                        "hostid": "10109"
                        # Host to run remote commands on. ID of the host; if set to 0 the command will be run on the current host.
                    }
                ],
                "opcommand": {
                    "type": 0,  # Possible values: 0 - custom script; 1 - IPMI; 2 - SSH; 3 - Telnet; 4 - global script.
                    "command": "service httpd restart",  # Command to run.
                    "execute_on": 0,  # Possible values: 0 - Zabbix agent; 1 - Zabbix server.

                }
            }
]

},
    "auth": auth_code,
    "id": 1
}
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

                #将所有的主机信息显示出来
                print response
                #显示主机个数
                #print "Number Of Hosts: ",len(response['result'])
























