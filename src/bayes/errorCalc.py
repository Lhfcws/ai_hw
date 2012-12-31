#encoding=utf-8

def calc(M_H, H_M):
	f = open("testResult.txt",'r')
	lines = f.readlines()
	SUM_H = len(lines)
	f.close()
	f = open("MisResult.txt",'r')
	lines = f.readlines()
	SUM_M = len(lines)
	f.close()

	return ((SUM_H - M_H + H_M)/float(SUM_H + H_M) + (SUM_M - H_M + M_H)/float(SUM_M + M_H) )/2.0


