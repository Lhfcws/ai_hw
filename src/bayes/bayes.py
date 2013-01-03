#! /usr/bin/python2
#encoding=utf-8

# P(H|T) = P(T|H)*P(H) / (P(T|H)*P(H) + P(T|M)*P(M))								Bayesian Law
# P(H|t1 ,t2, t3……tn) = (P1*P2*……PN) / [P1*P2*……PN + (1-P1)*(1-P2)*……(1-PN)] 		Compound Probability

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import os
path = os.path.dirname(__file__)
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
stopword = getStopwordList()

def idf(N, C_Ti, N_Ti):
	return math.log(N*float(C_Ti)/N_Ti)

def sortDict(d):
	items = d.items()
	inv = [(v[1],v[0]) for v in items]
	inv.sort(reverse=True)
	return dict(inv)

def getSum():
	l1 = readFile(srcFile)
	l2 = readFile(srcFile)
	return [len(l1), len(l2)]

def abandon(d):
	l = len(d)
	l = math.trunc(l*0.9)
	dd = d 
	k = d.keys()
	for i in range(l+1):
		dd.pop(k[i])
	
	return dd
	
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
	jieba.load_userdict(path+"/user.dict")
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

def merge(d1, d2):
	for d in d2.keys():
		if d1.has_key(d):
			d2[d] += d1[d]
	
	return dict(d1, **d2)

def xorDict(d1, d2):
	for k in d2.keys():
		if d1.has_key(k):
			d1.pop(k)

	return d1

def calcSum(d):
	sm = 0
	for k in d.keys():
		v = int(d[k])
		sm += v
	return sm

def getTokensProbability():
	keyword = readFile("trainKeyword")
	keyword = keyword[0]
	print keyword
	hitlist = readFile(hitsFile)
	htoken = dict()
	for hit in hitlist:
		hl = segword(hit)
		for word in hl:
			if word == keyword:
				continue
			if htoken.has_key(word):
				htoken[word] += 1
			else:
				htoken[word] = 1
	
	P_TH = dict()
	hsum = calcSum(htoken)

	for key in htoken.keys():
		P_TH[key] = float(htoken[key]) / float(hsum)
	

	misslist = readFile(missFile)
	mtoken = dict()
	for mis in misslist:
		ml = segword(mis)
		for word in ml:
			if word == keyword:
				continue
			if mtoken.has_key(word):
				mtoken[word] += 1
			else:
				mtoken[word] = 1
	
	P_TM = dict()
	msum = calcSum(mtoken)

	for key in mtoken.keys():
		P_TM[key] = float(mtoken[key]) / float(msum)

	tokens = merge(htoken, mtoken)
	hidf = {}
	midf = {}
	N = getSum()
	N = N[0] + N[1]
	for ti in tokens.keys():
		if not P_TH.has_key(ti):
			hidf[ti] = 0
		else:
			hidf[ti] = P_TH[ti] * idf(N, htoken[ti], tokens[ti])

		if not P_TM.has_key(ti):
			midf[ti] = 0
		else:
			midf[ti] = P_TM[ti] * idf(N, mtoken[ti], tokens[ti])

	hidf = abandon(sortDict(hidf))
	midf = abandon(sortDict(midf))
	P_TH = xorDict(P_TH, hidf)
	P_TM = xorDict(P_TM, midf)
	htoken = xorDict(htoken, hidf)
	mtoken = xorDict(mtoken, midf)
	tokens = merge(htoken, mtoken)
	
	store = {}
	store['V'] = len(tokens)
	store['sum_htoken'] = calcSum(htoken)
	store['sum_mtoken'] = calcSum(mtoken)

	return [P_TH, P_TM, store]

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
			P_TH[token] = 1.0/hsum
		if not(P_TM.has_key(token)) or P_TM[token] == 0:
			P_TM[token] = 1.0/msum

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
			P_TH[token] = 1.0/hsum
		if not(P_TM.has_key(token)) or P_TM[token] == 0:
			P_TM[token] = 1.0/msum

		P_MT[token] = getP_MT(P_H, P_M, P_TH[token], P_TM[token])
		
	return P_MT

def hitProbability(tokens, P_HT, P_MT, P_H, P_M, store):
	res = 0
	s1 = P_H
	s2 = P_M
	for token in tokens:
		if token in stopword:
			continue
		if not(P_HT.has_key(token)) or P_HT[token] == 0:
			P_HT[token] = (1.0)/float(store['V'] + store['sum_htoken'])
		if not(P_MT.has_key(token)) or P_MT[token] == 0:
			P_MT[token] = (1.0)/float(store['V'] + store['sum_mtoken'])
		if P_HT[token] < 0:
			continue
		s1 *= float(P_HT[token])
		s2 *= float(P_MT[token])

#	return s1 / ( s1 + s2 )
	return s1

def missProbability(tokens, P_HT, P_MT, P_H, P_M, store):
	res = 0
	s1 = P_M
	s2 = P_H
	for token in tokens:
		if token in stopword:
			continue
		if not(P_MT.has_key(token)) or P_MT[token] == 0:
			P_MT[token] = (1.0)/float(store['V'] + store['sum_mtoken'])
		if not(P_HT.has_key(token)) or P_HT[token] == 0:
			P_HT[token] = (1.0)/float(store['V'] + store['sum_htoken'])
		if P_MT[token] < 0:
			continue
		s1 *= float(P_MT[token])
		s2 *= float(P_HT[token])

	#return s1 / ( s1 + s2 )
	return s2

def init(keyword, songlist):
	# training
	#hsum, msum = train_frontend()
	P_TH, P_TM, store = getTokensProbability()
	hsum, msum = store['sum_htoken'], store['sum_mtoken']
	P_H = float(hsum) / float(hsum + msum)
	P_M = float(msum) / float(hsum + msum)

	# Bayesian Calculate
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

	return [P_HT, P_MT, P_H, P_M, hsum, msum, store]

# ================MAIN=====================
def main():
	keyword = "梁博"
	songlist = kuworank.main(keyword)
	editDict(songlist)

	P_HT, P_MT, P_H, P_M, hsum, msum, store = init(keyword, songlist)
	
	xmlOperation.create_xml(P_HT, "music_HT_dict.xml");
	xmlOperation.create_xml({'hits':P_H}, "music_H_dict.xml");
	xmlOperation.create_xml(P_MT, "music_MT_dict.xml");
	xmlOperation.create_xml({'miss':P_M}, "music_M_dict.xml");
	xmlOperation.create_xml(store, "store.xml");
	
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
