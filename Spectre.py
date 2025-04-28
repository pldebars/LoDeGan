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


dom1 = Readn42("CH0@DT5724B_1274_EspectrumR_run_4_20241016_112328")

## Sortir les spectres :

GetChannelData1  = dom1.getElementsByTagName("ChannelData")
racineChannelData1 = GetChannelData1[0]
filsChannelData1   = racineChannelData1.childNodes[0]
textChannelData1 = filsChannelData1.nodeValue
textChannelData21 = textChannelData1.split() 
channelData1 = [eval(i) for i in textChannelData21]




x=list(range(1, len(channelData1)+1))


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


fig1=plt.figure(1)
ax = plt.gca()
ax.set(xlim=(0, 7500), ylim=(0, 14000))
plt.plot(x,channelData1)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))



font1 = {'family':'Arial','color':'black','size':25}
font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
# font2 = {'family':'serif','color':'darkred','size':15}


plt.xlabel("Channel number",fontdict = font1)
plt.ylabel("Counts",fontdict = font1)
# plt.title("Energy spectrum", loc = 'left',fontdict = font2)
#plt.legend(loc="upper right",fontsize=15)
#cursor = Cursor(ax, color='green', linewidth=2)
#mplcursors.cursor()
#plt.grid(True, which="both", ls="-")

plt.show()

