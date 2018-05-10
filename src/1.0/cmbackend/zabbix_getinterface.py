#!/usr/bin/env python
#-*-coding:utf-8-*-


# 导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request, urlopen, URLError, HTTPError
from auth import zabbix_header,zabbix_user,zabbix_url,zabbix_pass,auth_code,auth_data
import MySQLdb
json_data = {
                "method": "hostinterface.get",
                "params": {
                    "output": "extend",
                },

                "jsonrpc": "2.0",
                "auth": auth_code,
                "id": 1
            }


if len(auth_code) == 0:
        sys.exit(1)
if len(auth_code) != 0:
        get_host_data = json.dumps(json_data)

        #create request object
        request = urllib2.Request(zabbix_url,get_host_data)
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
                # print response


                #统计几个主机
                long = len(response['result'])
                # print long
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
                sql1 = "DELETE FROM main_cinterface "
                cur.execute(sql1)
                conn.commit()
                for interface in response['result']:
                    get_data =[ interface['interfaceid'],  interface['hostid'],interface['ip']]
                    # print get_data
                    # 连接数据库mysql
                    cur = conn.cursor()

                    # 插入一条数据
                    sql = "insert into main_cinterface values(%s,%s,%s) "
                    try:
                        cur.execute(sql, get_data)  # 执行sql语句
                        conn.commit()
                        print "insert success!"
                    except:
                        print "Error: unable to fetch data"
                cur.close()
                conn.close()
