# -*- encoding: utf8 -*-
import MySQLdb
# get_data = "sss"
# print get_data

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='cmc',
    charset='utf8',
)
cur = conn.cursor()
get_data = ['xxx']
print get_data
# 插入一条数据
sql = "insert into main_chost(hostName) values(%s)"
try:
    cur.execute(sql,get_data)  # 执行sql语句
    cur.close()
    conn.commit()
    conn.close()
    print "insert success!"
except:
    print "Error: unable to fetch data"