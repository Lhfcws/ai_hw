#not /usr/bin/python2
#encoding=utf-8

# P(H|T) = P(T|H)*P(H) / (P(T|H)*P(H) + P(T|M)*P(M))								Bayesian Law
# P(H|t1 ,t2, t3……tn) = (P1*P2*……PN) / [P1*P2*……PN + (1-P1)*(1-P2)*……(1-PN)] 		Compound Probability

import jieba

hitsFile = "hits.txt"
missFile = "miss.txt"
srcFile = "train.txt"


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
	seg_list = jieba.cut(sentence, cut_all=False)
	s = ','.join(seg_list)
	s = s.split(',')
	return s

def train_frontend():
	hitsFile = "hits.txt"
	missFile = "miss.txt"
	srcFile = "train.txt"

	lines = readFile(srcFile)
	hitlist = misslist = []

	for line in lines:
		print "=============================================================="
		print "Weibo: \n" + line
		print ""
		yn = raw_input("Is it about his music? (y/n): ")
		if yn == "y":
			hitlist.append(line)
		else:
			misslist.append(line)

	writeFile(hitlist, hitsFile)	
	writeFile(misslist, missFile)	
	return [len(hitlist), len(misslist)]

def getTokensProbability(hsum, msum):
	hitsFile = "hits.txt"
	missFile = "miss.txt"
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
			P_TH[token] = 1.0 / float(hsum)
		if not(P_TM.has_key(token)) or P_TM[token] == 0:
			P_TM[token] = 1.0 / float(msum)

		print P_H,P_M, P_TH[token], P_TM[token]
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
			P_TH[token] = 1.0 / float(hsum)
		if not(P_TM.has_key(token)) or P_TM[token] == 0:
			P_TM[token] = 1.0 / float(msum)

		P_MT[token] = getP_MT(P_H, P_M, P_TH[token], P_TM[token])
		
	return P_MT

def hitProbability(tokens, P_HT, hsum):
	res = 0
	s1 = 1
	s2 = 1
	for token in tokens:
		if not(P_HT.has_key(token)) or P_HT[token] == 0:
			P_HT[token] = 1.0 / float(hsum)
		s1 *= float(P_HT[token])
		s2 *= float(1 - P_HT[token])

	return s1 / ( s1 + s2 )

def missProbability(tokens, P_MT, msum):
	res = 0
	s1 = 1
	s2 = 1
	for token in tokens:
		if not(P_MT.has_key(token)) or P_MT[token] == 0:
			P_MT[token] = 1.0 / float(msum)
		s1 *= float(P_MT[token])
		s2 *= float(1 - P_MT[token])

	return s1 / ( s1 + s2 )

def init():
	# training
	hsum, msum = train_frontend()
	P_H = float(hsum) / float(hsum + msum)
	P_M = float(msum) / float(hsum + msum)

	# Bayesian Calculate
	P_TH, P_TM = getTokensProbability(hsum, msum)
	P_HT = getP_HT_Table(hsum, msum, P_TH, P_TM)
	P_MT = getP_MT_Table(hsum, msum, P_TH, P_TM)

	return [P_HT, P_MT, P_H, P_M, hsum, msum]

# ================MAIN=====================
def main():
	P_HT, P_MT, P_H, P_M, hsum, msum = init()
	
	lines = readFile("testFile.txt")
	resList = []

	for line in lines:
		tokens = segword(line)
		hitP = hitProbability(tokens, P_HT, hsum) * P_H
		missP = missProbability(tokens, P_MT, msum) * P_M
		if missP > hitP:
			resList.append(line)

	print P_HT
	print P_MT

	writeFile([str(len(lines))+"\n", len(resList)], "result.txt")



if __name__ == "__main__":
	main()
