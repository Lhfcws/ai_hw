
from  xml.dom import  minidom
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')
#useful!
def get_xml_data(path):
	tag = 'item'
	dom = minidom.parse(path)
	root = dom.documentElement
	childs = root.getElementsByTagName(tag)
	dic = {}
	for item in childs:
		node_index = item.getElementsByTagName("index")
		index = node_index[0].childNodes[0].nodeValue
		node_frequency = item.getElementsByTagName("frequency")
		frequency = node_frequency[0].childNodes[0].nodeValue
		dic[index] = float(frequency)
	
	return dic

#this function is none of use
def get_xml_data_nums(root):
	maxid = root.getElementsByTagName("maxid")
	num = maxid[0].childNodes[0].nodeValue
	return num

#useful!
def create_xml(dic, path):
	impl = minidom.getDOMImplementation();
	dom = impl.createDocument(None, 'catalog', None);
	#define the root node
	root = dom.documentElement
	
	#count the length of the dic
	count = len(dic)
		
	#write the maxid node, indicate the length	
	maxid_text = dom.createTextNode(repr(count))
	maxid = dom.createElement('maxid')
	maxid.appendChild(maxid_text)
	root.appendChild(maxid)
	
	for key in dic.keys():
		item = dom.createElement('item')
		
		text1 = dom.createTextNode(key)
		sub_item1 = dom.createElement('index')
		sub_item1.appendChild(text1)
		text2 = dom.createTextNode(str(dic[key]))
		sub_item2 = dom.createElement('frequency')
		sub_item2.appendChild(text2)
		#append child 'index' and 'frequency' to each 'item'
		item.appendChild(sub_item1)
		item.appendChild(sub_item2)
		root.appendChild(item)
		# print item.toxml().decode('utf-8')
		# print item.childNodes[0].nodeValue.decode('utf-8')
	#print root.toxml().decode('utf-8')
	
	#write to the xml file
	f = open(path, 'w')
	dom.writexml(f, addindent = '	', newl = '\n')
	f.close()
	
	return 0

#this function is none of use besides test
def test_get_xml_data(root):
	count = get_xml_data_nums(root)
	print 'There are %d items.' % (int)(count)
	dic = get_xml_data()
	
	for key in dic.keys(): 
		print 'key=%s, value=%s' % (key, dic[key]) 
	#print '\n'
	

	
#entrance of the program

#test write xml
#impl = minidom.getDOMImplementation();
#dom2 = impl.createDocument(None, 'catalog', None);
#dic for test
#dic = {"陈潇楠": '0.05', '苍井空': '0.35', '小仓优子': '0.15'}
#create_xml(dic)



#test read xml
#dom = minidom.parse('g:/catalog.xml')
#root = dom.documentElement
#print get_xml_data_nums(root)
#test_get_xml_data(root)
