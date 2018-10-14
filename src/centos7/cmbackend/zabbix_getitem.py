#!/usr/bin/env python
# -*- encoding: utf8 -*-

# 导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request, urlopen, URLError, HTTPError
from auth import zabbix_header,zabbix_user,zabbix_url,zabbix_pass,auth_code,auth_data,auth_code,MySQLport,MySQLuser,MySQLpasswd
import MySQLdb
json_data = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": "extend",
        "selectApplications":"extend",
        # "hostids": "10177",
        # "itemids":"27726"

    },
}
json_base = {
    "jsonrpc": "2.0",
    "auth": auth_code,
    "id": 1
}

json_data.update(json_base)
# 用得到的SESSIONID去验证，获取主机的信息(用http.get方法)
if len(auth_code) == 0:
    sys.exit(1)
if len(auth_code) != 0:
    get_host_data = json.dumps(json_data)

    # create request object
    request = urllib2.Request(zabbix_url, get_host_data)
    for key in zabbix_header:
        request.add_header(key, zabbix_header[key])

    # get host list
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        response = json.loads(result.read())
        result.close()
        # print response

        # print "Number Of Items: ", len(response['result'])
        # 连接数据库
        conn = MySQLdb.connect(
            host='localhost',
            port=MySQLport,
            user=MySQLuser,
            passwd=MySQLpasswd,
            db='cmc',
            charset='utf8',
        )
        cur = conn.cursor()
        # 清空数据库
        sql1 = "DELETE FROM main_citem "
        cur.execute(sql1)
        conn.commit()
        for item in response['result']:
            for i in item['applications']:
                get_data =[ item['itemid'],item['name'],item['key_'],item['status'],item['hostid'],
                        item['interfaceid'],item['value_type'],item['data_type'],item['units'],
                        i['applicationid'],item['description']]
                # print get_data
            # print item['templateid']
            # 连接数据库mysql


            # 插入一条数据
            sql = "insert into main_citem values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            try:
                cur.execute(sql, get_data)  # 执行sql语句
                conn.commit()
                # print "insert success!"
            except:
                # 1
                print "Error: unable to fetch data"
                # print get_data



        cur.close()
        conn.close()