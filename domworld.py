#! /usr/bin/env python

import os            
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def domworld(*configs):
    """ Domworld function: Takes multiple (but atleast 1) config files as input 
    (Call as domworld('config.ini', 'config2.ini', etc). Runs them using Domworld.
    The data is extracted from the outputfiles and used to create both graphs
    depicting the settings from one configuration file, as well as graphs 
    which compare the results of the different configurations. It also asks which 
    graphs you want. Best working conditions for this script is inside the same
    folder as cDomWorld.exe and the config files you want to use (otherwise,
    use path for config files)"""
    #G1 = raw_input("Do you want a graph of average dominance? y/n? ")   #Ask for which graphs you want to create
    G2 =  raw_input("Do you want a pie chart of actions taken? y/n? ")
    allnames = []                                                       #Variables for creating comparison graphs outside of the loop.
    #if G1 == 'y':                                                     #If you want to graphs depicting average dominace, this will create a variable to to compare it outside the loop.
	   #MAverageDom = []
    #Add line which places all *.csv files in folder in a new folder so they are out of the way
    for ini in configs:                                                #Run the following code for each configuration file you put in.
    	maxperiod = int(os.popen("grep 'Periods' "+ ini +" | cut -d ' ' -f 3").read())                     #Extract some handy data from the config file. This line extracts the total number of periods
    	startperiod = int(os.popen("grep 'firstDataPeriod' "+ ini +" | cut -d ' ' -f 3").read())           #Extract the period from which the file will start measuring.
        periodduration = int(os.popen("grep 'PeriodDurationFactor' "+ ini +" | cut -d ' ' -f 3").read())   #Extract how many activations per individual constitutes as a period 
    	name = os.popen("grep 'OutFileName' "+ ini +" | cut -d ' ' -f 3").read().strip('\n').strip('"')    #Extracts name of the output file. Also delete the line endings and quotation marks for name
        allnames = allnames.append(name)                                                                   #Sends name outside the loop
    	totfemales = int(os.popen("grep 'NumFemales' "+ ini +" | cut -d ' ' -f 3").read())                 #Number of females
    	totmales = int(os.popen("grep 'NumMales' "+ ini +" | cut -d ' ' -f 3").read())                     #Number of males
    	totchimps = totfemales + totmales                                                                  #Total number of individuals
    	#os.popen('wine cDomWorld.exe '+ ini)                                                              #Run domworld, using ini as input
        filenumber = 1                                                                                     #Used in dataframe to differentiate between output of different files
        activat = (startperiod - 1) * periodduration * totchimps  #The first activation/datapoint that is recorded
        print activat
        endline = periodduration * totchimps * maxperiod          #The last activation/datapoint that is recorded
        print endline
        MonkeyFrame = pd.DataFrame({ 'Run' : 'NaN',               #Create the 'empty' dataframe with a junk line to add the other data to
		'Activation' : 'NaN', 
		'Period' : 'NaN', 
		'Individual' : 'NaN', 
		'Sex' : 'NaN',
		'Behavior' : 'NaN',
		'Score' :  'NaN',
        'Receiver_sex': 'NaN',
		'X-pos' : 'NaN', 
		'Y-pos' : 'NaN'},
		index = ['Junk'])
        for outputfiles in glob.glob(name+"*.csv"):                  #Run the following codeblock on each output csv file
            print 'Now processing :' + outputfiles              #Report which outputfile is currently being processed
            line = activat + 1                                  #Prepare the starting value for the while loop
            infile = open(outputfiles, 'r')                     #Open the output file for reading
            infile.readline()                                   #Skip over the header
            while line <= endline:                                 #While loop used to read the entire file until the last datapoint, as defined by the configfile
                current_line = infile.readline().split()           #Read line and safe it as list seperated by tabs
                NewFrame = pd.DataFrame({ 'Run' : current_line[1], #Create a new line to add to the dataframe. 
                'Activation' : int(current_line[2]),               
		        'Period' : int(current_line[3]), 
         		'Individual' : int(current_line[4]), 
	        	'Sex' : current_line[5],
	        	'Behavior' : current_line[6],
		        'Score' :  float(current_line[7]),
                'Receiver_sex': current_line[12],
	        	'X-pos' : float(current_line[9]), 
	        	'Y-pos' : float(current_line[10])},
		        index = ["F"+str(filenumber)+'A'+str(line)])      #Create a ascession code for the line, which consists of the File it is from + the Activation that is saved.
                line = line + 1                                   #+ 1 to close the loop at the end
                sep_pieces = [MonkeyFrame, NewFrame]              #Add the new line to the existing dataframe
                MonkeyFrame = pd.concat(sep_pieces)
            filenumber = filenumber + 1                           #+1 to indicate the next file with data to be added to the datafram
        MonkeyFrame = MonkeyFrame[1:]                 #Remove the junkline from the dataframe
        print MonkeyFrame.head(5)
        print MonkeyFrame.tail(5)
        test = MonkeyFrame
        if G2 == 'y':                                     #Create pie chart of actions taken
            labellist = MonkeyFrame.Behavior.unique()
            number_of_actions = MonkeyFrame.groupby('Behavior').Activation.nunique()
            max_cat = len(labellist)
            count = 0
            labels = 'test '
            while count < max_cat:
                labels = labels + labellist[count] + ' '
                count = count + 1
            labels = labels.split()
            labels = labels[1:]
            count = 0
            list_n_actions = []
            while count < max_cat:
                list_n_actions.append(number_of_actions[labels[count]])
                count = count + 1
            print labels
            print list_n_actions
            fig1, pie1 = plt.subplots()
            pie1.pie(list_n_actions, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
            pie1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.show()
            fig1.savefig(name + '_pie_chart.png')
                
        
        os.popen("mkdir -p Output_" + name)
        #os.popen('mv *.csv Output_'+name)
    os.popen("mkdir -p Comparison_Graphs")
 
    
domworld('config.ini')
