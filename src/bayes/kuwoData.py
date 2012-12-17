#encoding=utf8
import kuworank

def main():
	f = open("names.txt", 'r')
	lines = f.readlines()
	for line in lines:
		kugourank.main(line.strip())
	
if __name__ == "__main__":
	main()
