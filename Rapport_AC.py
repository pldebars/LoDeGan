import math
import decimal
import xml.dom 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Cursor
from xml.dom.minidom import parse 
from N42 import Readn42
from termcolor import colored
import mplcursors
from divList import divList


dom1 = Readn42("CH1@DT5724B_1274_EspectrumR_run_1_20240917_180910")
dom2 = Readn42("CH2@DT5724B_1274_EspectrumR_run_1_20240917_180910")

## Sortir les coefficients de la calibration :

GetCoeffCalib = dom1.getElementsByTagName("CoefficientValues")
racineCalib = GetCoeffCalib[0]
filsCalib = racineCalib.childNodes[0]
textCalib = filsCalib.nodeValue
textCalib2 = textCalib.split()
coeffCalib=[eval(i) for i in textCalib2]
print(colored('- Calibration coefficients: ','white',attrs=['bold']))
c1=coeffCalib[1]
c2=coeffCalib[0]
print("\t", "a : ", c1, "keV/ch", "\n")
print("\t", "b : ", c2, "keV", "\n")
if (coeffCalib[0]==0 and coeffCalib[1]==1):
    print("\t", "There is no calibration for these data.", "\n")
    flag=0
else:
    flag=1
print("")


## Sortir les spectres :

GetChannelData1  = dom1.getElementsByTagName("ChannelData")
racineChannelData1 = GetChannelData1[0]
filsChannelData1   = racineChannelData1.childNodes[0]
textChannelData1 = filsChannelData1.nodeValue
textChannelData21 = textChannelData1.split() 
channelData1 = [eval(i) for i in textChannelData21]

GetChannelData2  = dom2.getElementsByTagName("ChannelData")
racineChannelData2 = GetChannelData2[0]
filsChannelData2   = racineChannelData2.childNodes[0]
textChannelData2 = filsChannelData2.nodeValue
textChannelData22 = textChannelData2.split() 
channelData2 = [eval(i) for i in textChannelData22]


x=list(range(1, len(channelData1)+1))
E=list()
for i in range(0,len(x)):
    E.append(coeffCalib[1]*x[i]+coeffCalib[0])

# print("E :")
# print(E)
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['lines.linestyle'] = '-'
plt.rcParams['axes.linewidth'] = 1.5
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#plt.yscale('log')
#plt.gca().ticklabel_format(useMathText=True)
#plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.yscale('symlog')

R = divList(channelData2,channelData1)

l=list(range(1, len(R)+1))
print(R)

fig1=plt.figure(1)
ax = plt.gca()
#ax.set(xlim=(40, 1360), ylim=(0, 15000))
plt.plot(l,R)
#plt.plot(E,channelData2, label = "Avec A-C")


font1 = {'family':'Arial','color':'black','size':25}
font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
# font2 = {'family':'serif','color':'darkred','size':15}
if (flag==1):
    plt.xlabel("Energy (keV)",fontdict = font1)
else:
    plt.xlabel("Channel number",fontdict = font1)
plt.ylabel("Counts",fontdict = font1)
#plt.title("Energy spectrum", loc = 'left',fontdict = font2)
plt.legend(loc="upper left",fontsize=15)
#cursor = Cursor(ax, color='green', linewidth=2)
mplcursors.cursor()
#plt.grid(True, which="both", ls="-")
plt.show()


