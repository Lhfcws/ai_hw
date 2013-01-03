#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bayes.xmlOperation import get_xml_data
from bayes import bayes 
from bayes import transinger
import dbconf
import MySQLdb

def bayes_init(keyword):
	bayes.main(keyword)

def main():
	con = dbconf.dbconfig()
	conn = MySQLdb.connect(host=con[0], user=con[1], passwd=con[2])
	conn.select_db("ai_hw")
	cursor = conn.cursor()
	cursor.execute("SET NAMES 'utf8'")
	conn.commit()
	cursor.execute("SELECT * FROM `request` order by id desc limit 1")
	ls = cursor.fetchall()
	keyword = ls[0][1]
	print keyword

	P_HT = get_xml_data("bayes/music_HT_dict.xml")
	P_H = get_xml_data("bayes/music_H_dict.xml")
	P_MT = get_xml_data("bayes/music_MT_dict.xml")
	P_M = get_xml_data("bayes/music_M_dict.xml")
	store = get_xml_data("bayes/store.xml")

	P_H = P_H['hits']
	P_M = P_M['miss']
	P_HT = transinger.main(P_HT, keyword)
	P_MT = transinger.main(P_MT, keyword)

	#lines = bayes.readFile("bayes/testFile.txt")
	cursor.execute("SELECT weibo FROM `users` WHERE users.keyword = '"+keyword+"'")
	ls = cursor.fetchall()
	lines = []
	for i in range(len(ls)):
		lines.append(ls[i][0])

	resList = []
	msl = []
	for line in lines:
		tokens = bayes.segword(line)
		hitP = bayes.hitProbability(tokens, P_HT, P_MT, P_H, P_M, store)
		missP = bayes.missProbability(tokens, P_HT, P_MT, P_H, P_M, store)
		if missP/ hitP < 10.0:
			resList.append(line+'\n')
		else:
			msl.append(line+'\n')

	bayes.writeFile(resList, "bayes/testResult.txt")
	bayes.writeFile(msl, "bayes/MisResult.txt")
	cursor.execute("insert into `music_love` values("+str(len(lines))+","+str(len(resList))+", '"+keyword+"')")
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == "__main__":
	main()
