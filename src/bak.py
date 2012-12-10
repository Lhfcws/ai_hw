#! /usr/bin/python
#-*- coding:utf-8 -*-
# author: Lhfcws Wu [ 10389393 Wenjie Wu ]
# Copyright: Lhfcws
# Version: 1.0

from pyquery import PyQuery as pq
from splinter import Browser
import time
from datetime import date
import urllib
import json
import MySQLdb

##################
def sina_urlencode(s):
	reprStr = repr(s).replace(r'\x', '%25')
	return reprStr[1:-1]

##################
class AutoBrowserAction:
	def sleep(self, num):
		print "Waiting "+str(num)+" seconds...."
		time.sleep(num)

	def delay(self):
		num = 3
		url = self.br.url

		while True:
			print "Waiting "+str(num)+" seconds for redirecting...."
			time.sleep(num)
			self.current_url = self.br.url
			if url == self.br.url:
				break

			url = self.br.url
			num = num * 0.8
			if num < 0.5:
				self.warn = True
				return False

	def browser(self):
		return self.br

############
# Auto log in http://www.weibo.com
#
class Login(AutoBrowserAction):
	def __init__(self, browser, username, password):
		self.user, self.pwd = username, password
		self.weibo_index = "http://www.weibo.com"
		self.br = browser
		self.br.visit(self.weibo_index)
		htmlclass = {}
		htmlclass['user'] = 'name'
		htmlclass['pwd'] = 'pass'

	def set(self, username, password):
		self.user, self.pwd = username, password
	
	def login(self):
		self.br.find_by_css('.name').first.fill(self.user)
		self.br.find_by_css('.pass').first.fill(self.pwd)
		self.br.find_by_css(".W_checkbox").click()
		self.br.find_by_css(".W_btn_d").click()

		# Wait for the browser redirecting.

############## END

##############
# Auto log out and return to http://www.weibo.com
#
class Logout(AutoBrowserAction):
	def __init__(self, browser):
		self.br = browser
	
	def logout(self):
		self.weibo_logout = "http://weibo.com/logout.php?backurl=/"
		self.br.visit(self.weibo_logout)
		self.weibo_index = "http://www.weibo.com"
		self.br.visit(self.weibo_index)
		
############## END

##############
# Some preference for search.
#
#class SearchPreference(AutoBrowserAction);
#	def __init__(self, browser):
#		self.br = browser
#
#	def period(self, starttime, endtime):
#		self.st, self.et = starttime, endtime
#		self.br.find_by_css(".tab_all>a").last.click()
#
#		el = self.br.find_by_class("W_inputStp")
#		el[-2].fill(self.st)
#		el[-1].fill(self.et)
#		self.sleep(1)
#		
#		return self.br
#
#	def original(self):
#		self.br.visit(self.br.url+"&scope=ori")
#		self.delay()
#		return self.br
#
#
#	def flip(self, num):
#		self.br.visit(self.br.url+"&page="+str(num))
#		self.delay()
#		return self
#
#	def submitPrf(self):
#		self.br.find_by_class("W_btn_cb").first.click()
#		self.delay()

############## END


##############
# Auto search a specific keyword.
#
#class InitSearch(AutoBrowserAction):
#	def __init__(self,browser, keyword):
#		self.key = keyword
#		self.br = browser
#	
#	def init_search(self):
#		self.br.find_by_class("input_W_no_outline").first.fill(self.keyword)
#		self.br.find_by_css(".search > a").click()
#		self.delay()
#
#		return self.br
	
############## END

############## MAIN
class Main(AutoBrowserAction):
	def __init__(self, username, password):
		self.user, self.pwd = username, password
		self.clear()

	def start(self):
		self.br = Browser()

	
	def clear(self):
		self.warn = False
		self.stoppage = 1

	def quit(self):
		self.clear()
		self.br.quit()

	def restart(self):
		self.quit()
		self.start()

	def config(self):
		self.url = "http://s.weibo.com/weibo/"
		#keyword
		self.url += self.key
		# period
		self.url += "&timescope=custom:"+self.st+':'+self.ed
		# original
		self.url += "&scope=ori"
		#init page
		self.url += "&page="

	def login(self):
		Lg = Login(self.br, self.user, self.pwd)
		Lg.login()
	
	def logout(self):
		Lg = Logout(self.br)
		Lg.logout()
	
	def html(self):
		return self.br.html

	def keyword(self, key):
		self.key = sina_urlencode(key)

	def period(self, st, ed):
		self.st, self.ed = st, ed

	def visit(self, num):
		href = self.url + str(num)
		self.br.visit(href)
		self.D = pq(self.br.html)
	#	self.delay()
			
	def flip(self):
		self.visit(self.stoppage)
		self.stoppage += 1
		
	def sumstat(self):
		text = self.D(".topcon_num > .W_textc")
		if not text:
			self.br.reload()
			self.D = pq(self.br.html)
			text = self.D(".topcon_num > .W_textc")
		text = text.html().split()
		stat = text[1].split(',')
		r = ""
		for item in stat:
			r += item

		return int(r)

	def getUsers(self):
		self.D = pq(self.br.html)
		aa = self.D(".content > p > em").siblings("a")
		userls = []
		for i in range(len(aa)):
			if aa.eq(i).attr("suda-data"):
				p = aa.eq(i).attr("suda-data").split(':')
				userls.append(p[1])
		
		return userls
			
	def captcha(self):
		self.D = pq(self.br.html)
		cap = self.D(".code_img")
		return len(cap) > 0

	def save(self):
		f = open("stoppage","w")
		f.write(self.stoppage)
		f.close()
	
	def load(self):
		f = open("stoppage","r")
		p = f.readline()
		self.stoppage = int(p)
		f.close()

	def end(self):
		self.D = pq(self.br.html)
		noresult = self.D(".search_noresult")
		if not noresult:
			return True
		return False

############## END

############## Functions
def run(year):
	if year%400 == 0:
	 	return True
	if year%100 != 0 and year%4 == 0:
		return True
	return False

def tomorrow(dat):
	m = [0,31,28,31,30,31,30,31,31,30,31,30,31]
	day = dat.day
	mon = dat.month
	year = dat.year
	if run(year):
		m[2] += 1
	
	day += 1
	if day > m[mon]:
		day = 1
		mon += 1
	if mon > 12:
		year += 1
		mon = 1
	
	dt = dat.replace(year, mon, day)
	return dt

def trend(csr, M, st, ed):
	stat = []
	now = st
	while True:
		dt = now.isoformat()

		M.period(dt, dt)
		M.config()
		M.visit(1)
		if M.captcha():
			M.save()
			M.logout()
			M.restart()
			M.login()
			M.load()
			M.visit(1)

		temp = M.sumstat()
		
		value=[temp, dt]
		csr.execute("insert into plots value(%s, %s)", value)

		stat.append(temp)

		if now.isoformat() == ed.isoformat():
			break
		now = tomorrow(now)

	M.quit()
	return stat

def main():
	# connect MYSQL
	conn = MySQLdb.connect(host="localhost", user="root", passwd='')
	conn.select_db('ai')
	cursor = conn.cursor()

	# Init
	M = Main("lhfcws@163.com", "weibolhfcws")
	M.start()
	M.login()
	# configure
	M.keyword("梁博")
	#M.original()
	# get Plots
	#plot = trend(cursor, M, date(2012, 9, 1), date(2012, 9, 30))
	#conn.commit()
#	print plot
	# get Users
	M.clear()
	M.period("2012-09-27", "2012-09-27")
	M.config()

	while True:
		if M.end():
			break
		if M.captcha():
			M.save()
			M.logout()
			M.restart()
			M.login()
			M.load()

		stat = M.getUsers()	
		
		for item in stat:
			cursor.execute("insert into users value(%s)", item)

		M.flip()

	conn.commit()
	cursor.close()
	conn.close()
############################################################
if __name__ == '__main__':
	main()
