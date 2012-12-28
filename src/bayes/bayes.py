#! /usr/bin/python2
#encoding=utf-8

# P(H|T) = P(T|H)*P(H) / (P(T|H)*P(H) + P(T|M)*P(M))								Bayesian Law
# P(H|t1 ,t2, t3……tn) = (P1*P2*……PN) / [P1*P2*……PN + (1-P1)*(1-P2)*……(1-PN)] 		Compound Probability

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import jieba
import math
import xmlOperation
import kuworank
from editdict import editDict
from stopword import getStopwordList
import dbconf

hitsFile = "train_result/hits_music.txt"
missFile = "train_result/miss_music.txt"
srcFile = "train.txt"
#stopword = getStopwordList()

def readFile(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	f.close()
	return lines

def writeFile(lis, filename):
	f = open(filename, 'w')
	for l in lis:
		f.write(str(l))
	f.close()

def segword(sentence):
	jieba.load_userdict("/home/lhfcws/coding/projects/web/ai_hw/src/bayes/user.dict")
	seg_list = jieba.cut(sentence, cut_all=False)
	s = ','.join(seg_list)
	s = s.split(',')
	'''
	ans = []
	for ss in s:
		if not (ss in stopword):
			ans.append(ss)
	return ans
	'''
	return s

def train_frontend():
	lines = readFile(srcFile)
	hitlist = []
	misslist = []

	for line in lines:
		print "=============================================================="
		print "Weibo: \n" + line
		print ""
		yn = raw_input("Is it about his music? (y/n/q): ")
		if yn == "q":
			break

		if yn == "y":
			hitlist.append(line)
		else:
			misslist.append(line)

	writeFile(hitlist, hitsFile)	
	writeFile(misslist, missFile)	
	return [len(hitlist), len(misslist)]

def getTokensProbability(hsum, msum):
	hitlist = readFile(hitsFile)
	htoken = dict()
	for hit in hitlist:
		hl = segword(hit)
		for word in hl:
			if htoken.has_key(word):
				htoken[word] += 1
			else:
				htoken[word] = 0
	
	P_TH = dict()

	for key in htoken:
		P_TH[key] = float(htoken[key]) / float(hsum)
	

	misslist = readFile(missFile)
	mtoken = dict()
	for mis in misslist:
		hl = segword(mis)
		for word in hl:
			if mtoken.has_key(word):
				mtoken[word] += 1
			else:
				mtoken[word] = 0
	
	P_TM = dict()

	for key in mtoken:
		P_TM[key] = float(mtoken[key]) / float(msum)


	return [P_TH, P_TM]

# Bayesian Probability 
def getP_HT(P_H, P_M, P_TH, P_TM):
	return float(P_TH * P_H) / float( P_TH*P_H + P_TM*P_M )

def getP_HT_Table(hsum, msum, P_TH, P_TM):
	P_H = float(hsum) / float(hsum + msum)
	P_M = float(msum) / float(hsum + msum)
	
	P_HT = dict()
	for token in P_TH:
		# Laplace Correction
		if not(P_TH.has_key(token)) or P_TH[token] == 0:
			P_TH[token] = 0.5
		if not(P_TM.has_key(token)) or P_TM[token] == 0:
			P_TM[token] = 0.5

		#print P_H,P_M, P_TH[token], P_TM[token]
		P_HT[token] = getP_HT(P_H, P_M, P_TH[token], P_TM[token])
		
	return P_HT


# Bayesian Probability 
def getP_MT(P_H, P_M, P_TH, P_TM):
	return float(P_TM * P_M) / float( P_TH*P_H + P_TM*P_M )

def getP_MT_Table(hsum, msum, P_TH, P_TM):
	P_H = float(hsum) / float(hsum + msum)
	P_M = float(msum) / float(hsum + msum)
	
	P_MT = dict()
	for token in P_TM:
		# Laplace Correction
		if not(P_TH.has_key(token)) or P_TH[token] == 0:
			P_TH[token] = 0.5
		if not(P_TM.has_key(token)) or P_TM[token] == 0:
			P_TM[token] = 0.5

		P_MT[token] = getP_MT(P_H, P_M, P_TH[token], P_TM[token])
		
	return P_MT

def hitProbability(tokens, P_HT):
	res = 0
	s1 = 1
	s2 = 1
	for token in tokens:
		if not(P_HT.has_key(token)) or P_HT[token] == 0:
			P_HT[token] = 0.5
		if P_HT[token] < 0:
			continue
		s1 *= float(P_HT[token])
		s2 *= float(1 - P_HT[token])

	return s1 / ( s1 + s2 )

def missProbability(tokens, P_MT):
	res = 0
	s1 = 1
	s2 = 1
	for token in tokens:
		if not(P_MT.has_key(token)) or P_MT[token] == 0:
			P_MT[token] = 0.5
		if P_MT[token] < 0:
			continue
		s1 *= float(P_MT[token])
		s2 *= float(1 - P_MT[token])

	return s1 / ( s1 + s2 )

def getSum():
	l1 = readFile("hits_music.txt")
	l2 = readFile("miss_music.txt")
	return [len(l1), len(l2)]

def init(keyword, songlist):
	# training
	#hsum, msum = train_frontend()
	hsum, msum = getSum()
	P_H = float(hsum) / float(hsum + msum)
	P_M = float(msum) / float(hsum + msum)

	# Bayesian Calculate
	P_TH, P_TM = getTokensProbability(hsum, msum)
	P_HT = getP_HT_Table(hsum, msum, P_TH, P_TM)
	P_MT = getP_MT_Table(hsum, msum, P_TH, P_TM)
	P_HT[keyword] = -2;
	P_MT[keyword] = -2;

	for song in songlist:
		if not P_HT.has_key(song):
			P_HT[song] = 0.5
		if not P_MT.has_key(song):
			P_MT[song] = 0.5

		P_HT[song] = math.sqrt(100*P_HT[song]) / 10.0
		P_MT[song] = (10*P_MT[song])**2 / 100.0

	return [P_HT, P_MT, P_H, P_M, hsum, msum]

# ================MAIN=====================
def main():
	keyword = "梁博"
	songlist = kuworank.main(keyword)
	editDict(songlist)

	P_HT, P_MT, P_H, P_M, hsum, msum = init(keyword, songlist)
	
	xmlOperation.create_xml(P_HT, "music_HT_dict.xml");
	xmlOperation.create_xml({'hits':P_H}, "music_H_dict.xml");
	xmlOperation.create_xml(P_MT, "music_MT_dict.xml");
	xmlOperation.create_xml({'miss':P_M}, "music_M_dict.xml");
	
	'''
	con = dbconf.dbconfig()
	conn = MySQLdb.connect(host=con[0], user=con[1], passwd=con[2])
	conn.select_db("ai_hw")
	cursor = conn.cursor()
	P_HT = get_xml_data("music_HT_dict.xml")
	P_H = get_xml_data("music_H_dict.xml")
	P_MT = get_xml_data("music_MT_dict.xml")
	P_M = get_xml_data("music_M_dict.xml")
	'''
	'''
	lines = readFile("testFile.txt")
	resList = []
	hl = []
	ml = []
	for line in lines:
		tokens = segword(line)
		hitP = hitProbability(tokens, P_HT) * P_H
		missP = missProbability(tokens, P_MT) * P_M
		print hitP, missP
		if missP < hitP:
			resList.append(line)
			hl.append(line)
		else:
			ml.append(line)

	writeFile([str(len(lines))+"\n", len(resList)], "result.txt")
	writeFile(hl, "result_hits.txt")
	writeFile(ml, "result_miss.txt")
	'''
	'''
	cursor.execute("insert into `music_love` values('"+len(lines)"','"+len(resList)+"')")
	cursor.close()
	conn.close()
	'''

if __name__ == "__main__":
	main()
