#! /usr/bin/python
#-*- coding:utf-8 -*-
# author: Lhfcws Wu [ 10389393 Wenjie Wu ]
# Copyright: Lhfcws
# Version: 1.0
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from uglysina import Main
#from finish import finish
import MySQLdb
import re
from dbconf import dbconfig
from datetime import date

def model(crs):
	crs.execute("select * from request ORDER BY id desc limit 1")
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
	p = re.compile("http[0-9|:|/| |.|a-z|A-Z]*")
	# connect MYSQL
	res = dbconfig()
	conn = MySQLdb.connect(host=res[0], user=res[1], passwd=res[2])
	conn.select_db('ai_hw')
	cursor = conn.cursor()
	cursor.execute("set names 'utf8'")
	# Init
	M = Main("ai2012_go@126.com", "aiai2012")
	M.start()
	M.login()
	M.clear()

	# Test day
	M.period("2012-09-20", "2012-09-20")

	r = model(cursor)
	key = r[1]
	M.keyword(r[1])
	M.config()

	stop = 0
	while True:
		if stop == 10:
			break
		stop += 1
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
		for i in range(len(stat[0])):
			value = [stat[0][i], M.getKeyword(), stat[1][i].encode("utf-8")]
			value[2] = re.sub(p,"",value[2])
			cursor.execute("insert into users value(%s, %s, %s)", value)

		# Flip to next page.
		M.flip()

		conn.commit()

	M.quit()
	value = [M.getKeyword()]
	#cursor.execute("delete from request where keyword='%s'",value);
	#cursor.execute("insert into finish value(%s)", value);
	#conn.commit()
	cursor.close()
	conn.close()
