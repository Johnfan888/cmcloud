#!/usr/bin/ python
# -*- encoding: utf8 -*-
import string
import MySQLdb
import sys
import re
import yaml
#sys.path.append('/usr/CMC/zabbix_api/')
#import auth
#from auth import MySQLport,MySQLuser,MySQLpasswd,MYSQLip
data =sys.argv[1]
# data ="{'cmc_transfer1':{'step':'1','value':'123','time':'312'}}"

data=re.findall(r"'(.+?)'",data)#提取单引号之间的
#print data
actionName = data[0].rstrip(string.digits)#提取actionName
# actionName=actionName.rstrip(string.digits)
print actionName
#取出返回值是第几步
action_step=re.sub('.*?([0-9]*)$',r'1',data[0])
print action_step

conn = MySQLdb.connect(
    host='192.168.1.225',
    port=3306,
    user='root',
    passwd='111111',
    db='cmc',
    charset='utf8',
)
cur = conn.cursor()
'''
#取这个action最新的一条记录
sql1="select eventId,returnValue from main_crecovery_new where actionName=%s order by eventId DESC limit 1;"
#sql1="select eventId,recoveryDate,recoveryTime from main_crecovery_new where actionName=%s and returnValue='[]'"
sql2="update main_crecovery_new set `returnValue`=%s where eventId=%s"
'''

#取这个action最新的一条记录
sql0="select eventId,returnValue from main_crecovery_new where actionName=%s order by eventId DESC limit 1;"
#修改这个返回值
sql1="update main_crecovery_new set `returnValue`=%s where eventId=%s"

cur.execute(sql0,[actionName])
returnValue= cur.fetchone()
eventId=returnValue[0]
returnValue=returnValue[1].encode('utf-8')#取出的记录是unicode格式，转str
returnValue=re.findall(r"{(.+?)}",returnValue)#以{}中的内容划分为list
returnValue_len = len(returnValue)#得到此list的长度，这个长度有几个step就有几个，用作判断
#pritn returnValue_len


if action_step > returnValue_len:
	    fr = open('/etc/zabbix/script/return.yaml', "r")
		recovery = yaml.load(fr)
		fr.close()
		recovery_value = []
		for i in recovery:  # print i
			# --------------取出action中的yaml中的返回值
			if actionName in i and len(actionName) + 1 == len(i):
				return_time = recovery[i]['time']
				aa = {'Step': recovery[i]['step'], 'returnValue': recovery[i]['value'], 'time': return_time}
				recovery_value.append(aa)
				# print sorted(recovery_value)
				recovery_value = sorted(recovery_value)
				# print recovery_value
				j = 0
				n = len(recovery_value) - 1
				while j < n:
					while recovery_value[j]['time'] > recovery_value[j + 1]['time']:
						recovery_value.remove(recovery_value[j + 1])
						n = len(recovery_value) - 1
						if j == n:
							break
					j = j + 1
		recovery_value = str(recovery_value)
		print recovery_value
		print return_time
		# print re.findall(r"{(?)}",data)[3]
		cur.execute(sql1,[recovery_value,eventId])
conn.commit()
cur.close()









'''
cur.execute(sql1,[actionName])
value = cur.fetchone()
eventId = value[0]
print eventId
event_time=value[1]+" "+value[2]
print event_time
if eventId:
    if return_time >= event_time:
		fr = open('/etc/zabbix/script/return.yaml', "r")
		recovery = yaml.load(fr)
		fr.close()
		recovery_value = []
		for i in recovery:  # print i
			# --------------取出action中的yaml中的返回值
			if actionName in i and len(actionName) + 1 == len(i):
				return_time = recovery[i]['time']
				aa = {'Step': recovery[i]['step'], 'returnValue': recovery[i]['value'], 'time': return_time}
				recovery_value.append(aa)
				# print sorted(recovery_value)
				recovery_value = sorted(recovery_value)
				# print recovery_value
				j = 0
				n = len(recovery_value) - 1
				while j < n:
					while recovery_value[j]['time'] > recovery_value[j + 1]['time']:
						recovery_value.remove(recovery_value[j + 1])
						n = len(recovery_value) - 1
						if j == n:
							break
					j = j + 1
		recovery_value = str(recovery_value)
		print recovery_value
		print return_time
		# print re.findall(r"{(?)}",data)[3]
		cur.execute(sql2,[recovery_value,eventId])

conn.commit()
cur.close()
'''