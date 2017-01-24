#! /usr/bin/env python

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def domworld(*configs):
    G1 = raw_input("Do you want a graph of average dominance? y/n? ")   #Ask for which graphs you want
    allnames = []                                                       #Variables for creating graphs outside of the loop.
    print (configs)
    #if G1 == 'y':
	   #MAverageDom = []
    for ini in configs:
        numruns = int(os.popen("grep 'NumRuns' "+ ini +" | cut -d ' ' -f 3").read())
    	maxperiod = int(os.popen("grep 'Periods' "+ ini +" | cut -d ' ' -f 3").read())
    	startperiod = int(os.popen("grep 'firstDataPeriod' "+ ini +" | cut -d ' ' -f 3").read())
        periodduration = int(os.popen("grep 'PeriodDurationFactor' "+ ini +" | cut -d ' ' -f 3").read())
    	name = os.popen("grep 'OutFileName' "+ ini +" | cut -d ' ' -f 3").read()
        allnames = allnames.append(name)
    	totfemales = int(os.popen("grep 'NumFemales' "+ ini +" | cut -d ' ' -f 3").read())
    	totmales = int(os.popen("grep 'NumMales' "+ ini +" | cut -d ' ' -f 3").read())
    	totchimps = totfemales + totmales
    	#os.popen('wine cDomWorld.exe '+ ini)                      #Run domworld, using ini as input
    	os.popen('mkdir '+name+' -p').read()
        os.popen('mv *.csv '+name).read()
        os.popen('cat '+name+'/*.csv > '+ name).read()
