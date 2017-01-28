#############Installation
In order for Domworld.py to work, it needs to be in the same folder as cDomWorld.exe. Should you be using the example .csv files, these should also be in the same folder as Domworld.py.
Domworld.py also needs to have the following modules installed to work: os, numpy, matplotlib, glob, pandas, statistics and math.

##############How to use
Domworld.py can be started just by typing its path into the terminal (for example: ~/Downloads/Domworld.py) 
Domworld takes input in the form of config files. 2 example config.ini files with explanations of the parameters are included in the github. One or more can be loaded at the same time, using the following input format: 'config.ini' or for multiple files : 'config.ini', 'config2.ini'. To load different files, you need to change the last line in domworld.py, which calls the function. By default, the line is domworld('config.ini', 'config2.ini')

After loading the config files, the raw output data is created in the form of csv with the name specified in the config files. It is important that each config file has a different name than the others for its outputfiles. 
The csv files contains the following data for: setting (A name defined in config.ini), run(Which output file it is from), activation(which activation this is during the entire simulation), period(which period this datapoint is in, 1 period consist of a certain number of activations per individual, which is defined in the config file as setting perioddurationfactor), actor.id(Which individual is this), actor.sex(Which sex is the actor. With X females and Y males, the first X individuals are female and the last Y individuals are male), actor.behavior (What did the actor do at this point in the simulation),actor.score (Dominance or Elo score of the actor. The higher it is, the more dominant the individual is.), actor.oestrus(Is the actor in oestrus), actor.x (X-coordinate of the actor), actor.y(Y-coordinate of the actor) and receiver.id (If the actor is displaying a behavior which needs another individual (for example fighting or grooming), then this is the receiveing party.) In case there is an receiver, the same information is displayed for them: receiver.sex, receiver.behavior, receiver.score, receiver.oestrus, receiver.x and receiver.y.

The definitive output is a series of graphs done per configuration file:
A pie chart of counts of different behaviors
A boxplot of the average dominance (for all and per sex). 
A bar chart of the frequency of aggression (inter and intrasex).
A bar chart of the frequency of grooming (inter and intrasex)
A box plot of the average distance from center (for all and per sex). 
Furthermore, it also produces 2 graphs in which the bar charts of aggression and grooming of different configuration files can be easily compared. However, due to programming and time limitations, it can only compare up to 5 different configuration files and still display it in 1 graph. Any more will be left out/.
Originally, more graphs were planned, both new and comparison graphs, but due to time limititations, this is all tha is available (for now.)

#############Workflow

After starting domworld.py, the program will load the the configuration files into the domworld function. It will then ask the user which graphs they want to create. By typing in 'y', it will create the specified graph. For each configuration file, it will then do the following: 
First it will retrieve several settings from the configuration file (Periods' "+ ini +" | cut -d ' ' -f 3").read())                     #Extract some handy data from the config file. This line extracts several statistics (NumRuns, firstDataPeriod, PeriodDurationFactor, OutFileName and Number of males and females) from the configuration file and saves them as variables. These are then used to calculate the first and last datapoint of the outputfiles. Then, wine is used to load the configuration file into cDomWorld.exe and runs it. After that ,  the dataframe is set up with a junk input. The following for loop then adds the the data (Activation, Period, Individual, Sex, Behavior, Score (Dominance or Elo, depending on your settings), Receiver_sex, X_pos and Y_pos) to the previously created dataframe. After adding all the data from all the created data files, , the first junk line is removed. 
When you want the behavioral pie chart, the next if statement (G1) is used. The script will create a matrix of the taken action and and a count how many of each were taken. These are then turned into a list and used to create the pie chart.
The next if (G3) statement creates a barplot of the amount fights in and between sexes. It first reframes the matrix to get the actions per sex and opponent sex. It will then count these seperately for male-male violence, female-female violence and intersex violence. It will then calculate the mean and the standard error for each and puts them in a list. These lists are then send outside the loop and are then used to create a barplolt. 
The next if statement (G4) does exactly the same as the previous, only now it counts the amount of grooming.
For the dominance boxplots in the G2 if statement, the dataframe is first reduced to just 'Sex','Score', 'Activation' and 'Run', and then are seperated by sex. Using merge, another column is added to the frame, which due to using how = left, will feature missing data. This is needed to create the boxplot, as the boxplotfunction did not accept single column matrixes as input. In the next lines, the dataframes are reduced to just the dominance score and converted to a numpy matrix. These are then used as input for the boxplot, with the column with missing data not creating a image.
For the distance from centre boxplots in the G5 if statement, 


