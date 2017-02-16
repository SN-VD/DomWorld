#! /usr/bin/env python

import os            
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
import math
import matplotlib.cm as cmx
import matplotlib.colors as colors

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.''' "Not my own function. Source:http://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib"
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color

def domworld(*configs):
    """ Domworld function: Takes multiple (but atleast 1) config files as input 
    (Call as domworld('config.ini', 'config2.ini', etc). Runs them using Domworld.
    The data is extracted from the outputfiles and used to create both graphs
    depicting the settings from one configuration file, as well as graphs 
    which compare the results of the different configurations. It also asks which 
    graphs you want. Best working conditions for this script is inside the same
    folder as cDomWorld.exe and the config files you want to use (otherwise,
    use path for config files). Last function supports up to 5 config files. 
    Any more and it won't add them to the comparison anymore"""
    G2 = raw_input("Do you want a box plot and bar plot of average dominance? y/n? ")   #Ask for which graphs you want to create
    G1 = raw_input("Do you want a pie chart of actions taken? y/n? ")
    G3 = raw_input("Do you want a bar chart of the frequency of fighting? y/n? ")
    G4 = raw_input("Do you want a bar chart of the frequency of grooming? y/n? ")
    G5 = raw_input("Do you want a box plot and bar plot of the average distance to centre? y/n? ")
    G6 = raw_input("Do you want a box plot and bar plot of the steepness of the dominance hierarchy? y/n? ")
    G7 = raw_input("Do you want a box plot and bar plot of the degree of female dominance? y/n? ")
    G8 = raw_input("Do you want a error plot of the change in dominance over time? y/n? ")
    G9 = raw_input("Do you want a error plot of the change in steepness of the dominance hierarchy over time? y/n? ")
    allnames = 'junk '
    inicount = 0                                                       #Variables for creating comparison graphs outside of the loop.
    operiod_range = []
    if G2 == 'y':                                                     #If you want to graphs depicting average dominace, this will create a variable to to compare it outside the loop
        G2mste = []
        G2mmean = []
        G2allste = []
        G2allmean = []
        G2femste = []
        G2femmean = []
    if G3 == 'y':
        outx_values_fight_inter = []
        outsterror_fight_inter = []
        outx_values_fight_mm = []
        outsterror_fight_mm = []
        outx_values_fight_ff = []
        outsterror_fight_ff = []
    if G4 == 'y':
        outx_values_groom_inter = []
        outsterror_groom_inter = []
        outx_values_groom_mm = []
        outsterror_groom_mm = []
        outx_values_groom_ff = []
        outsterror_groom_ff = []
    if G5 == 'y':
        G5mdists = []
        G5femdists = []
        G5alldists = []
    if G6 == 'y':
        G6msteep = []
        G6femsteep = []
        G6allsteep = []
    if G7 == 'y':
        G7femdom = []
    if G8 == 'y':
        G8mste = []
        G8femste = []
        G8allste = []
        G8mmean = []
        G8femmean = []
        G8allmean = []
    if G9 == 'y':
        G9mste = []
        G9femste = []
        G9allste = []
        G9mmean = []
        G9femmean = []
        G9allmean = []
    for ini in configs:                                                #Run the following code for each configuration file you put in.
    	maxperiod = int(os.popen("grep 'Periods' "+ ini +" | cut -d ' ' -f 3").read())                     #Extract some handy data from the config file. This line extracts the total number of periods
    	maxruns = int(os.popen("grep 'NumRuns' "+ ini +" | cut -d ' ' -f 3").read())
        startperiod = int(os.popen("grep 'firstDataPeriod' "+ ini +" | cut -d ' ' -f 3").read())           #Extract the period from which the file will start measuring.
        periodduration = int(os.popen("grep 'PeriodDurationFactor' "+ ini +" | cut -d ' ' -f 3").read())   #Extract how many activations per individual constitutes as a period 
    	name = os.popen("grep 'OutFileName' "+ ini +" | cut -d ' ' -f 3").read().strip('\n').strip('"')    #Extracts name of the output file. Also delete the line endings and quotation marks for name
        allnames = allnames + name + ' '                                                                   #Sends name outside the loop
    	totfemales = int(os.popen("grep 'NumFemales' "+ ini +" | cut -d ' ' -f 3").read())                 #Number of females
    	totmales = int(os.popen("grep 'NumMales' "+ ini +" | cut -d ' ' -f 3").read())                     #Number of males
    	totchimps = totfemales + totmales                                                                  #Total number of individuals
    	m_range = range(totfemales + 1, totchimps + 1)
        fem_range = range(1, totfemales + 1)
        tot_range = range(1, totchimps + 1)
        period_range = range(startperiod, maxperiod + 1)
        operiod_range.append(period_range)
        print 'Now running ' + str(ini) + ' in Domworld'
        os.popen('wine cDomWorld.exe '+ ini).read()                                                              #Run domworld, using ini as input. Dont use if you dont have cDomWorld.exe, but do have a config + output
        inicount = inicount + 1
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
            filenumber = filenumber + 1                           #+1 to indicate the next file with data to be added to the datafram
            line = activat + 1                                  #Prepare the starting value for the while loop
            infile = open(outputfiles, 'r')                     #Open the output file for reading
            infile.readline()                                   #Skip over the header
            while line <= endline:                                 #While loop used to read the entire file until the last datapoint, as defined by the configfile
                current_line = infile.readline().split()           #Read line and safe it as list seperated by tabs
                NewFrame = pd.DataFrame({ 'Run' : str(current_line[1]), #Create a new line to add to the dataframe. 
                'Activation' : str(current_line[2]),               
		        'Period' : int(current_line[3]), 
         		'Individual' : int(current_line[4]), 
	        	'Sex' : current_line[5],
	        	'Behavior' : current_line[6],
		        'Score' :  float(current_line[7]),
                'Receiver_sex': current_line[12],
	        	'X_pos' : float(current_line[9]), 
	        	'Y_pos' : float(current_line[10])},
		        index = ["F"+str(current_line[1])+'A'+str(line)])      #Create a ascession code for the line, which consists of the File it is from + the Activation that is saved.
                line = line + 1                                   #+ 1 to close the loop at the end
                sep_pieces = [MonkeyFrame, NewFrame]              #Add the new line to the existing dataframe
                MonkeyFrame = pd.concat(sep_pieces)
        MonkeyFrame = MonkeyFrame[1:]                 #Remove the junkline from the dataframe
        if G1 == 'y':                                     #Create pie chart of actions taken
            labellist = MonkeyFrame.Behavior.unique()            #Get array of possible actions
            number_of_actions = MonkeyFrame.groupby('Behavior').Activation.nunique()   #Count actions
            max_cat = len(labellist)                             #Define how many actions there are
            count = 0
            labels = 'junk '                                  #Create beginning for string list
            while count < max_cat:
                labels = labels + labellist[count] + ' '         #Create list of actions
                count = count + 1
            labels = labels.split()
            pielabels = labels[1:]
            count = 0
            list_n_actions = []
            while count < max_cat:                     #Create list with the number of taken per action
                list_n_actions.append(number_of_actions[pielabels[count]])
                count = count + 1
            fig1, pie1 = plt.subplots()
            pie1.pie(list_n_actions, labels=pielabels, autopct='%1.1f%%',shadow=True, startangle=90)    #Create a pie diagram 
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
            ste_malemale = st.stdev(malemale) / math.sqrt(len(malemale))                  #Calculate standard error of the interactions
            ste_intersex = st.stdev(intersex) / math.sqrt(len(intersex))
            ste_femalefemale = st.stdev(femalefemale) / math.sqrt(len(femalefemale))
            x_values = [mean_malemale, mean_femalefemale, mean_intersex]                 #Put means and standard error into lists
            sterror =  [ste_malemale, ste_femalefemale, ste_intersex]
            outx_values_fight_inter.append(mean_intersex)                                          #Sends data outside the loop
            outsterror_fight_inter.append(ste_intersex)
            outx_values_fight_ff.append(mean_femalefemale)                                          #Sends data outside the loop
            outsterror_fight_ff.append(ste_femalefemale)
            outx_values_fight_mm.append(mean_malemale)                                          #Sends data outside the loop
            outsterror_fight_mm.append(ste_malemale)
            fig2, bar1 = plt.subplots()
            ind = np.arange(3)
            bar1.bar(ind + 0.35, x_values, width = 0.35,color='b', yerr = sterror, ecolor='black')                       #Create barplot
            bar1.set_title('Frequency of Agression')             #Graph Titel
            bar1.set_ylabel('# of attacks')                 #Y-axis name
            bar1.set_xticks(ind + 0.54)                #Distance between the bars
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
                intersex.append(n_interactions[str(current_run), 'Groom', 'F', 'M'] + n_interactions[str(current_run),'Groom', 'M', 'F'])
                femalefemale.append(n_interactions[str(current_run), 'Groom', 'F', 'F'])
                current_run = current_run + 1
            mean_malemale = st.mean(malemale)                                             #Calculate means of the interactions
            mean_intersex = st.mean(intersex)
            mean_femalefemale = st.mean(femalefemale)
            ste_malemale = st.stdev(malemale) / math.sqrt(len(malemale))                  #Calculate standard error of the interactions
            ste_intersex = st.stdev(intersex) / math.sqrt(len(intersex))
            ste_femalefemale = st.stdev(femalefemale) / math.sqrt(len(femalefemale))
            x_values = [mean_malemale, mean_femalefemale, mean_intersex]                 #Put means and standard error into lists
            sterror =  [ste_malemale, ste_femalefemale, ste_intersex]
            outx_values_groom_inter.append(mean_intersex)                                          #Sends data outside the loop
            outsterror_groom_inter.append(ste_intersex)
            outx_values_groom_ff.append(mean_femalefemale)                                          #Sends data outside the loop
            outsterror_groom_ff.append(ste_femalefemale)
            outx_values_groom_mm.append(mean_malemale)                                          #Sends data outside the loop
            outsterror_groom_mm.append(ste_malemale)
            fig2, bar1 = plt.subplots()
            ind = np.arange(3)
            bar1.bar(ind + 0.35, x_values, width = 0.35,color='r', yerr = sterror, ecolor='black')                       #Create barplot
            bar1.set_title('Frequency of Grooming')               #Titel
            bar1.set_ylabel('# of grooms')              #Y-axis name
            bar1.set_xticks(ind + 0.54)                #Distance between the bars
            bar1.set_xticklabels(('Male-Male', 'Female-Female', 'Intersex'))
            plt.show()
            fig2.savefig(name + '_grooming_bar_chart.png')            
        if G2 == 'y':                             #Boxplot average dominance
            meandoms = MonkeyFrame.groupby(['Run']).Score.mean()     #Get Dominance score, ativation number and file number colums           
            sexdom = MonkeyFrame.loc[:,['Sex','Run','Score']]    #Get Dominance score, ativation number and file number and the sex colums
            meanfemdoms = sexdom[(sexdom.Sex == 'F')].groupby(['Run']).Score.mean()      #Sort by female and male
            meanmdoms = sexdom[(sexdom.Sex == 'M')].groupby(['Run']).Score.mean()
            mean_all_femdoms = []
            mean_all_mdoms = []
            mean_all_doms = []
            run_range = range(0, maxruns)
            for current_run in run_range:
                mean_all_femdoms.append(meanfemdoms[current_run])
                mean_all_mdoms.append(meanmdoms[current_run])
                mean_all_doms.append(meandoms[current_run])
            ste_all_doms = st.stdev(mean_all_doms) / (math.sqrt(len(mean_all_doms)))
            ste_all_femdoms = st.stdev(mean_all_doms) / (math.sqrt(len(mean_all_doms)))
            ste_all_mdoms = st.stdev(mean_all_doms) / (math.sqrt(len(mean_all_doms)))
            G2mste.append(ste_all_mdoms)
            G2mmean.append(mean_all_mdoms)
            G2allste.append(ste_all_doms)
            G2allmean.append(mean_all_doms)
            G2femste.append(ste_all_femdoms)
            G2femmean.append(mean_all_doms)
            print mean_all_doms
            print meandoms
            fig3, box1 = plt.subplots()              #Create the boxplots
            box1.boxplot((mean_all_mdoms, mean_all_femdoms, mean_all_doms), labels=('Male', 'Female', 'All Individuals'), showmeans=True, positions = ([0.5, 1.0, 1.5]))
            box1.set_title('Dominance', fontsize=10)
            plt.show()
            fig3.savefig(name + '_All_Dom_Box.png')
            ind = np.arange(3)
            fig5, bar3 = plt.subplots()
            bar3.bar(ind + 0.35, (st.mean(mean_all_mdoms), st.mean(mean_all_femdoms), st.mean(mean_all_doms)), width = 0.35,color='b', yerr = (ste_all_mdoms, ste_all_femdoms, ste_all_doms), ecolor='black')                       #Create barplot
            bar3.set_title('Mean dominance')             #Graph Titel
            bar3.set_ylabel('Dominance score')                 #Y-axis name
            bar3.set_xticks(ind + 0.54)                #Distance between the bars
            bar3.set_xticklabels(('Male', 'Female', 'All individuals'))
            plt.show()
            fig5.savefig(name + '_All_Dom_bar.png')
        if G5 == 'y':                             #Create distance to centre
            centralxy = MonkeyFrame.loc[:,['X_pos', 'Y_pos', 'Sex', 'Activation', 'Run']].rolling(window = 20).mean()   #Calculate the average X and Y position in a 20 line windows, which is a reasonable approximation of the coordinates of the central point of the group
            indixy = MonkeyFrame.loc[:,['X_pos', 'Y_pos', 'Sex', 'Activation', 'Run']].rolling(window = 1).mean()      #Contains the individual x and y positions
            sqrx = centralxy.X_pos.subtract(indixy.X_pos).abs().pow(2)             #Use rule of Pythagoras to calculate the distance between the centre and the current location of the individual and save it as zside
            sqry = centralxy.Y_pos.subtract(indixy.Y_pos).abs().pow(2)
            zside = sqrx.add(sqry)
            zside = zside.apply(np.sqrt)
            zside = zside.fillna(zside.mean())                              #Fill up the Nan with the mean, so the boxplots can be made
            distmatrix = pd.concat([zside, MonkeyFrame.loc[:,['Sex', 'Activation', 'Run']].rolling(window = 1).mean()], axis = 1) #Add distance to center as part of the array 
            mdist = distmatrix[(distmatrix.Sex == 'M')].loc[:,[0, 'Sex', 'Activation', 'Run']]                  #seperate into male and female
            femdist = distmatrix[(distmatrix.Sex == 'F')].loc[:,[0, 'Sex', 'Activation', 'Run']]
            mdistmatrix = pd.merge(mdist, femdist, how = 'left', on = ['Activation', 'Sex', 'Run'])            #Create matrixes which can be used to make boxplots
            femdistmatrix = pd.merge(femdist, mdist, how = 'left', on = ['Activation', 'Sex', 'Run'])
            alldistmatrix = pd.merge(distmatrix, femdist, how = 'left', on = ['Activation', 'Sex', 'Run'])
            alldistmatrix = alldistmatrix.loc[:,['0_x', '0_y']].as_matrix()
            femdistmatrix = femdistmatrix.loc[:,['0_x', '0_y']].as_matrix()
            mdistmatrix = mdistmatrix.loc[:,['0_x', '0_y']].as_matrix()
            alldists = []
            femdists = []
            mdists = []
            len_all = len(alldistmatrix)
            len_fem = len(femdistmatrix)
            len_m = len(mdistmatrix)
            act_range_all = range(0, len_all)
            act_range_fem = range(0, len_fem)
            act_range_m = range(0, len_m)
            for activation in act_range_all:
                tempdist = alldistmatrix[activation]
                alldists.append(tempdist[0])
            for activation in act_range_fem:
                tempdist = femdistmatrix[activation]
                femdists.append(tempdist[0])
            for activation in act_range_m:
                tempdist = mdistmatrix[activation]
                mdists.append(tempdist[0])
            G5mdists.append(mdists)
            G5femdists.append(femdists)
            G5alldists.append(alldists)
            fig4, box2 = plt.subplots()           #Somehow needs to create a second, empty boxplot to create boxplot
            box2.boxplot((mdists, femdists, alldists), labels=('Male', 'Female', 'All individuals'), showmeans=True, positions = ([0.5, 1.0, 1.5]))    
            box2.set_title('Distance from Center with outliers', fontsize=10)
            plt.show()       
            fig4.savefig(name + '_All_Dist_Box_Outlier.png')       #Due to the large divergence of outliers usually generated in here, create boxplots with outliers (above) and without (below)
            fig4, box2 = plt.subplots()
            box2.boxplot((mdists, femdists, alldists), labels=('Male', 'Female', 'All individuals'), showmeans=True, positions = ([0.5, 1.0, 1.5]), sym = '')    
            box2.set_title('Distance from Center', fontsize=10)
            plt.show()
            ind = range(3)
            fig4.savefig(name + '_All_Dist_Box.png')
         #   fig5, bar3 = plt.subplots()
         #   bar3.bar(ind + 0.35, (st.mean(mdists), st.mean(femdists), st.mean(alldists)), width = 0.35,color='b', yerr = ((st.stdev(mdists) / math.sqrt(st.mean(mdists))), (st.stdev(femdists) / math.sqrt(st.mean(femdists))), (st.stdev(alldists) / math.sqrt(st.mean(alldists)))), ecolor='black')                       #Create barplot
          #  bar3.set_title('Distance from Center')             #Graph Titel
           # bar3.set_ylabel('Distance')                 #Y-axis name
          #  bar3.set_xticks(ind + 0.54)                #Distance between the bars
          #  bar3.set_xticklabels(('Male', 'Female', 'All individuals'))
          #  plt.show()
            #fig5.savefig(name + '_All_Disy_bar.png')
        if G6 == "y":
            mean_dom = MonkeyFrame.groupby(['Run', 'Sex', 'Individual']).Score.mean()
            current_run = 1
            all_dom_steep = []
            m_dom_steep = []
            fem_dom_steep = []
            while current_run <= maxruns:                              #Create a list with the amount of fight actions taken per inputfile)
                all_m_dom =[]
                all_fem_dom = []
                for individual in m_range:
                    all_m_dom.append(mean_dom[str(current_run), 'M', individual])
                for individual in fem_range:
                    all_fem_dom.append(mean_dom[str(current_run), 'F', individual])
                all_dom = all_fem_dom + all_m_dom
                all_stdev = st.stdev(all_dom)
                all_fem_stdev = st.stdev(all_fem_dom)
                all_m_stdev = st.stdev(all_m_dom)
                dom_steep = all_stdev / st.mean(all_dom)
                mdom_steep = all_m_stdev / st.mean(all_m_dom)
                femdom_steep = all_fem_stdev / st.mean(all_fem_dom)
                all_dom_steep.append(dom_steep)
                m_dom_steep.append(mdom_steep)
                fem_dom_steep.append(femdom_steep)
                current_run = current_run + 1
            G6msteep.append(m_dom_steep)
            G6femsteep.append(fem_dom_steep)
            G6allsteep.append(all_dom_steep)
            fig5, bar3 = plt.subplots()
            ind = np.arange(3)
            bar3.bar(ind + 0.35, (st.mean(m_dom_steep), st.mean(fem_dom_steep), st.mean(all_dom_steep)), width = 0.35,color='b', yerr = (st.stdev(m_dom_steep) / math.sqrt(len(m_dom_steep)), st.stdev(fem_dom_steep) / math.sqrt(len(fem_dom_steep)), st.stdev(all_dom_steep) / math.sqrt(len(all_dom_steep))), ecolor='black')                       #Create barplot
            bar3.set_title('Steepness of the dominance hierarchy')             #Graph Titel
            bar3.set_ylabel('Steepness')                 #Y-axis name
            bar3.set_xticks(ind + 0.54)                #Distance between the bars
            bar3.set_xticklabels(('Male', 'Female', 'All individuals'))
            plt.show()
            fig5.savefig(name + '_All_Steep_bar.png')
            fig22, box4 = plt.subplots()
            box4.boxplot((m_dom_steep, fem_dom_steep, all_dom_steep), labels=('Male', 'Female', 'All individuals'), showmeans=True, positions = ([0.5, 1, 1.5]))
            box4.set_title('Steepness of the dominace hierarchy', fontsize=10)
            box4.set_ylabel('Steepness')
            plt.show()
            fig22.savefig(name + '_All_Steep_Box.png')
        if G7 == 'y':                         #Degree pf female dominacne
            doms = MonkeyFrame.groupby(['Run', 'Period', 'Individual']).Score.mean()
            current_run = 1                                  #Variables for the loop
            deg_fem_dom = []
            max_points = totfemales * totmales
            while current_run <= maxruns:
                points = 0
                for female in fem_range:
                    for male in m_range:
                        if doms[str(current_run), int(maxperiod), int(female)] >= doms[str(current_run), int(maxperiod), int(male)]:
                            points = points + 1
                dom_score = (points / float(max_points)) * 100
                deg_fem_dom.append(dom_score)
                current_run = current_run + 1
            fig6, box5 = plt.subplots()
            plt.ylim((0,100))
            G7femdom.append(deg_fem_dom)
            box5.boxplot( deg_fem_dom, showmeans=True)
            box5.set_title('Degree of female dominance', fontsize=10)
            box5.set_ylabel('% female over male dominance')
            plt.show()
            fig6.savefig(name + '_Degree_female_Dominance_Box.png')
            fig7, bar4 = plt.subplots()
            ind = np.arange(1)
            if st.mean(deg_fem_dom) != 0:
               plt.ylim((0,100))
               bar4.bar(0.35, st.mean(deg_fem_dom), width = 0.35,color='r', yerr = (st.stdev(deg_fem_dom) / math.sqrt(len(deg_fem_dom))), ecolor='black')                       #Create barplot
               bar4.set_title('Degree of female dominance')             #Graph Titel
               bar4.set_ylabel('% female over male dominance')                 #Y-axis name
               plt.show()
               fig7.savefig(name + '_Degree_female_Dominance_Bar.png')
        if G8 == 'y':
            meandoms = MonkeyFrame.groupby(['Period']).Score.mean()     #Get Dominance score, ativation number and file number colums           
            sexdom = MonkeyFrame.loc[:,['Sex','Run', 'Period','Score']]    #Get Dominance score, ativation number and file number and the sex colums
            meanfemdoms = sexdom[(sexdom.Sex == 'F')].groupby(['Period']).Score.mean()      #Sort by female and male
            meanmdoms = sexdom[(sexdom.Sex == 'M')].groupby(['Period']).Score.mean()
            stddoms = MonkeyFrame.groupby(['Period']).Score.std()
            stdfemdoms = sexdom[(sexdom.Sex == 'F')].groupby(['Period']).Score.std()    
            stdmdoms = sexdom[(sexdom.Sex == 'M')].groupby(['Period']).Score.std()
            mean_all_femdoms = []
            mean_all_mdoms = []
            mean_all_doms = []
            std_all_doms = []
            std_all_femdoms = []
            std_all_mdoms = []
            ste_all_doms = []
            ste_all_femdoms = []
            ste_all_mdoms = []
            for period in period_range:
                mean_all_femdoms.append(meanfemdoms[period])
                mean_all_mdoms.append(meanmdoms[period])
                mean_all_doms.append(meandoms[period])
                std_all_doms.append(stddoms[period])
                std_all_femdoms.append(stdfemdoms[period])
                std_all_mdoms.append(stdmdoms[period])
            G8range = range(0, (len(period_range)))
            for position in G8range:
                ste_all_doms.append(std_all_doms[position] / (math.sqrt(periodduration * totchimps)))
                ste_all_femdoms.append(std_all_femdoms[position] / (math.sqrt(periodduration * totfemales)))
                ste_all_mdoms.append(std_all_mdoms[position] / (math.sqrt(periodduration * totmales)))
            G8mste.append(ste_all_mdoms)
            G8femste.append(ste_all_femdoms)
            G8allste.append(ste_all_doms)
            G8mmean.append(mean_all_mdoms)
            G8femmean.append(mean_all_femdoms)
            G8allmean.append(mean_all_doms)
            fig8, error1 = plt.subplots()
            error1.errorbar(period_range, mean_all_doms, yerr = ste_all_doms, label = 'All individuals')
            error1.errorbar(period_range, mean_all_femdoms, yerr = ste_all_femdoms, label = 'Female')
            error1.errorbar(period_range, mean_all_mdoms, yerr = ste_all_mdoms, label = 'Male')
            error1.legend(loc='best', framealpha = 0.5)
            error1.set_title('Mean dominance over time')
            error1.set_xlabel('Period')
            error1.set_ylabel('Dominance Score')
            plt.show()
            fig8.savefig(name + '_Dominance_over_time_error.png')
        if G9 == 'y':
            mean_dom = MonkeyFrame.groupby(['Period', 'Run', 'Sex', 'Individual']).Score.mean()
            all_dom_steep_periods = []
            fem_dom_steep_periods = []
            m_dom_steep_periods = []
            all_dom_steep_periods_sterror = []
            fem_dom_steep_periods_sterror = []
            m_dom_steep_periods_sterror = []
            for period in period_range:
                current_run = 1
                all_dom_steep = []
                m_dom_steep = []
                fem_dom_steep = []
                while current_run <= maxruns:                              #Create a list with the amount of fight actions taken per inputfile)
                    all_m_dom =[]
                    all_fem_dom = []
                    for individual in m_range:
                        all_m_dom.append(mean_dom[int(period), str(current_run), 'M', individual])
                    for individual in fem_range:
                        all_fem_dom.append(mean_dom[int(period), str(current_run), 'F', individual])
                    all_dom = all_fem_dom + all_m_dom
                    all_stdev = st.stdev(all_dom)
                    all_fem_stdev = st.stdev(all_fem_dom)
                    all_m_stdev = st.stdev(all_m_dom)
                    dom_steep = all_stdev / st.mean(all_dom)
                    mdom_steep = all_m_stdev / st.mean(all_m_dom)
                    femdom_steep = all_fem_stdev / st.mean(all_fem_dom)
                    all_dom_steep.append(dom_steep)
                    m_dom_steep.append(mdom_steep)
                    fem_dom_steep.append(femdom_steep)
                    current_run = current_run + 1
                all_dom_steep_periods.append(st.mean(all_dom_steep))
                all_dom_steep_periods_sterror.append(st.stdev(all_dom_steep) / (math.sqrt(periodduration * totchimps)))
                fem_dom_steep_periods.append(st.mean(fem_dom_steep))
                fem_dom_steep_periods_sterror.append(st.stdev(fem_dom_steep) / (math.sqrt(periodduration * totfemales)))
                m_dom_steep_periods.append(st.mean(m_dom_steep))
                m_dom_steep_periods_sterror.append(st.stdev(m_dom_steep) / (math.sqrt(periodduration * totmales)))
            G9mste.append(m_dom_steep_periods)
            G9femste.append(fem_dom_steep_periods)
            G9allste.append(all_dom_steep_periods_sterror)
            G9mmean.append(m_dom_steep_periods_sterror)
            G9femmean.append(fem_dom_steep_periods_sterror)
            G9allmean.append(all_dom_steep_periods)
            fig9, error2 = plt.subplots()
            error2.errorbar(period_range, all_dom_steep_periods, yerr = all_dom_steep_periods_sterror, label = 'All individuals')
            error2.errorbar(period_range, fem_dom_steep_periods, yerr = fem_dom_steep_periods_sterror, label = 'Female')
            error2.errorbar(period_range, m_dom_steep_periods, yerr = m_dom_steep_periods_sterror, label = 'Male')
            error2.legend(loc='best', framealpha = 0.5)
            error2.set_title('Mean steepness of the dominance hierarchy over time')
            error2.set_xlabel('Period')
            error2.set_ylabel('Steepness of the dominance hierarchy')
            plt.show()
            fig9.savefig(name + '_Steepness_over_time_error.png')
        os.popen("mkdir -p Output_" + name)                  #Create a directory and put all the newly generated images and csv files into it.
        os.popen('mv ' + name + '*.csv Output_'+name)
        os.popen('mv ' + name + '*.png Output_'+name)
    os.popen("mkdir -p Comparison_Graphs")              #Create directory for comparison graphs
    allnames = allnames.split()
    print allnames
    allnames = allnames[1:]
    print allnames
    inirange = range(0, inicount)
    inirange2 = range(1, inicount * 2)
    posrange = range(15, 1001, 10)
    ind = np.arange(1,inicount + 1)
    cmap = get_cmap(inicount)
    width = 0.7 / inicount
    if G2 == 'y':
        ofig3, obox1 = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6), sharex=True)              #Create the boxplots
        for files in inirange:
            obox1[0,0].boxplot(G2allmean[files], showmeans=True, positions = [(posrange[files] / 20.0)])
            obox1[0,1].boxplot(G2mmean[files], showmeans=True,  positions = [(posrange[files] / 20.0)])
            obox1[1,0].boxplot(G2femmean[files], showmeans=True, positions = [(posrange[files] / 20.0)])
        obox1[0,0].set_title('All individual mean dominance', fontsize=10)
        obox1[0,1].set_title('Male mean dominance', fontsize=10)
        obox1[1,0].set_title('Female mean dominance', fontsize=10)
        obox1[0,0].set_ylabel('Dominance score') 
        obox1[1,0].set_ylabel('Dominance score') 
        plt.xlim(0,(posrange[inicount - 1] / 10))
        plt.show()
        ofig3.savefig('Comparison_Dom_Box.png')
     #   ofig4, obox2 = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6),sharey=True, sharex=True)              #Create the boxplots
    #    for files in inirange:
    #        obox2[0,0].boxplot(G2allmean[files], showmeans=True, positions = [(posrange[files] / 20.0)])
     #       obox2[0,1].boxplot(G2mmean[files], showmeans=True,  positions = [(posrange[files] / 20.0)])
     #       obox2[1,0].boxplot(G2femmean[files], showmeans=True, positions = [(posrange[files] / 20.0)])
    #    obox2[0,0].set_title('All individual mean dominance', fontsize=10)
     #   obox2[0,1].set_title('Male mean dominance', fontsize=10)
    #    obox2[1,0].set_title('Female mean dominance', fontsize=10)
     #   plt.xlim(0,(posrange[inicount - 1] / 15))
    #    plt.show()
    #    ofig4.savefig('Comparison_Dom_Box_shared_yaxis.png')
        ind = np.arange(3)
        ofig5, obar3 = plt.subplots()
        for files in inirange:
            obar3.bar((ind + width + (width * files)), (st.mean(G2mmean[files]), st.mean(G2femmean[files]), st.mean(G2allmean[files])), width = width,color= cmap(0.5 + files), yerr = (G2mste[files], G2femste[files], G2allste[files]), ecolor='black')                       #Create barplot
            #legend(obar3, allnames[files], loc='best', framealpha = 0.5)
        obar3.set_title('Mean dominance')             #Graph Titel
        obar3.set_ylabel('Dominance score')                 #Y-axis name
        obar3.set_xticks(ind + width * 1.5 + (width * 0.5  * files))                #Distance between the bars
        obar3.set_xticklabels(('Male', 'Female', 'All individuals'))
        plt.show()
        ofig5.savefig('Comparison_Dom_bar.png')
    if G3 == 'y':
        ind = np.arange(3)
        ofig5, obar3 = plt.subplots()
        for files in inirange:
            obar3.bar((ind + width + (width * files)), (outx_values_fight_mm[files], outx_values_fight_ff[files], outx_values_fight_inter[files]), width = width,color= cmap(0.5 + files), yerr = (outsterror_fight_mm[files], outsterror_fight_ff[files], outsterror_fight_inter[files]), ecolor='black')                       #Create barplot
        obar3.set_title('Mean number of fights between and within sexes')             #Graph Titel
        obar3.set_ylabel('# of fights')                 #Y-axis name
        obar3.set_xticks(ind + width * 1.5 + (width * 0.5  * files))                #Distance between the bars
        obar3.set_xticklabels(('Male-Male', 'Female-Female', 'Intersex'))
        plt.show()
        ofig5.savefig('Comparison_Fights_bar.png')
    if G4 == 'y':
        ind = np.arange(3)
        ofig5, obar3 = plt.subplots()
        for files in inirange:
            obar3.bar((ind + width + (width * files)), (outx_values_groom_mm[files], outx_values_groom_ff[files], outx_values_groom_inter[files]), width = width,color= cmap(0.5 + files), yerr = (outsterror_groom_mm[files], outsterror_groom_ff[files], outsterror_groom_inter[files]), ecolor='black')                       #Create barplot
        obar3.set_title('Mean number of grooms between and within sexes')             #Graph Titel
        obar3.set_ylabel('# of grooms')                 #Y-axis name
        obar3.set_xticks(ind + width * 1.5 + (width * 0.5  * files))                #Distance between the bars
        obar3.set_xticklabels(('Male-Male', 'Female-Female', 'Intersex'))
        plt.show()
        ofig5.savefig('Comparison_Grooms_bar.png')
    if G5 == 'y':
        ofig3, obox1 = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6), sharex=True)              #Create the boxplots
        for files in inirange:
            obox1[0,0].boxplot(G5alldists[files], showmeans=True, positions = [(posrange[files] / 20.0)])
            obox1[0,1].boxplot(G5mdists[files], showmeans=True,  positions = [(posrange[files] / 20.0)])
            obox1[1,0].boxplot(G5femdists[files], showmeans=True, positions = [(posrange[files] / 20.0)])
        obox1[0,0].set_title('All individuals average distance from centre', fontsize=10)
        obox1[0,1].set_title('Male average distance from centre', fontsize=10)
        obox1[1,0].set_title('Female average distance from centre', fontsize=10)
        plt.xlim(0,(posrange[inicount - 1] / 10))
        obox1[0,0].set_ylabel('Distance from centre')
        obox1[1,0].set_ylabel('Distance from centre')
        plt.show()
        ofig3.savefig('Comparison_Dist_Box_with outliers.png')
        ofig, obox = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6), sharex=True)              #Create the boxplots
        for files in inirange:
            obox[0,0].boxplot(G5alldists[files], showmeans=True, positions = [(posrange[files] / 20.0)], sym = '')
            obox[0,1].boxplot(G5mdists[files], showmeans=True,  positions = [(posrange[files] / 20.0)], sym = '')
            obox[1,0].boxplot(G5femdists[files], showmeans=True, positions = [(posrange[files] / 20.0)], sym = '')
        obox[0,0].set_title('All individuals average distance from centre', fontsize=10)
        obox[0,1].set_title('Male average distance from centre', fontsize=10)
        obox[1,0].set_title('Female average distance from centre', fontsize=10)
        plt.xlim(0,(posrange[inicount - 1] / 10))
        obox[0,0].set_ylabel('Distance from centre')
        obox[1,0].set_ylabel('Distance from centre')
        plt.show()
        ofig.savefig('Comparison_Dist_Box.png')
    if G6 == 'y':
        ofig3, obox1 = plt.subplots(nrows = 2, ncols=2, figsize=(6, 6), sharex=True)              #Create the boxplots
        for files in inirange:
            obox1[0,0].boxplot(G6allsteep[files], showmeans=True, positions = [(posrange[files] / 20.0)])
            obox1[0,1].boxplot(G6msteep[files], showmeans=True,  positions = [(posrange[files] / 20.0)])
            obox1[1,0].boxplot(G6femsteep[files], showmeans=True, positions = [(posrange[files] / 20.0)])
        obox1[0,0].set_title('All individuals average steepness of the dominance hierarchy', fontsize=10)
        obox1[0,1].set_title('Male average steepness of the dominance hierarchy', fontsize=10)
        obox1[1,0].set_title('Female average steepness of the dominance hierarchy', fontsize=10)
        plt.xlim(0,(posrange[inicount - 1] / 10))
        obox1[0,0].set_ylabel('Steepness coefficient')
        obox1[1,0].set_ylabel('Steepness coefficient')
        plt.show()
        ofig3.savefig('Comparison_Steep_Box.png') 
    if G7 == 'y':
        ofig3, obox1 = plt.subplots()              #Create the boxplots
        for files in inirange:
            obox1.boxplot(G7femdom[files], showmeans=True, positions = [(posrange[files] / 20.0)])
        obox1.set_title('Average female dominance', fontsize=10)
        obox1.set_ylabel('Female over male dominance %') 
        plt.xlim(0,(posrange[inicount - 1] / 10))
        plt.ylim((0,100))
        plt.show()
        ofig3.savefig('Comparison_FemDom_Box.png')
        ind = np.arange(3)
    #    ofig5, obar3 = plt.subplots()
    #    for files in inirange:
   #         if st.mean(G7femdom[files]) != 0:
    #            obar3.bar((ind + width + (width * files)), st.mean(G7femdom[files]), width = width,color= cmap(0.5 + files), yerr = st.stdev(G7femdom[files]) / math.sqrt(len(G7femdom[files])), ecolor='black')                       #Create barplot
     #   obar3.set_title('Mean female dominance')             #Graph Titel
    #    obar3.set_ylabel('Female over male dominance %')                 #Y-axis name
      #  obar3.set_xticks(ind + width * 1.5 + (width * 0.5  * files))                #Distance between the bars
     #   obar3.set_xticklabels(('Male', 'Female', 'All individuals'))
    #    plt.ylim((0,100))
   #     plt.show()
     #   ofig5.savefig('Comparison_FemDom_bar.png')
    if G8 == 'y':
        fig1, error1 = plt.subplots()
        fig2, error2 = plt.subplots()
        fig3, error3 = plt.subplots()
        for files in inirange:
            error1.errorbar(operiod_range[files], G8allmean[files], yerr = G8allste[files], label = allnames[files])
            error2.errorbar(operiod_range[files], G8femmean[files], yerr = G8femste[files], label = allnames[files])
            error3.errorbar(operiod_range[files], G8mmean[files], yerr = G8mste[files], label = allnames[files])
        error1.legend(loc='best', framealpha = 0.5)
        error1.set_title('Mean dominance over time')
        error1.set_xlabel('Period')
        error1.set_ylabel('Dominance Score')
        error2.legend(loc='best', framealpha = 0.5)
        error2.set_title('Mean female dominance over time')
        error2.set_xlabel('Period')
        error2.set_ylabel('Dominance Score')
        error3.legend(loc='best', framealpha = 0.5)
        error3.set_title('Mean male dominance over time')
        error3.set_xlabel('Period')
        error3.set_ylabel('Dominance Score')
        plt.show()
        fig1.savefig('Comparison_Dominance_over_time_error.png')
        fig2.savefig('Comparison_Female_Dominance_over_time_error.png')
        fig3.savefig('Comparison_Male_Dominance_over_time_error.png')
    if G9 == 'y':
        fig1, error1 = plt.subplots()
        fig2, error2 = plt.subplots()
        fig3, error3 = plt.subplots()
        for files in inirange:
            error1.errorbar(operiod_range[files], G9allmean[files], yerr = G9allste[files], label = allnames[files])
            error2.errorbar(operiod_range[files], G9femmean[files], yerr = G9femste[files], label = allnames[files])
            error3.errorbar(operiod_range[files], G9mmean[files], yerr = G9mste[files], label = allnames[files])
        error1.legend(loc='best', framealpha = 0.5)
        error1.set_title('Mean steepness of the dominance hierarchy over time')
        error1.set_xlabel('Period')
        error1.set_ylabel('Steepness coefficient')
        error2.legend(loc='best', framealpha = 0.5)
        error2.set_title('Mean female steepness of the dominance hierarchy over time')
        error2.set_xlabel('Period')
        error2.set_ylabel('Steepness coefficient')
        error3.legend(loc='best', framealpha = 0.5)
        error3.set_title('Mean male steepness of the dominance hierarchy over time')
        error3.set_xlabel('Period')
        error3.set_ylabel('Steepness coefficient')
        plt.show()
        fig1.savefig('Comparison_Steepness_over_time_error.png')
        fig2.savefig('Comparison_Female_Steepness_over_time_error.png')
        fig3.savefig('Comparison_Male_Steepness_over_time_error.png')
    os.popen('mv  *.png -p Comparison_Graphs')
    
domworld('config.ini', 'config2.ini')      #Change input by changing the names of the input files here
