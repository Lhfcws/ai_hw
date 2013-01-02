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
import re

##################
# Encode Chinese characters into sina url encodings.
def sina_urlencode(s):
	reprStr = repr(s).replace(r'\x', '%25')
	return reprStr[1:-1]

# UNUSED
#def sina_urldecode(s):
#	reprStr = repr(s).replace('%25', '%')
#	reprStr = urllib.unquote(reprStr)
#	return reprStr[1:-1]

##################
# Abstract class
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
		elist = self.br.find_by_css('.W_input')
		if not elist.is_empty():
			elist.first.fill(self.user)
			(elist[1]).fill(self.pwd)
			self.br.find_by_css(".W_checkbox").first.click()
			self.br.find_by_css(".W_btn_g").first.click()
		else:
			self.br.find_by_css(".name").first.fill(self.user)
			self.br.find_by_css(".pass").first.fill(self.pwd)
			self.br.find_by_css(".W_checkbox").first.click()
			self.br.find_by_css(".W_btn_d").first.click()


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
	# Start a browser
	def start(self):
		self.br = Browser()

	# Clear the stoppage
	def clear(self):
		self.warn = False
		self.stoppage = 1

	# Quit the browser
	def quit(self):
		self.clear()
		self.br.quit()

	# Restart a browser
	def restart(self):
		self.quit()
		self.start()

	# Final config to generate the url
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

	# Login
	def login(self):
		Lg = Login(self.br, self.user, self.pwd)
		Lg.login()
		time.sleep(2)
	
	# Logout
	def logout(self):
		Lg = Logout(self.br)
		Lg.logout()
	
	# Return the html source for pyquery
	def html(self):
		return self.br.html

	# Set keyword
	def keyword(self, key):
		self.key = sina_urlencode(key)
		self.orikey = key

	# Get keyword
	def getKeyword(self):
		return self.orikey

	# Set time period
	def period(self, st, ed):
		self.st, self.ed = st, ed

	# Visit the page on a given number
	def visit(self, num):
		href = self.url + str(num)
		self.br.visit(href)
		self.D = pq(self.br.html)
	#	self.delay()
			
	# Flip to the next page
	def flip(self):
		self.visit(self.stoppage)
		self.stoppage += 1
		
	# Get the total statistics of the search result.
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

	# Get the user id list of the current page
	def getUsers(self):
		self.D = pq(self.br.html)
		pre = re.compile("http[0-9|:|/| |.|a-z|A-Z]*")
		aa = self.D(".content > p > em").siblings("a")
		userls = []
		weibols = []
		for i in range(len(aa)):
			if aa.eq(i).attr("suda-data"):
				p = aa.eq(i).attr("suda-data").split(':')
				userls.append(p[1])
				w = aa.eq(i).siblings("em").html()
				ww = re.sub('</?\w+[^>]*>',"",w)
				ww = re.sub(pre, "", ww)
				weibols.append(ww.strip())
		
		return [userls,weibols]
			
	# Judge if we meet a captcha.
	def captcha(self):
		self.D = pq(self.br.html)
		cap = self.D(".code_img")
		return len(cap) > 0

	# Save current stoppage
	def save(self):
		f = open("stoppage","w")
		f.write(str(self.stoppage))
		f.close()
	
	# Load stoppage which was saved.
	def load(self):
		f = open("stoppage","r")
		p = f.readline()
		self.stoppage = int(p)
		f.close()

	# Judge if there's no results any more.
	def end(self):
		self.D = pq(self.br.html)
		noresult = self.D(".search_noresult")
		if not noresult:
			return False
		return True

############## END

############## Functions
# Judge if the given year is run year
def run(year):
	if year%400 == 0:
	 	return True
	if year%100 != 0 and year%4 == 0:
		return True
	return False

# Get the next date of a given date.
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

# Get the data to build the lines graph.
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
		
		value=[temp, dt, M.getKeyword()]
		csr.execute("insert into plots value(%s, %s, %s)", value)

		stat.append(temp)

		if now.isoformat() == ed.isoformat():
			break
		now = tomorrow(now)

	M.quit()
	return stat

