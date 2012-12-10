#! /usr/bin/python
#-*- coding:utf-8 -*-
# author: Lhfcws Wu [ 10389393 Wenjie Wu ]
# Copyright: Lhfcws
# Version: 1.0
#encoding=utf-8 
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8") 
import MySQLdb
from dbconf import dbconfig

def finish(cursor, M):
	# connect MYSQL
	#res = dbconfig()
	#conn = MySQLdb.connect(host=res[0], user=res[1], passwd=res[2])
	#conn.select_db('ai_hw')
	#cursor = conn.cursor()
	#cursor.execute("set names 'utf8'")
	
	
	#conn.commit()
	#cursor.close()
	#conn.close()
