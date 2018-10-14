#!/usr/bin/python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
import sys
import MySQLdb
import json
mail_host = 'smtp.163.com'
mail_user = 'xijialin321@163.com'
mail_pass = 'xjl123456789'
mail_postfix = '163.com'
def send_mail(to_list,subject,content):
    me = "CMC 监控告警平台"+"<"+mail_user+"@"+mail_postfix+">"
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
    send_mail(h1, h2, h3)  # 接受来自zabbix的参数
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
    get_data=[h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14]
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
    sql = "insert into main_crecovery(recoveryTime,recoveryDate,actionName,triggerStatus,itemValues,triggerSeverity,eventId,eventStatus,eventValue,originaleventID,triggerName) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    try:
                cur.execute(sql, get_data)  # 执行sql语句
                cur.close()
                conn.commit()
                conn.close()
                print "insert success!"
    except:
                print "Error: unable to fetch data"