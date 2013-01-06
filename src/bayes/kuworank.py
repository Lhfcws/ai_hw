#! /usr/bin/env python
#encoding=utf-8

from pyquery import PyQuery as pq
import urllib
import re
import os
path = os.path.dirname(__file__)

# Encode chars to sinalurl mode
def sina_urlencode(s):
	reprStr = repr(s).replace(r'\x', '%25')
	reprStr = repr(reprStr).replace(' ', '%2520')
	return reprStr[1:-1]

def initUrl(keyword):
	keyword = urllib.quote(keyword)
	return "http://www.kuwo.cn/mingxing/" + keyword

# Judge if value is in a list
def exist(lis, name):
	for l in lis:
		if l == name:
			return True

	return False

# Strip the song name
def strip(songname):
	s = list(songname)
	l = [['(', ')'], ['（','）'], ['[', ']']]
	for kh in l:
		try:
			if exist(s, kh[0]):
				s = s[0:s.index(kh[0])]
		except:
			continue
	
	return ''.join(s)

# For debug
def printd(dic):
	for item in dic.items():
		print item[0], item[1]

# In case of duplication
def insert_once(name, value, dic):
	bo = not dic.has_key(name)
	if bo:
		dic[name] = int(value)
		f = open(path+"/user.dict",'r')
		lines = f.readlines()
		lines = [(lp.split(' '))[0] for lp in lines]
		f.close()
		name = (name.split(' '))[0]
		name = name.encode('utf-8')
		if not exist(lines, name):
			f = open(path+"/user.dict",'a')
			f.write(name +" 3\n")
			f.close()
	else:
	 	dic[name] += int(value)

	return dic

# For debug
def writeFile(keyword, inv):
	f = open("inv.js",'a')
	f.write(',\n')
	f.write("{ name: '"+keyword+"', data: [")
	
	for item in inv:
		f.write(str(item[0]))
		if item != inv[len(inv)-1]:
			f.write(', ')

	f.write(' ]}')
	f.close()


# Get the rank of songs in sina weibo
def getWeiboRank(keyword, res):
	src = "http://s.weibo.com/weibo/"
	suff= "&scope=ori"
	dd = dict()
	cnt = 1
	for r in res:
		if cnt>=10:
			break
		print cnt,r
		key = sina_urlencode(keyword) + '%2520' + sina_urlencode(r.encode("utf-8"))
		print src+key+suff
		D = pq(url=src+key+suff)
		text = D.html()
		pn = re.compile("noresult_tit")	
		p = re.compile("\\\\u627e\\\\u5230 [,|0-9]*")
		non = pn.search(text)
		if non != None:
			continue
		st = p.search(text)
		st = st.group()
		print st
		lis = st.split()
		if len(lis) == 1:
			continue
		print lis
		lis = lis[1].split(',')

		stat = ""
		for l in lis:
			stat = stat + l
		stat = int(stat)
		dd[stat] = r
		cnt += 1
	
	lis = dd.items()
	lis = sorted(lis, reverse=True)
	return lis
		

def main(keyword):
	D = pq(url=initUrl(keyword))
	names = D(".songName > a")
	songers = D(".songName > a").parent().siblings(".songer > a")
	vals = D(".rq > span")
	cnt = 0
	dic = dict()

	for i in range(len(names)):
		item = names[i]
	
		name = strip(item.text).strip()
		dic = insert_once(name, int(vals[cnt].text), dic)
		cnt += 1

#	lis = dic.items()
#	inv = [[v[1], v[0]] for v in lis]
#	inv = sorted(inv, reverse=True)
	
#	res = [v[1] for v in inv]
	res = dic.keys()
	res = getWeiboRank(keyword, res)
	
	writeFile(keyword, res)

	return [r[1] for r in res]
