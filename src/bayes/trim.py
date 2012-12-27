#encoding=utf-8
import re
import sys
import getopt

def main():
	if len(sys.argv) <= 1:
		return
	argv = getopt.getopt(sys.argv[1:], "")
	filename = argv[1][0]
	p = re.compile("http[0-9|:|/| |.|a-z|A-Z]*")
	p1 = re.compile("\([^\)]*\)")
	p3 = re.compile("£¨[^£©]*£©")
	p2 = re.compile("@[^ ]* ")
	f = open(filename, 'r')
	lines = f.readlines()
	f.close()
	f = open(filename, 'w')
	for line in lines:
		line = re.sub(p,"",line)
		line = re.sub(p1,"",line)
		line = re.sub(p2,"",line)
		line = re.sub(p3,"",line)
		print line
		f.write(line)
	f.close()

if __name__ == "__main__":
	main()
