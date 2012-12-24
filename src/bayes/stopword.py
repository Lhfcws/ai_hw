#encoding=utf-8

def getStopwordList():
	f = open("stopword.txt",'r')
	lines = f.readlines()
	f.close()
	return set(lines)
