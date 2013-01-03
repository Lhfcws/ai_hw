#encoding=utf-8
import os
path = os.path.dirname(__file__)


def getStopwordList():
	f = open(path+"/stopword.txt",'r')
	lines = f.readlines()
	f.close()
	f = open(path+"/user.dict",'r')
	songs = f.readlines()
	songs = [s.split()[0] for s in songs]
	f.close()
	songs = set(songs)
	lines = set(lines)

	return lines.difference(songs)
