#! /usr/bin/env python

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def domworld(*configs):
    #G1 = raw_input("Do you want a graph of average dominance? y/n? ")   #Ask for which graphs you want
    allnames = []                                                       #Variables for creating graphs outside of the loop.
    print (configs)
    #if G1 == 'y':
	   #MAverageDom = []
    for ini in configs:
        numruns = int(os.popen("grep 'NumRuns' "+ ini +" | cut -d ' ' -f 3").read())
    	maxperiod = int(os.popen("grep 'Periods' "+ ini +" | cut -d ' ' -f 3").read())
    	startperiod = int(os.popen("grep 'firstDataPeriod' "+ ini +" | cut -d ' ' -f 3").read())
        periodduration = int(os.popen("grep 'PeriodDurationFactor' "+ ini +" | cut -d ' ' -f 3").read())
    	name = os.popen("grep 'OutFileName' "+ ini +" | cut -d ' ' -f 3").read().strip('\n').strip('"')
        allnames = allnames.append(name)
    	totfemales = int(os.popen("grep 'NumFemales' "+ ini +" | cut -d ' ' -f 3").read())
    	totmales = int(os.popen("grep 'NumMales' "+ ini +" | cut -d ' ' -f 3").read())
    	totchimps = 10#totfemales + totmales
    	#os.popen('wine cDomWorld.exe '+ ini)                      #Run domworld, using ini as input
        filenumber = 1
        activat = (startperiod - 1) * periodduration * totchimps
        print activat
        endline = periodduration * totchimps * maxperiod
        print endline
        MonkeyFrame = pd.DataFrame({ 'Run' : 'NaN', 
		'Activation' : 'NaN', 
		'Period' : 'NaN', 
		'Individual' : 'NaN', 
		'Sex' : 'NaN',
		'Behavior' : 'NaN',
		'Score' :  'NaN',
		'X-pos' : 'NaN', 
		'Y-pos' : 'NaN'},
		index = ['Init'])
        for outputfiles in glob.glob("*.csv"):
            print 'Now processing :' + outputfiles
            line = activat + 1
            infile = open(outputfiles, 'r')
            infile.readline()
            while line <= endline:
                current_line = infile.readline().split()
                NewFrame = pd.DataFrame({ 'Run' : current_line[1], 
                'Activation' : int(current_line[2]), 
		        'Period' : int(current_line[3]), 
         		'Individual' : int(current_line[4]), 
	        	'Sex' : current_line[5],
	        	'Behavior' : current_line[6],
		        'Score' :  float(current_line[7]),
	        	'X-pos' : float(current_line[9]), 
	        	'Y-pos' : float(current_line[10])},
		        index = ["F"+str(filenumber)+'A'+str(line)])
                line = line + 1
                sep_pieces = [MonkeyFrame, NewFrame]
                MonkeyFrame = pd.concat(sep_pieces)
            filenumber = filenumber + 1
        #Remove startline van Monkeydata
        print MonkeyFrame.head(5)
        print MonkeyFrame.tail(5)
        print MonkeyFrame['Init']
        
        
        
        
        os.popen("mkdir -p Output_" + name)
        #os.popen('mv *.csv Output_'+name)

 
      
domworld('config.ini')