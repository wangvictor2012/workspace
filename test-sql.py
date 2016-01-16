# -*- coding: utf-8 -*-
import pymssql
import sys
import chardet

def encodechinese(chinese):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    return chinese.encode('utf-8')

#创建一个数据库连接，host是服务器的ip地址，如果是本机可以用"."，user是访问用户名，password是密码，database是数据库名，比ADO的连接似乎简单一些
conn=pymssql.connect(host="kingdee-5",user="sa",password="1Yuan$!!", database="AIS20140820155611", port='1433',charset="UTF8")
#创建游标对象，相当于ADO的记录集
'''
SQLSERVER_HOST = 'localhost'
SQLSERVER_PORT = '1433'
SQLSERVER_USER = 'sa'
SQLSERVER_PASS = 'wang123456'
SQLSERVER_DB = 'test'
conn=pymssql.connect(host=SQLSERVER_HOST,user=SQLSERVER_USER, password=SQLSERVER_PASS, database=SQLSERVER_DB, port=SQLSERVER_PORT, charset="UTF-8")
'''
f = open('D:/test.txt','w')
Material_serial_Index = "var Material_serial_Index = '"    
cou=conn.cursor()
#sql="select * from dbo.t_ICItemCore where FNumber like '%%s%'" %(str('02.03.006\r'))
sql="select * from dbo.t_ICItemCore" 
#执行命令
cou.execute(sql)
#取出所有记录，返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
for x in cou.fetchall():
    Material_serial_Index = Material_serial_Index + " " + str(x[6])
    #print chardet.detect(x[1])
    
Material_serial_Index += "';"
f.write(Material_serial_Index)
f.close()
conn.close()
