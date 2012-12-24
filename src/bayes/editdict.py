#coding:utf-8
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 

def editDict(ls):
	f = open("user.dict", 'a')
	for l in ls:
		l = l.split(' ')
		f.write(l[0] +" 3\n")
	f.close()

