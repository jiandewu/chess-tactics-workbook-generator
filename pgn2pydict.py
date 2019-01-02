#!/usr/bin/python
#coding=utf-8
#Filename:pgn2pydict.py

import os
import time, re
import codecs, random

def isint(value):
  try:
    int(value)
    return True
  except:
    return False

chessdict={}
key=0
fin = open("4462.pgn",'r')
for line in fin.readlines():
	line=line.rstrip()
	if line=='':
		continue
	if line[:6]=="[Event":
		attr=line.split()
		key=int(attr[1][2:-2])
		chessdict[key]={}
		chessdict[key]['solve']=[]
		chessdict[key]['solve_sep']=[]
		chessdict[key]['mul_solution']=0
	elif line[:6]=="[White":
		attr=line.split()
		if attr[-1][:3]=="one":
			chessdict[key]['mate_num']=1
		elif attr[-1][:3]=="two":
			chessdict[key]['mate_num']=2
		else:
			chessdict[key]['mate_num']=3
	elif line[:6]=="[Black":
		attr=line.split()
		if attr[1][1:6]=="White":
			chessdict[key]['move_first']='w'
		else:
			chessdict[key]['move_first']='b'
	elif line[:4]=="[FEN":
		chessdict[key]['fen']=line[6:-2]
		chessdict[key]['fullmove_num']=chessdict[key]['fen'].split()[-1]
	else:
		chessdict[key]['solve'].append(line)
		if line[0]!=' ' and line[0]!='(':
			line=re.sub(r" {.+}",'',line)
			steps=line.split()
			for i in range(len(steps)):
				if not isint(steps[i][0]):
					steps[i]=steps[i-1][0]+'...'+steps[i]
			chessdict[key]['solve_sep'].extend(steps)
		else:
			chessdict[key]['mul_solution']=1
fin.close()

fout = open("4462.txt",'w')
fout.write(repr(chessdict))
fout.close()
