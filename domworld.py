#! /usr/bin/env python

import os            
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
import math

def domworld(*configs):
    """ Domworld function: Takes multiple (but atleast 1) config files as input 
    (Call as domworld('config.ini', 'config2.ini', etc). Runs them using Domworld.
    The data is extracted from the outputfiles and used to create both graphs
    depicting the settings from one configuration file, as well as graphs 
    which compare the results of the different configurations. It also asks which 
    graphs you want. Best working conditions for this script is inside the same
    folder as cDomWorld.exe and the config files you want to use (otherwise,
    use path for config files)"""
    G2 = raw_input("Do you want a box plot of average dominance? y/n? ")   #Ask for which graphs you want to create
    G1 = raw_input("Do you want a pie chart of actions taken? y/n? ")
    G3 = raw_input("Do you want a bar chart of the frequency of fighting? y/n? ")
    G4 = raw_input("Do you want a bar chart of the frequency of grooming? y/n? ")
    G5 = raw_input("Do you want a box plot of the average distance to centre? y/n? ")
    allnames = []                                                       #Variables for creating comparison graphs outside of the loop.
    #if G1 == 'y':                                                     #If you want to graphs depicting average dominace, this will create a variable to to compare it outside the loop.
	   #MAverageDom = []
    if G2 == 'y':
        pielabels = []
    #Add line which places all *.csv files in folder in a new folder so they are out of the way
    for ini in configs:                                                #Run the following code for each configuration file you put in.
    	maxperiod = int(os.popen("grep 'Periods' "+ ini +" | cut -d ' ' -f 3").read())                     #Extract some handy data from the config file. This line extracts the total number of periods
    	maxruns = int(os.popen("grep 'NumRuns' "+ ini +" | cut -d ' ' -f 3").read())
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
		'Activation' : 1, 
		'Period' :2, 
		'Individual' : 100, 
		'Sex' : 'NaN',
		'Behavior' : 'NaN',
		'Score' :  12.4,
        'Receiver_sex': 'NaN',
		'X_pos' : 22.1, 
		'Y_pos' : 839.1},
		index = ['Junk'])
        for outputfiles in glob.glob(name+"*.csv"):                  #Run the following codeblock on each output csv file
            print 'Now processing :' + outputfiles              #Report which outputfile is currently being processed
            line = activat + 1                                  #Prepare the starting value for the while loop
            infile = open(outputfiles, 'r')                     #Open the output file for reading
            infile.readline()                                   #Skip over the header
            while line <= endline:                                 #While loop used to read the entire file until the last datapoint, as defined by the configfile
                current_line = infile.readline().split()           #Read line and safe it as list seperated by tabs
                NewFrame = pd.DataFrame({ 'Run' : current_line[1], #Create a new line to add to the dataframe. 
                'Activation' : str(current_line[2]),               
		        'Period' : int(current_line[3]), 
         		'Individual' : int(current_line[4]), 
	        	'Sex' : current_line[5],
	        	'Behavior' : current_line[6],
		        'Score' :  float(current_line[7]),
                'Receiver_sex': current_line[12],
	        	'X_pos' : float(current_line[9]), 
	        	'Y_pos' : float(current_line[10])},
		        index = ["F"+str(filenumber)+'A'+str(line)])      #Create a ascession code for the line, which consists of the File it is from + the Activation that is saved.
                line = line + 1                                   #+ 1 to close the loop at the end
                sep_pieces = [MonkeyFrame, NewFrame]              #Add the new line to the existing dataframe
                MonkeyFrame = pd.concat(sep_pieces)
            filenumber = filenumber + 1                           #+1 to indicate the next file with data to be added to the datafram
        MonkeyFrame = MonkeyFrame[1:]                 #Remove the junkline from the dataframe
        if G1 == 'y':                                     #Create pie chart of actions taken
            labellist = MonkeyFrame.Behavior.unique()
            number_of_actions = MonkeyFrame.groupby('Behavior').Activation.nunique()
            max_cat = len(labellist)
            count = 0
            labels = 'junk '
            while count < max_cat:
                labels = labels + labellist[count] + ' '
                count = count + 1
            labels = labels.split()
            pielabels = labels[1:]
            count = 0
            list_n_actions = []
            while count < max_cat:
                list_n_actions.append(number_of_actions[pielabels[count]])
                count = count + 1
            fig1, pie1 = plt.subplots()
            pie1.pie(list_n_actions, labels=pielabels, autopct='%1.1f%%',shadow=True, startangle=90)
            pie1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.show()
            fig1.savefig(name + '_pie_chart.png')
            print list_n_actions
        if G3 == 'y':                            #Create frequenccy of aggresion bar plot
            n_interactions = MonkeyFrame.groupby(['Run','Behavior', 'Sex', 'Receiver_sex']).Activation.nunique()      #Reframe matrix to easily get the actions per sex and opponent sex
            current_run = 1                                  #Variables for the loop
            malemale = []
            femalefemale = []
            intersex = []
            while current_run <= maxruns:                              #Create a list with the amount of fight actions taken per inputfile)
                malemale.append(n_interactions[str(current_run), 'Fight', 'M', 'M'])
                intersex.append(n_interactions[str(current_run), 'Fight', 'F', 'M'] + n_interactions[str(current_run),'Fight', 'M', 'F'])
                femalefemale.append(n_interactions[str(current_run), 'Fight', 'F', 'F'])
                current_run = current_run + 1
            mean_malemale = st.mean(malemale)                                             #Calculate means of the interactions
            mean_intersex = st.mean(intersex)
            mean_femalefemale = st.mean(femalefemale)
            ste_malemale = st.stdev(malemale) / math.sqrt(mean_malemale)                  #Calculate standard error of the interactions
            ste_intersex = st.stdev(intersex) / math.sqrt(mean_intersex)
            ste_femalefemale = st.stdev(femalefemale) / math.sqrt(mean_femalefemale)
            x_values = [mean_malemale, mean_femalefemale, mean_intersex]                 #Put means and standard error into lists
            sterror =  [ste_malemale, ste_femalefemale, ste_intersex]
            fig2, bar1 = plt.subplots()
            ind = np.arange(3)
            bar1.bar(ind + 0.35, x_values, width = 0.35,color='b', yerr = sterror, ecolor='black')                       #Create barplot
            bar1.set_title('Frequency of Agression')
            bar1.set_ylabel('# of attacks')
            bar1.set_xticks(ind + 0.54)
            bar1.set_xticklabels(('Male-Male', 'Female-Female', 'Intersex'))
            plt.show()
            fig2.savefig(name + '_aggression_bar_chart.png')
        if G4 == 'y':                                               #Create frequency of grooming barplot
            n_interactions = MonkeyFrame.groupby(['Run','Behavior', 'Sex', 'Receiver_sex']).Activation.nunique()      #Reframe matrix to easily get the actions per sex and opponent sex
            current_run = 1                                  #Variables for the loop
            malemale = []
            femalefemale = []
            intersex = []
            while current_run <= maxruns:                              #Create a list with the amount of fight actions taken per inputfile)
                malemale.append(n_interactions[str(current_run), 'Groom', 'M', 'M'])
                intersex.append(n_interactions[str(current_run), 'Groom', 'F', 'M'] + n_interactions[str(current_run),'Fight', 'M', 'F'])
                femalefemale.append(n_interactions[str(current_run), 'Groom', 'F', 'F'])
                current_run = current_run + 1
            mean_malemale = st.mean(malemale)                                             #Calculate means of the interactions
            mean_intersex = st.mean(intersex)
            mean_femalefemale = st.mean(femalefemale)
            ste_malemale = st.stdev(malemale) / math.sqrt(mean_malemale)                  #Calculate standard error of the interactions
            ste_intersex = st.stdev(intersex) / math.sqrt(mean_intersex)
            ste_femalefemale = st.stdev(femalefemale) / math.sqrt(mean_femalefemale)
            x_values = [mean_malemale, mean_femalefemale, mean_intersex]                 #Put means and standard error into lists
            sterror =  [ste_malemale, ste_femalefemale, ste_intersex]
            fig2, bar1 = plt.subplots()
            ind = np.arange(3)
            bar1.bar(ind + 0.35, x_values, width = 0.35,color='r', yerr = sterror, ecolor='black')                       #Create barplot
            bar1.set_title('Frequency of Grooming')
            bar1.set_ylabel('# of grooms')
            bar1.set_xticks(ind + 0.54)
            bar1.set_xticklabels(('Male-Male', 'Female-Female', 'Intersex'))
            plt.show()
            fig2.savefig(name + '_grooming_bar_chart.png')            
        if G2 == 'y':                             #Boxplot average dominance
            doms = MonkeyFrame.loc[:,['Score', 'Activation','Run']]
            sexdom = MonkeyFrame.loc[:,['Sex','Score', 'Activation','Run']]
            femdom = sexdom[(sexdom.Sex == 'F')].loc[:,['Score', 'Activation', 'Run']]
            mdom = sexdom[(sexdom.Sex == 'M')].loc[:,['Score', 'Activation', 'Run']]
            femdommatrix = pd.merge(femdom, mdom, how = 'left', on = ['Activation', 'Run'])
            mdommatrix = pd.merge(mdom, femdom, how = 'left', on = ['Activation', 'Run'])
            alldommatrix = pd.merge(doms, mdom, how = 'left', on = ['Activation', 'Run'])
            alldommatrix = alldommatrix.loc[:,['Score_x', 'Score_y']].as_matrix()
            femdommatrix = femdommatrix.loc[:,['Score_x', 'Score_y']].as_matrix()
            mdommatrix = mdommatrix.loc[:,['Score_x', 'Score_y']].as_matrix()
            #print alldommatrix
            fig3, box1 = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6), sharey=True)
            #labels = ['Males', 'Females', 'All_individuals']
            box1[1,0].boxplot(mdommatrix, labels=('Male', ''), showmeans=True, positions = ([1.5, 1.5]))
            box1[1,0].set_title('Male Dominance', fontsize=10)
            box1[0,1].boxplot(femdommatrix, labels=('Female',''), showmeans=True, positions = ([1.5, 1.5]))
            box1[0,1].set_title('Female Dominance', fontsize=10)
            box1[0,0].boxplot(alldommatrix, labels=('All Inividuals', ''), showmeans=True, positions = ([1.5, 1.5]))
            box1[0,0].set_title('Dominance', fontsize=10)
            plt.show()
            fig3.savefig(name + '_All_Dom_Box.png')
        if G5 == 'y':                            
            centralxy = MonkeyFrame.loc[:,['X_pos', 'Y_pos', 'Sex', 'Activation', 'Run']].rolling(window = 20).mean()
            indixy = MonkeyFrame.loc[:,['X_pos', 'Y_pos', 'Sex', 'Activation', 'Run']].rolling(window = 1).mean()
            sqrx = centralxy.X_pos.subtract(indixy.X_pos).abs().pow(2)
            sqry = centralxy.Y_pos.subtract(indixy.Y_pos).abs().pow(2)
            zside = sqrx.add(sqry)
            zside = zside.apply(np.sqrt)
            zside = zside.fillna(zside.mean())
            distmatrix = pd.concat([zside, MonkeyFrame.loc[:,['Sex', 'Activation', 'Run']].rolling(window = 1).mean()], axis = 1)
            mdist = distmatrix[(distmatrix.Sex == 'M')].loc[:,[0, 'Sex', 'Activation', 'Run']]
            femdist = distmatrix[(distmatrix.Sex == 'F')].loc[:,[0, 'Sex', 'Activation', 'Run']]
            mdistmatrix = pd.merge(mdist, femdist, how = 'left', on = ['Activation', 'Sex', 'Run'])
            femdistmatrix = pd.merge(femdist, mdist, how = 'left', on = ['Activation', 'Sex', 'Run'])
            alldistmatrix = pd.merge(distmatrix, femdist, how = 'left', on = ['Activation', 'Sex', 'Run'])
            alldistmatrix = alldistmatrix.loc[:,['0_x', '0_y']].as_matrix()
            femdistmatrix = femdistmatrix.loc[:,['0_x', '0_y']].as_matrix()
            mdistmatrix = mdistmatrix.loc[:,['0_x', '0_y']].as_matrix()
            print alldistmatrix
            fig4, box2 = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6), sharey=True)
            box2[1,0].boxplot(mdistmatrix, labels=('Male', ''), showmeans=True, positions = ([1.5, 1.5]))
            box2[1,0].set_title('Male Distance from Center with outliers', fontsize=10)
            box2[0,1].boxplot(femdistmatrix, labels=('Female',''), showmeans=True, positions = ([1.5, 1.5]))
            box2[0,1].set_title('Female Distance from Center with outliers', fontsize=10)
            box2[0,0].boxplot(alldistmatrix, labels=('All Inividuals', ''), showmeans=True, positions = ([1.5, 1.5]))
            box2[0,0].set_title('Distance from Center with outliers', fontsize=10)
            plt.show()
            fig4.savefig(name + '_All_Dist_Box.png')
            fig4, box2 = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6), sharey=True)
            box2[1,0].boxplot(mdistmatrix, labels=('Male', ''), showmeans=True, positions = ([1.5, 1.5]), sym = '')
            box2[1,0].set_title('Male Distance from Center', fontsize=10)
            box2[0,1].boxplot(femdistmatrix, labels=('Female',''), showmeans=True, positions = ([1.5, 1.5]), sym = '')
            box2[0,1].set_title('Female Distance from Center', fontsize=10)
            box2[0,0].boxplot(alldistmatrix, labels=('All Inividuals', ''), showmeans=True, positions = ([1.5, 1.5]), sym = '')
            box2[0,0].set_title('Distance from Center', fontsize=10)
            plt.show()
            fig4.savefig(name + '_All_Dist_Box.png')
        os.popen("mkdir -p Output_" + name)
        #os.popen('mv ' + name + '*.csv Output_'+name)
    os.popen("mkdir -p Comparison_Graphs")
 
    
domworld('config.ini')
