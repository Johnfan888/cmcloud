# -*- encoding: utf8 -*-
from auth import zabbix_header,zabbix_pass,zabbix_url,zabbix_user,auth_code,MySQLport,MySQLuser,MySQLpasswd
import MySQLdb
f = open("/usr/CMC/zabbix_api/trigger_condition.txt", "r")
s=f.readlines()
triggerName= s[0].strip("\n")#去掉换行符
condition= s[1]
# print triggerName
# print condition
#-----替换数据表-------
conn = MySQLdb.connect(
            host='localhost',
            port=MySQLport,
            user=MySQLuser,
            passwd=MySQLpasswd,
            db='cmc',
            charset='utf8',
        )
cur = conn.cursor()
sql = "select triggerId from main_ctrigger where triggerName=%s "
cur.execute(sql,[triggerName])
triggerId = cur.fetchone()#取到eventId,
sql1 = "update main_ctrigger set `condition`=%s where triggerId=%s "
cur.execute(sql1,[condition ,triggerId])
conn.commit()

cur.close()
conn.close()
