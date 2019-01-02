#!/usr/bin/python
#coding=utf-8
#Filename:GenChessExci.py

import os
import time
import random

def geneachquest(quests):
	global answerlist,style
	chessfile = open("./4462.txt",'r')
	line=chessfile.read()
	chessdict=eval(line)
	chessfile.close()
	questslist=[]
	for i in quests:
		if style==21:
			texstr=r'''\begin{minipage}{0.33\linewidth}
\#%04d (mate in %s)\\
\newchessgame[id=show%04d,
setfen=%s,moverstyle=circle,print]
\begin{itemize}
\setlength\itemsep{1em}
\item[]
\item[(\quad).] \underline{\qquad\qquad\quad} \underline{\qquad\qquad\quad}
\item[(\quad).] \underline{\qquad\qquad\quad} \underline{\qquad\qquad\quad}
\item[(\quad).] \underline{\qquad\qquad\quad} \underline{\qquad\qquad\quad}
\item[(\quad).] \underline{\qquad\qquad\quad} \underline{\qquad\qquad\quad}
\item[(\quad).] \underline{\qquad\qquad\quad} \underline{\qquad\qquad\quad}
\end{itemize}
\end{minipage}'''%(i,chessdict[i]['mate_num'],i,chessdict[i]['fen'])
		elif style==12:
			texstr=r'''\begin{minipage}{0.25\linewidth}
\#%04d (mate in %s)\\
\newchessgame[id=show%04d,
setfen=%s,moverstyle=circle,print]
\end{minipage}
\begin{minipage}{0.25\linewidth}
  \begin{itemize}
    \setlength\itemsep{1em}
    \item[]
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
  \end{itemize}
\end{minipage}'''%(i,chessdict[i]['mate_num'],i,chessdict[i]['fen'])
		
		questslist.append(texstr)
		
		texstr=r'''\begin{verbatim}
#%04d
%s
\end{verbatim}'''%(i,"\n".join(chessdict[i]['solve']))
		answerlist.append(texstr)
	return questslist
		
def genrow(questslist):
	global qpr
	rowlist=[]
	for i in range(0,len(questslist),qpr):
		if (i+qpr)>len(questslist):
			end=-1
		else:
			end=i+qpr
		rowstr="\n".join(questslist[i:end])
		rowlist.append(rowstr)
	return rowlist
	
def genpage(rowlist):
	global answerlist,rpp,qpr
	pagelist=[]
	for i in range(0,len(rowlist),rpp):
		if (i+rpp)>len(rowlist):
			end=-1
		else:
			end=i+rpp
		pagestr="\\\\[1cm]\n\n".join(rowlist[i:end])
		#pagestr="\\pagenumbering{arabic}\n"+pagestr
		pagelist.append(pagestr)
		if ((i+rpp)*qpr)>len(answerlist):
			end=-1
		else:
			end=(i+rpp)*qpr
		pagestr="\n\n".join(answerlist[i*qpr:end])
		pagestr="\\pagenumbering{gobble}\\thispagestyle{empty}\\begin{multicols}{2}\n"+pagestr+"\\end{multicols}\\pagenumbering{arabic}\n"
		#pagestr="\\pagenumbering{gobble}\\begin{multicols}{2}\n"+pagestr+"\\end{multicols}\n"
		pagelist.append(pagestr)
	return pagelist
	
def gendoc(pagelist):
	return "\n\n\\clearpage\n\n".join(pagelist)
	
def genquestlist(conf):
	desel=conf['questperpage']
	quests=[]
	if conf['wrong']!='' and conf['halfwrong']!='' :
		wronglist=conf['wrong'].split(',')
		halfwronglist=conf['halfwrong'].split(',')
		allquests=conf['lastquestion']+10*len(wronglist)+5*len(halfwronglist)
	else:
		allquests=conf['lastquestion']
	for p in range(conf['page']):
		if conf['lastquestion']>conf['randsel']+10:
			desel=conf['questperpage']-conf['randsel']
			randlist=[]
			for i in range(conf['randsel']):
				while True:
					cat=random.random()
					if cat<conf['lastquestion']/float(allquests):
						r1=random.randint(1,conf['lastquestion'])
					elif cat<(conf['lastquestion']+10*len(wronglist))/float(allquests):
						r1=int(random.choice(wronglist))
					else:
						r1=int(random.choice(halfwronglist))
					if not(r1 in quests or r1 in randlist):
						break
				randlist.append(r1)
			randlist.sort()
			quests.extend(randlist)
		quests.extend(range(conf['lastquestion']+1+desel*p,conf['lastquestion']+1+desel*(p+1)))
	return quests

conf={'lastquestion': 0, 'questperpage': 6, 'randsel': 2, 'page': 1}
fin = open("helpGen.txt",'r')
for line in fin.readlines():
	line=line.strip()
	attr=line.split("=")
	if attr[0]=="wrong" or attr[0]=="halfwrong":
		conf[attr[0]]=attr[1]
	else:
		conf[attr[0]]=int(attr[1])
fin.close()

rpp=2
qpr=3
style=21
boardfontsize=0.65
if conf['questperpage']==8:
	rpp=4
	qpr=2
	style=12
	boardfontsize=0.5
else:
	conf['questperpage']=6
quests=genquestlist(conf)
answerlist=[]

texdoc=r'''\documentclass{article}
\usepackage[top=0.8in,bottom=1in,left=1cm,right=1cm]{geometry}
\usepackage{multicol}
\usepackage[indonesian]{babel}
\usepackage{animate}
\usepackage{chessboard,xskak}
\definecolor{warna1}{HTML}{1E90FF}
\definecolor{warna2}{HTML}{F0E68C}
\definecolor{warna3}{HTML}{2F4F4F}
\usepackage[colorlinks]{hyperref}

\begin{document}
\setchessboard{boardfontsize=%scm,shortenend=5pt, margin=false}
\skaklanguage[english]

%s

\end{document}'''%(boardfontsize,gendoc(genpage(genrow(geneachquest(quests)))))

handfile='temp'
handtexfile=handfile+'.tex'
handtex=open(handtexfile,'w')
handtex.write(texdoc)
handtex.close()

if conf['randsel']<conf['questperpage']:
	conf['lastquestion']=quests[-1]

latex_command="xelatex %s" %(handtexfile)
if os.system(latex_command)==0:
	# if os.system(latex_command)==0:
		pdfname='chess_%04d_%s_'%(conf['lastquestion'],conf['questperpage'])+time.strftime('%Y%m%d%H%M')+'.pdf'
		print "Successful generate PDF file, Now copy %s..."%pdfname
		os.system("mv -f "+handfile+".pdf "+pdfname)
		#os.system("mv -f "+handfile+".tex "+"test.tex")
		os.system("rm -f "+handfile+"*")
else:
	print "First xelatex Failed!!!"

fout = open("helpGen.txt",'w')
for key, value in conf.iteritems():
	fout.write("%s=%s\n"%(key,value))
fout.close()
