#!/usr/bin/env python
# -*- encoding: utf8 -*-

# 导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request, urlopen, URLError, HTTPError
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code,MySQLport,MySQLuser,MySQLpasswd
import MySQLdb

json_data = {
    "jsonrpc": "2.0",
    "method": "trigger.get",
    "params": {
        # "hostids": "10177",
        # "triggerids":14504,
        "output": "extend",
        "selectFunctions": "extend"
        # "output": [
        # "triggerid",
        # "description",
        # "priority",
        # "status"
        # ],
         # "hostids":"10084",
         # "itemids":"24559",
        # "filter": {
        #     "value": 1
        # },
        #  "sortfield": "priority",
        #  "sortorder": "DESC"
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
        # # 将所有的主机jiankong信息显示出来
        # print "Number Of Triggers: ", len(response['result'])
        # print response
        # # 连接数据库
        conn = MySQLdb.connect(
            host='localhost',
            port=MySQLport,
            user=MySQLuser,
            passwd=MySQLpasswd,
            db='cmc',
            charset='utf8',
        )
        # cur = conn.cursor()
        # 清空数据库
        # sql1 = "DELETE FROM main_ctrigger "
        # cur.execute(sql1)
        # conn.commit()
        triggerID=[]#将所有id汇总
        for trigger in response['result']:
            triggerID.append(trigger['triggerid'])#将所有id汇总
            for item in trigger["functions"]:
                condition=[item['itemid'],item['triggerid'],item['function'],trigger['expression']]
                condition = ','.join(condition)#数据库中没有
                # condition = str(condition)#数据库中带[]
                # print condition
                get_data =[trigger['triggerid'],trigger['description'], trigger['value'],trigger['priority'],item[ "itemid"],
                            trigger['comments'],condition]
                get_data1 = [trigger['description'], trigger['value'], trigger['priority'],item["itemid"],trigger['comments']]
                # print get_data
                # 连接数据库mysql
                cur = conn.cursor()
                # 插入一条数据
                sql = "insert into main_ctrigger values(%s,%s,%s,%s,%s,%s,%s) "
                # sql = "insert into main_ctrigger(triggerId,triggerName,triggerValue,triggerPriority,itemId,triggerDescription) values(%s,%s,%s,%s,%s,%s) "
                sql1 = "updata main_ctrigger set triggerName=%s,triggerValue=%s,triggerPriority=%s,itemId=%s,triggerDescription=%s WHERER triggerId ="+trigger['triggerid']
                try:
                    cur.execute(sql, get_data)  # 新建
                    conn.commit()
                    cur.execute(sql1, get_data1)  # 更新
                    conn.commit()
                    # cur.execute(sql2, get_data1)  # 删除zabbix没有的
                    # conn.commit()
                    # print "insert success!"
                except:
                    1
                    # print "Error: unable to fetch data"
                    # print get_data
        # triggerID=tuple(triggerID)

        triggerID = ",".join(triggerID)#输出类型为unicode
        triggerID = triggerID.encode('unicode-escape').decode('string_escape')
        # print triggerID,type(triggerID)
        sql2 = "delete  from main_ctrigger where triggerId not in (%s)" %(triggerID)
        cur.execute(sql2)  # 删除zabbix没有的
        conn.commit()
        # tt = cur.fetchall()  # 取查询出来的节点信息
        # print tt
        cur.close()
        conn.close()