#!/usr/bin/python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
import sys
import MySQLdb
import json
import yaml
import time
mail_host = 'smtp.163.com'
mail_user = 'xijialin321'
mail_pass = 'xjl123456789'
mail_postfix = '163.com'
def send_mail(to_list,subject,content):
    me = "CMC"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        # s.sendmail(me, to_list, msg)
        s.close()
        return True
    except Exception,e:
        print str(e)
        return False
if __name__ == "__main__":
    h1=sys.argv[1]
    h2=sys.argv[2]
    h3=sys.argv[3]
    send_mail(h1, h2, h3)  #发邮件
    s = json.loads(h3)#读取h3
    h4 = s["Event time"]
    h5 = s["Event date"]
    h6 = s["Action name"]
    h7 = s["Trigger status"]
    h8 = s["Item values"]
    h9 = s["Trigger severity"]
    h10 = s["Event ID"]
    h11 = s["Event status"]
    h12 = s["Event value"]
    h13 = s["Original event ID"]
    h14 = s["Trigger name"]
    # get_data=[h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14]
    # print get_data
# 连接数据库mysql
    conn = MySQLdb.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='123456',
                db='cmc',
                charset='utf8',
    )
    cur = conn.cursor()
    # 插入一条数据
    sql1 = "replace into main_crecovery values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql2 = "replace into main_crecovery_new values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql3 = "delete from main_crecovery where eventId=%s"
    sql4 = "replace into main_crecovery_old select * from main_crecovery where eventId=%s"
    try:            
                fr = open('/etc/zabbix/script/return.yaml', "r")
                recovery = yaml.load(fr)
                recovery_value = [] 
                for i in recovery:
                    if '%s' % (h6) in i:   
                        return_time = recovery[i]['time']  
                        aa = {'actionStepName': i, 'returnValue': recovery[i]['value'],'time':return_time}
                        recovery_value.append(aa)
                print recovery_value
                j=0
                n=len(recovery_value)-1
                while  j < n:  
                     while recovery_value[j]['time'] > recovery_value[j+1]['time']:
                         recovery_value.remove(recovery_value[j+1])
                         n=len(recovery_value)-1
                         if j == n :
                             break
                       # print j,recovery_value
                     j=j+1
                print recovery_value 
                recovery_value = str(recovery_value)
                get_data = [h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, recovery_value]
                if h7 == "OK" :
                    cur.execute(sql4,[h10])
                    cur.execute(sql3,[h10])
                    cur.execute(sql2, get_data)  # 执行sql语句
                else:
                    cur.execute(sql1, get_data)  # 执行sql语句
                cur.close()
                conn.commit()
                conn.close()
                print "insert success!"
    except:
                print "Error: unable to fetch data"
