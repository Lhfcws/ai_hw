#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bayes.xmlOperation import get_xml_data
from bayes import bayes 
import dbconf
import MySQLdb

def bayes_init(keyword):
	bayes.main(keyword)

def main():
	keyword = "Áº²©"
	con = dbconf.dbconfig()
	conn = MySQLdb.connect(host=con[0], user=con[1], passwd=con[2])
	conn.select_db("ai_hw")
	cursor = conn.cursor()

	P_HT = get_xml_data("bayes/music_HT_dict.xml")
	P_H = get_xml_data("bayes/music_H_dict.xml")
	P_MT = get_xml_data("bayes/music_MT_dict.xml")
	P_M = get_xml_data("bayes/music_M_dict.xml")

	P_H = P_H['hits']
	P_M = P_M['miss']
	lines = bayes.readFile("bayes/testFile.txt")
	resList = []
	for line in lines:
		tokens = bayes.segword(line)
		hitP = bayes.hitProbability(tokens, P_HT) * P_H
		missP = bayes.missProbability(tokens, P_MT) * P_M
		if missP < hitP:
			resList.append(line)

	cursor.execute("insert into `music_love` values("+str(len(lines))+","+str(len(resList))+", "+keyword+")")
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == "__main__":
	main()
