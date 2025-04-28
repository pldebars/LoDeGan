import math
import decimal
import xml.dom 
import numpy as np
import matplotlib.pyplot as plt
from xml.dom.minidom import parse 
import os
import os.path
from os import path
from termcolor import colored


print (colored('\n\tWELCOME to Moulinette_n42 !','red',attrs=['bold']))
print(colored('\tWritten by Dr. C. Stasser in 2024','red',attrs=['bold']))
print(colored('\tThis program makes possible to concvert n.42 spectrum data file to .txt data file. \n\n','red',attrs=['bold']))

#dom=parse(r"C:\Users\Coraline\Documents\Python\LoDeGaN\file.N42")
dom=parse(r"C:\Users\Coraline\Documents\Python\LoDeGaN\CH0@DT5724B_1274_EspectrumR_run_2_20240130_151517.N42")

## Sortir le nombre de coups :
GetChannelData  = dom.getElementsByTagName("ChannelData")
racineChannelData = GetChannelData[0]
filsChannelData   = racineChannelData.childNodes[0]
textChannelData = filsChannelData.nodeValue
textChannelData2 = textChannelData.split() 
channelData = [eval(i) for i in textChannelData2]

## Numéro des canaux :

x=list(range(1, len(channelData)+1))


## Écrire les données dans un fichier .txt : 

flag = path.exists(r"C:\Users\Coraline\Documents\Python\LoDeGaN\data.txt")

if flag==True:

    os.remove(r"C:\Users\Coraline\Documents\Python\LoDeGaN\data.txt")

fichier = open(r"C:\Users\Coraline\Documents\Python\LoDeGaN\data.txt", "x")

for i in range(0,len(x)):
    fichier.write(str(x[i]))
    fichier.write('\t')
    fichier.write(str(channelData[i]))
    fichier.write('\n')
    #fichier.write("\n")

fichier.close() 


