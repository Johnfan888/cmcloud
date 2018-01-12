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
    "method": "host.create",
    "params": {

        "host": "qule",
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "192.168.18.26",
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": "4"
            }
        ],
        "templates": [
            {
                "templateid": "10001"
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
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
                print "Number Of Hosts: ",len(response['result'])

