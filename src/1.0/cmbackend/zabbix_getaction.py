#!/usr/bin/env python
# -*- encoding: utf8 -*-

# 导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code,auth_code,MySQLport,MySQLuser,MySQLpasswd
import MySQLdb

# url and url header


json_data = {
    "jsonrpc": "2.0",
    "method": "action.get",
    "params": {
        # "output": ["name","esc_period","operations"],
        "output":"extend",
        "selectOperations":"extend",
        # "selectOperations": ["esc_step_from"],
        # "selectRecoveryOperations": "extend",
        # "selectFilter": "operations",
        "selectFilter": "extend",

        "filter": {

             # "actionid": 27,


        }
        # "output": ["actionids","hostids","name"],

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
        print response
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
        sql1 = "DELETE FROM main_caction "
        cur.execute(sql1)
        conn.commit()
        for a1 in response['result']:
            # print a1['filter']['conditions']
            for a2 in a1['filter']['conditions']:
                triggerId = a2['value']  # triggerId!!

            actionId= a1['actionid']#actionId!!
            actionName= a1['name']#actionNmae!!
            status=a1['status']#status!!
            for a3 in a1['operations']:
                period = a3['esc_period']#默然步骤时间！！
            n = []
            m = []
            p = []
            for b1 in a1['operations']:
                 n.append(b1['esc_step_from'])
            # print len(n)#判断有几步
            for j in range(len(n)):
                for kk in [a1['operations'][j]]:
                    # print kk['operationtype']
                    if kk['operationtype'] == "1":#1为发命令的步骤
                        # print kk['opcommand_hst']
                        for jj in kk['opcommand_hst']:
                            # for ll in [kk['opcommand']]:
                            #     command={kk['esc_step_from'],kk['esc_period'],jj['hostid'],kk['opcommand']['command']}
                            #     m1=[]
                            #     m1.append(kk['esc_step_from'])
                            #     m1.append(kk['esc_period'])
                            #     m1.append(jj['hostid'])
                            #     m1.append(kk['opcommand']['command'])
                                # print m1
                                # m1 = ','.join(m1)
                                m1=kk['esc_step_from']+','+kk['esc_period']+','+jj['hostid']+','+kk['opcommand']['command']
                                m1=m1.encode('gb18030')#unicode转str
                                print m1,type(m1)
                                m.append(m1)
                                # m+=m1
                                # m=m.format(my=m1)
                                # print m
                                # print 2121

                                # print command
                    if kk['operationtype'] == "0":#为发邮件的步骤
                        print kk['esc_step_from'],kk['esc_period'],kk['opmessage']
                        for mm in [kk['opmessage']]:
                            message={kk['esc_step_from'],kk['esc_period'],kk['opmessage']['mediatypeid']}
                            print message
                        p1=[]
                        p1.append(kk['esc_step_from'])
                        p1.append(kk['esc_period'])
                        p1.append(kk['opmessage']['mediatypeid'])
                        p1 = ','.join(p1)
                        p.append(p1)
            # print m
            # m=str(m)
            # print m
            # p=str(p)
            m='\''.join(m)

            print type(m)
            get_data=[actionId,actionName,status,period,triggerId,m,p]
            print get_data

            # print get_data
            # print m
            # print m
            # 连接数据库,k['opcommand_hst'],k['opcommand']


            # get_data = [pp['actionid'], pp['name'], pp['status'], m]
                # print get_data
                # 连接数据库mysql
            cur = conn.cursor()

                # 插入一条数据
            sql2 = "insert into main_caction values(%s,%s,%s,%s,%s,%s,%s) "
            try:
                cur.execute(sql2, get_data)  # 执行sql语句

                conn.commit()

                # print "insert success!"
            except:
                print "Error: unable to fetch data"
                # print get_data
        cur.close()
        conn.close()