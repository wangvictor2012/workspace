#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost","root","wang123456","internal" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

code = '21'
searchname = '%'+code+'%'
sql = "SELECT * FROM product_sub_partname \
                    WHERE sub_partname like '" + searchname + "'"

cursor.execute(sql)
# 获取所有记录列表
results = cursor.fetchall()
print results


# 关闭数据库连接
db.close()
