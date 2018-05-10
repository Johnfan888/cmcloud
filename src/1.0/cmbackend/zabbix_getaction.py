#!/usr/bin/env python
# -*- encoding: utf8 -*-

# 导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code
import MySQLdb

# url and url header


json_data = {
    "jsonrpc": "2.0",
    "method": "action.get",
    "params": {

        # "output": ["actionids","hostids","name"],
          "output": "extend",
        # "hostids": "10084",
        # "search": {
        #      "key_": "system"
        #  },
        #  "sortfield": "name"
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

        # print "Number Of Actions: ", len(response['result'])
        # 连接数据库
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='cmc',
            charset='utf8',
        )
        cur = conn.cursor()
        # 清空数据库
        sql1 = "DELETE FROM main_caction "
        cur.execute(sql1)
        conn.commit()
        for action in response['result']:
            get_data=[action['actionid'],action['name'],action['status']]
            # print get_data
            # 连接数据库mysql
            cur = conn.cursor()

            # 插入一条数据
            sql2 = "insert into main_caction values(%s,%s,%s) "
            try:
                cur.execute(sql2, get_data)  # 执行sql语句

                conn.commit()

                print "insert success!"
            except:
                print "Error: unable to fetch data"
        cur.close()
        conn.close()