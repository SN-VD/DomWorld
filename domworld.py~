#!/usr/bin/env python

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def domworld (*configs):
	#G1 = raw_input("Do you want a graph of average dominance? y/n?")   #Ask for which graphs you want
	allnames = []                                                       #Variables for creating graphs outside of the loop.
	print ("Outside loop ok)
	#if G1 == 'y':
		#MAverageDom = []
	for ini in configs:
		numruns = os.popen("grep 'NumRuns' "+ ini +" | cut -d ' ' -f 3").read
		print('inside loop ok')
		maxperiod = os.popen("grep 'Periods' "+ ini +" | cut -d ' ' -f 3").read
		startperiod = os.popen("grep 'firstDataPeriod' "+ ini +" | cut -d ' ' -f 3").read
		periodduration = os.popen("grep 'PeriodDurationFactor' "+ ini +" | cut -d ' ' -f 3").read
		name = os.popen("grep 'OutFileName' "+ ini +" | cut -d ' ' -f 3").read
		allnames = allnames.append(name)
		totfemales = os.popen("grep 'NumFemales' "+ ini +" | cut -d ' ' -f 3").read 
		totmales = os.popen("grep 'NumMales' "+ ini +" | cut -d ' ' -f 3").read
		totchimps = totfemales + totmales
		#os.popen('wine cDomWorld.exe '+ ini)                      #Run domworld, using ini as input
		os.popen('cat '+ name +'*.csv > ' +name+'.csv')
