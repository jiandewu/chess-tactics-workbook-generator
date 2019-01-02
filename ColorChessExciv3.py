#!/usr/bin/python
#coding=utf-8
#Filename:ColorChessExci.py

import os
import time
import random

def genanimfram(steps,color=0):
	strsteps=[]
	for step in steps:
		if color==0:
			strsteps.append("\\newframe\\hidemoves{%s}\n\\currentboard"%(step))
		else:
			strsteps.append("\\hidemoves{%s}"%(step))
	return "\n".join(strsteps)
	
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
$\%s$%04d (mate in %d)\\
\newchessgame[id=show%04d,setfen=%s,moveid=%s%s]
\unitlength1pt
%s
\begin{animateinline}[controls]{0.5}
\begin{picture}(173.9,165)
\put(9,13){\chessboard[moverstyle=circle,pgfshortenend=0.3em,setfen=\xskakgetgame{initfen}]}
\end{picture}
\newframe
\xskakloop{
\getmovestyle{\xskakget{piecechar}}
\begin{picture}(164.1,165)
\put(-4.2,13){
\chessboard[moverstyle=circle,pgfstyle=\mymovestyle, color=red!50!gray,
pgfshortenend=0.3em,arrow=to,
markmoves=\xskakget{move},
coloremph,piececolor=warna1,
emphfields={\xskakget{moveto}},
setfen=\xskakget{nextfen}]}
\end{picture}
\newframe}
\begin{picture}(170.8,165)
\put(5.8,13){\chessboard[moverstyle=circle,pgfshortenend=0.3em,setfen=\xskakgetgame{lastfen}]}
\end{picture}
\end{animateinline}
\begin{itemize}
\setlength\itemsep{1em}
\item[(\quad).] \underline{\qquad\qquad\qquad} \underline{\qquad\qquad\qquad}
\item[(\quad).] \underline{\qquad\qquad\qquad} \underline{\qquad\qquad\qquad}
\item[(\quad).] \underline{\qquad\qquad\qquad} \underline{\qquad\qquad\qquad}
\item[(\quad).] \underline{\qquad\qquad\qquad} \underline{\qquad\qquad\qquad}
\item[(\quad).] \underline{\qquad\qquad\qquad} \underline{\qquad\qquad\qquad}
\end{itemize}
\end{minipage}'''%('natural' if chessdict[i]['mul_solution']==0 else 'sharp',i,chessdict[i]['mate_num'],i,chessdict[i]['fen'],chessdict[i]['fullmove_num'],chessdict[i]['move_first'],genanimfram(chessdict[i]['solve_sep'],1))
		elif style==12:
			texstr=r'''\begin{minipage}{0.25\linewidth}
$\%s$%04d (mate in %d)\\
\newchessgame[id=show%04d,setfen=%s,moveid=%s%s]
\unitlength1pt
%s
\begin{animateinline}[controls]{0.5}
\begin{picture}(135,135)
\put(7,13){\chessboard[moverstyle=circle,pgfshortenend=0.3em,setfen=\xskakgetgame{initfen}]}
\end{picture}
\newframe
\xskakloop{
\getmovestyle{\xskakget{piecechar}}
\begin{picture}(125,135)
\put(-6.5,13){
\chessboard[moverstyle=circle,pgfstyle=\mymovestyle, color=red!50!gray,
pgfshortenend=0.3em,arrow=to,
markmoves=\xskakget{move},
coloremph,piececolor=warna1,
emphfields={\xskakget{moveto}},
setfen=\xskakget{nextfen}]}
\end{picture}
\newframe}
\begin{picture}(131.5,135)
\put(3.5,13){\chessboard[moverstyle=circle,pgfshortenend=0.3em,setfen=\xskakgetgame{lastfen}]}
\end{picture}
\end{animateinline}
\end{minipage}
\begin{minipage}{0.25\linewidth}
  \begin{itemize}
    \setlength\itemsep{1em}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
    \item[(\quad).] \underline{\qquad\qquad}, \underline{\qquad\qquad}
  \end{itemize}
\end{minipage}'''%('natural' if chessdict[i]['mul_solution']==0 else 'sharp',i,chessdict[i]['mate_num'],i,chessdict[i]['fen'],chessdict[i]['fullmove_num'],chessdict[i]['move_first'],genanimfram(chessdict[i]['solve_sep'],1))
		
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
			end=len(questslist)
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
			end=len(rowlist)
		else:
			end=i+rpp
		pagestr=("\\\\[%scm]\n\n"%('1' if rpp==2 else '0.5')).join(rowlist[i:end])
		#pagestr="\\pagenumbering{arabic}\n"+pagestr
		pagelist.append(pagestr)
		if ((i+rpp)*qpr)>len(answerlist):
			end=-1
		else:
			end=(i+rpp)*qpr
		pagestr="\n\n".join(answerlist[i*qpr:end])
		pagestr="\\begin{multicols}{2}\n"+pagestr+"\\end{multicols}\\addtocounter{page}{-1}\n"
		#pagestr="\\pagenumbering{gobble}\\begin{multicols}{2}\n"+pagestr+"\\end{multicols}\n"
		pagelist.append(pagestr)
	return pagelist
	
def gendoc(pagelist):
	return "\n\n\\clearpage\n\n".join(pagelist)
	
def genquestlistEx(conf):
	totalnum=4462
	quests=[]
	wronglist=[]
	halfwronglist=[]
	if conf['wrong']!='':
		wronglist=conf['wrong'].split(',')
	if conf['halfwrong']!='':
		halfwronglist=conf['halfwrong'].split(',')

	for p in range(conf['page']):
		if conf['lastquestion']>=totalnum:
			break
		else:
			allquests=conf['lastquestion']+10*len(wronglist)+5*len(halfwronglist)
			if conf['lastquestion']>conf['randsel']*10:
				randlist=[]
				for i in range(conf['randsel']):
					while True:
						cat=random.random()
						if cat<=conf['lastquestion']/float(allquests):
							r1=random.randint(1,conf['lastquestion'])
						elif cat<=(conf['lastquestion']+10*len(wronglist))/float(allquests):
							r1=int(random.choice(wronglist))
						else:
							r1=int(random.choice(halfwronglist))
						if not(r1 in quests or r1 in randlist):
							break
					randlist.append(r1)
				randlist.sort()
				quests.extend(randlist)
				questend=conf['lastquestion']+conf['questperpage']-conf['randsel']+1
			else:
				questend=conf['lastquestion']+conf['questperpage']+1
			questend=questend if questend<=totalnum+1 else totalnum+1
			quests.extend(range(conf['lastquestion']+1,questend))
			conf['lastquestion']=quests[-1]
	return quests
	
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
		questend=conf['lastquestion']+1+desel*(p+1)
		quests.extend(range(conf['lastquestion']+1+desel*p,questend))
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
quests=genquestlistEx(conf)
answerlist=[]

texdoc=r'''\documentclass{article}
\usepackage[top=0.8in,bottom=0.5in,left=1cm,right=1cm]{geometry}
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

\newcommand\getmovestyle[1]{
\ifthenelse
{\equal{#1}{N}}
{\def\mymovestyle{[clockwise=false,style=knight]curvemove}}
{\ifthenelse
{\equal{#1}{}}
{\def\mymovestyle{curvemove}}
{\def\mymovestyle{straightmove}}}}

\newcommand\currentboard{
\begin{picture}(130,130)
\put(13,13){\chessboard[moverstyle=circle]}
\end{picture}}

%s

\end{document}'''%(boardfontsize,gendoc(genpage(genrow(geneachquest(quests)))))


bkdir=os.environ.get('jBACKUPDIR')
tmpdir=bkdir.replace('\\','/')+'/tmp/'
hwdir=bkdir.replace('\\','/')+'/HW/'

filename=tmpdir+'temp'
texfile=filename+'.tex'

handtex=open(texfile,'w')
handtex.write(texdoc)
handtex.close()

latex_command="xelatex -output-directory %s \"%s\"" %(tmpdir,texfile)
#latex_command="xelatex %s" %(handtexfile)
if os.system(latex_command)==0:
	# if os.system(latex_command)==0:
	pdfname=hwdir+time.strftime('%Y%m%d%H%M%S')+'chessCo_%04d_%s_'%(conf['lastquestion'],conf['questperpage'])+'.pdf'
	print "Successful generate PDF file, Now copy %s..."%pdfname
	os.system("mv -f "+filename+".pdf "+pdfname)
	#os.system("mv -f "+filename+".tex "+"test.tex")
	os.system("rm -f "+filename+"*")
else:
	print "First xelatex Failed!!!"

fout = open("helpGen.txt",'w')
for key, value in conf.iteritems():
	fout.write("%s=%s\n"%(key,value))
fout.close()
