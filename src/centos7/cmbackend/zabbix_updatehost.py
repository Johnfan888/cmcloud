#!/usr/bin/env python
# -*- encoding: utf8 -*-

#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
import  xdrlib ,sys
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code

# sys.path.append('/usr/CMC/main/')
#
# import views
# from views import add_host
# views.add_host( 'add_host_data' )


#request json //create host

ip="192.168.1.222"

json_data = {
        "jsonrpc": "2.0",
        "method": "host.update",
        "params": {
            "hostid": "10177",
            "host":"cdcddcd123",
                    # "host": "hhh33",
            # "interface":
            # {
            #
            #     "ip": "192.168.1.122",
            # }
            #         ,
            # "ip":ip,
            "groups":
                        {
                            # "groupid": '4'
                    "groupid": "17",
                        },
            "templates":
                        {
                            # "templateid": '10001'
                    "templateid": "10001"
                        },
                },
        "auth": auth_code,
        "id": 1
            }
# print json_data

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


