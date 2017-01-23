#!/usr/bin/env python

import os

def domworld (*configs)
	#G1 = raw_input("Do you want a graph of average dominance? y/n?")
	#if G1 == 'y':
		#MAverageDom = []
	for ini in configs:
		os.popen('wine cDomWorld.exe '+ ini)

