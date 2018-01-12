# /usr/bin/env python
# encoding:utf-8
import json
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import yaml

def  Zabbix_Url_Request(zabbix_url,data,zabbix_header,*args,**kwargs):
    #print data
    # create request object
    request = urllib2.Request(zabbix_url, data, zabbix_header)
    try:
        result = urllib2.urlopen(request)
    # 对于出错新的处理
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request, Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.Reason: ', e.reason
    else:
        response = json.loads(result.read())
        #print  response
        return response
        result.close()


def Zabbix_Auth_Code(zabbix_url,zabbix_header,*args,**kwargs):
    with open('config.ymal') as f:
        result = yaml.load(f)
    result_zabbix_info = result['Zabbix_Config']
    zabbix_user = result_zabbix_info['zabbix_user']
    zabbix_pass = result_zabbix_info['zabbix_pass']
    # auth user and password
    # 用户认证信息的部分，最终的目的是得到一个SESSIONID
    # 这里是生成一个json格式的数据，用户名和密码
    auth_data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params":
                {
                    "user": zabbix_user,
                    "password": zabbix_pass
                },
            "id": 0
        })
    response = Zabbix_Url_Request(zabbix_url,auth_data,zabbix_header)
    # print response
    if 'result' in response:
        #print response
        return  response['result'],response['id']

    else:
        print  response['error']['data']
