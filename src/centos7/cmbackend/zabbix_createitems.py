#!/usr/bin/env python
# -*- encoding: utf8 -*-

#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
import MySQLdb
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code
# from read import itemKey,itemName,hostId,valueType,dataType,interfaceId
import  xdrlib ,sys
#request json //create host
json_data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": "cvcvc21",
        "key_": "cvvvvc",
        "hostid": "10167",
        "interfaceid": 58,
        "type": 0,  # 0 - Zabbix agent; 1 - SNMPv1 agent;
        "value_type": 0,  # 0 - numeric float; 1 - character; 2 - log; 3 - numeric unsigned; 4 - text.
        "data_type":3,  # 0 - (default) decimal; 1 - octal; 2 - hexadecimal; 3 - boolean.
        # zai interface biaoli yilaiyu hostid
        "applications": ["959"],#!!!此处需要[]
        "description": "qw",
        "units":"M",
        "delay": 30

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
                print response

                #将所有的主机信息显示出来
                # print response
                #显示主机个数
                # print "Number Of Hosts: ",len(response['result'])
