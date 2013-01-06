#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import kuworank
import math
import numpy
import random
import matplotlib.pyplot as Mp

# Following functions are for least-square method.

def f(i, x):
	return x**i

def leastSquareSolve(xa, ya):
	global ORDER
	# Linear Fitting
	ORDER = 1
	Y = numpy.array(ya)
	matf = []
	for x in xa:
		l = []
		for o in range(ORDER):
			a = f(o, x)
			l.append(float(a))
		matf.append(l)
		 
	F = numpy.array(matf)
	C = numpy.linalg.solve(F, Y)
	return C

def leastSquarePrepare(xa, ya):
	
	return leastSquareSolve(xa, ya)

def leastSquare(x,C):
	s = 0
	for i in range(ORDER):
		s = float(s) + float(C[i]) * f(i, x)
	
	return s
#=========================================

def sortDictByValues(d, key):
	items = d.items()
	inv = [[v[1],v[0]] for v in items]
	inv = sorted(inv, reverse=True)

	newd = dict()
	for i in inv:
		newd[i[1]] = i[0]
	
	return newd

# Change the songs in the probability table.
def trans(dic, key1, key2):
	pr = dic
	for k in key1:
		if dic.has_key(k):
#			pr[k] = dic[k]
			pass
		else:
		 	pr[k] = -1
	
	#pr = sortDictByKey1(pr, key1)
	xa = []
	ya = []
	for i in range(1, len(key1)+1):
		if pr[key1[i-1]] != -1:
			xa.append(i)
			ya.append(pr[key1[i-1]])
	
	C = leastSquarePrepare(xa, ya)

	for i in range(1, len(key1)+1):
		if pr[key1[i-1]] == -1:
			pr[key1[i-1]] = leastSquare(i, C)
	
	longer = False
	for i in range(len(key1)):
		if len(key2) <= i:
			longer = True
			break
		pr[key2[i]] = pr[key1[i]]
		pr.pop(key1[i])
	
	# if key2 is longer than key1
	if longer:
		for i in range(len(key1)+1, len(key2)):
			pr[key2[i]] = leastSquare(i, C)
	
	return pr

def main(dic, keyword2):
	#print dic
	keyword1 = u"\u6881\u535a"
	dic[keyword2.decode("utf-8")] = dic[keyword1]
	dic.pop(keyword1)
	keylist1 = kuworank.main(keyword1.encode("utf-8"))
	keylist2 = kuworank.main(keyword2)
	pr = trans(dic, keylist1, keylist2)
	return pr
