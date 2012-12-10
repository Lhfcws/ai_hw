#! /usr/bin/python
#-*- coding:utf-8 -*-
# author: Lhfcws Wu [ 10389393 Wenjie Wu ]
# Copyright: Lhfcws
# Version: 1.0

from uglysina import Main
#from finish import finish
import MySQLdb
from dbconf import dbconfig
from datetime import date

def model(crs):
	crs.execute("select * from request")
	rids = crs.fetchall()
	result = []
	return rids[0]
'''
	for r in rids:
		rid = r[1]
		ls = []
		crs.execute("select * from user_request where id='%s'", rid)
		ls = crs.fetchall()
		crs.execute("delete from user_request where id='%s'", rid)
		result.append(ls)
'''
def main():

	# connect MYSQL
	res = dbconfig()
	conn = MySQLdb.connect(host=res[0], user=res[1], passwd=res[2])
	conn.select_db('ai_hw')
	cursor = conn.cursor()
	cursor.execute("set names 'utf8'")
	# Init
	M = Main("lhfcws@163.com", "weibolhfcws")
	M.start()
	M.login()
	M.clear()

	# Test day
	M.period("2012-09-27", "2012-09-27")

	r = model(cursor)
	key = r[1]
	M.keyword(r[1])
	M.config()

	while True:
		if M.end():
			break
		# If we meet a captcha we can solve it by login.
		if M.captcha():
			M.save()
			M.logout()
			M.restart()
			M.login()
			M.load()
	
		stat = M.getUsers()	
		
		# Write the user list into database
		for item in stat:
			value = [item, M.getKeyword()]
			cursor.execute("insert into users value(%s, %s)", value)

		# Flip to next page.
		M.flip()

		conn.commit()

	value = [M.getKeyword()]
	#cursor.execute("delete from request where keyword='%s'",value);
	cursor.execute("insert into finish value(%s)", value);
	conn.commit()
	cursor.close()
	conn.close()
