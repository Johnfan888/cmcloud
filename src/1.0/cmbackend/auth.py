# /usr/bin/env python
#-*-coding:utf-8-*-
#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
import MySQLdb
from urllib2 import Request,urlopen,URLError,HTTPError
#url and url header
#zabbix的API地址、用户名、密码、这里修改为实际的参数
# sys.path.append('/usr/CMC/')
# from conf import MySQLport,MySQLuser,MySQLpasswd
import ConfigParser
cf=ConfigParser.ConfigParser()
cf.read('/usr/CMC/zabbix_api/cmc.conf')
MySQLport=int(cf.get('db','db_port'))
MySQLuser=cf.get('db','db_user')
MySQLpasswd=cf.get('db','db_passwd')
MYSQLip=cf.get('db','db_host')
# myhostip=cf.get('server','server_ip')
zabbix_url=str(cf.get('zbx','zbx_url'))
zabbix_user=str(cf.get('zbx','zbx_user'))
zabbix_pass=str(cf.get('zbx','zbx_pass'))
zabbix_header1=cf.get('zbx','zbx_header')
zabbix_header=eval(zabbix_header1)
auth_code=''



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
# print zabbix_url
# print type(zabbix_url)
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
# 判断SESSIONID是否在返回的数据中
if 'result' in response0:
        auth_code = response0['result']
else:
        print response0['error']['data']