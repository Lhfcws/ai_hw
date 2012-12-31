#encoding=utf-8

def getStopwordList():
	f = open("/home/lhfcws/coding/projects/web/ai_hw/src/bayes/stopword.txt",'r')
	lines = f.readlines()
	f.close()
	f = open("/home/lhfcws/coding/projects/web/ai_hw/src/bayes/user.dict",'r')
	songs = f.readlines()
	songs = [s.split()[0] for s in songs]
	f.close()
	songs = set(songs)
	lines = set(lines)

	return lines.difference(songs)
