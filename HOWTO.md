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

####################

