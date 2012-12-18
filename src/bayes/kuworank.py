#! /usr/bin/env python
#encoding=utf-8

from pyquery import PyQuery as pq
import urllib
import re

def sina_urlencode(s):
	reprStr = repr(s).replace(r'\x', '%25')
	reprStr = repr(reprStr).replace(' ', '%2520')
	return reprStr[1:-1]

def initUrl(keyword):
	keyword = urllib.quote(keyword)
	return "http://www.kuwo.cn/mingxing/" + keyword + "/music.htm"

def exist(lis, name):
	for l in lis:
		if l == name:
			return True

	return False

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

def printd(dic):
	for item in dic.items():
		print item[0], item[1]

def insert_once(name, value, dic):
	bo = not dic.has_key(name)
	if bo:
		dic[name] = int(value)
	else:
	 	dic[name] += int(value)

	return dic

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

def getWeiboRank(keyword, res):
	src = "http://s.weibo.com/weibo/"
	suff= "&scope=ori"
	dd = dict()
	cnt = 0
	for r in res:
		if cnt>10:
			break
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
		lis = st.split()
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
