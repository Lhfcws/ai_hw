#! /usr/bin/python
#-*- coding:utf-8 -*-
# author: Lhfcws Wu [ 10389393 Wenjie Wu ]
# Copyright: Lhfcws
# Version: 1.0

def dbconfig():
	# Read server.conf
	f = open("server.conf", 'r')
	lines = f.readlines()
	f.close()

	# Trim the '\n'
	result = []
	for line in lines:
		result.append(line.strip())

	if len(result) < 3:
		print "Something missed in server.conf!\n"
	else:
		return result
