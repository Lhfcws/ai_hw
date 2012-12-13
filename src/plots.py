#! /usr/bin/python
#-*- coding:utf-8 -*-
# author: Lhfcws Wu [ 10389393 Wenjie Wu ]
# Copyright: Lhfcws
# Version: 1.0

from uglysina import Main
from uglysina import trend
import MySQLdb
from dbconf import dbconfig
from datetime import date

def model(crs):
	ls = []
	crs.execute("select * from request")
	ls = crs.fetchall()
	return ls[0]
#	crs.execute("delete from request limit 1")

def main():
	# connect MYSQL
	res = dbconfig()
	conn = MySQLdb.connect(host=res[0], user=res[1], passwd=res[2])
	conn.select_db('ai_hw')
	cursor = conn.cursor()
	cursor.execute("set names 'utf8'")
	# init 
	M = Main("ai2012_go@126.com", "aiai2012")
	M.start()
	M.login()

	l = model(cursor)
	conn.commit()

	M.keyword(l[1])

	# get Plots
	#plot = trend(cursor, M, date(ls[1], ls[2], ls[3]), date(ls[4], ls[5], ls[6]))
	plot = trend(cursor, M, date(2012,9,1), date(2012,9,30))
	conn.commit()

	cursor.close()
	conn.close()
