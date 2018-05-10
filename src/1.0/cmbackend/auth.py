# /usr/bin/env python
#-*-coding:utf-8-*-
#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
#url and url header
#zabbix的API地址、用户名、密码、这里修改为实际的参数

zabbix_url="http://192.168.1.89/zabbix/api_jsonrpc.php"
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
request0 = urllib2.Request(zabbix_url,auth_data)
for key in zabbix_header:
        request0.add_header(key,zabbix_header[key])

#认证和获取SESSION ID
try:
        result = urllib2.urlopen(request0)
#对于认证出错的处理
except HTTPError,e:
        print 'The server couldn\'t fulfill the request, Error code: ',e.code
except URLError,e:
        print 'We failed to reach a server.Reason: ',e.reason
else:
        response0 = json.loads(result.read())

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
if 'result' in response0:
        auth_code = response0['result']
else:
        print response0['error']['data']