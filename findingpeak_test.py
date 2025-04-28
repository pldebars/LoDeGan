import math
import decimal
import xml.dom 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from xml.dom.minidom import parse 
from termcolor import colored
from Spectro import detectionLimit, detectionEfficiency, minimumDetectableActivity, activity
from scipy.signal import chirp, find_peaks, peak_widths

## INTRODUCTION DU CODE ##

print(colored('\nWELCOME!','red',attrs=['bold']))
print(colored('Written by Dr. C. Stasser in 2024','red',attrs=['bold']))
print(colored('This code makes possible to get acquisition information from a n.42 data file and perform different analysis.\n\n','red',attrs=['bold']))
print(colored('Possible analysis to perform:\n','red',attrs=['bold']))
print(colored('- ROI interactive selection, ','red',attrs=['bold']))
print(colored('- Background estimation and subtraction, ','red',attrs=['bold']))
print(colored('- Detection efficiency calculation, ','red',attrs=['bold']))
print(colored('- Detection limit calculation, ','red',attrs=['bold']))
print(colored('- Minimal Detectable Activity calculation, ','red',attrs=['bold']))
print(colored('- Activity calculation. \n\n','red',attrs=['bold']))


## Lecture du fichier n.42 :: 

# dom=parse(r"C:\Users\Coraline\Documents\Python\LoDeGaN\file.N42")
#dom=parse(r"C:\Users\Coraline\Documents\Python\LoDeGaN\CH0@DT5724B_1274_EspectrumR_run_2_20240130_151517.N42")
#dom=parse(r"C:\Users\Coraline\Documents\Python\LoDeGaN\CH1@DT5724_164_EspectrumR_run_2_20220315_155543.N42")


dom=parse(r"C:\Users\cstasser\Documents\LoDeGaN\Compass\Traitement\Python\LoDeGaN\CH0@DT5724B_1274_EspectrumR_run_20240911_103928.N42")

print(colored('Information about the acquisition: \n','white',attrs=['bold']))

## Sortir le modèle du digitizer :

GetDigitizerModel = dom.getElementsByTagName("RadInstrumentModelName")
racineDigitizerModel = GetDigitizerModel[0]
filsDigitizerModel = racineDigitizerModel.childNodes[0]
DigitizerModel = filsDigitizerModel.nodeValue
print(colored('- Digitizer model: ','white',attrs=['bold']))
print("\t", DigitizerModel, "\n")

## Sortir le temps d'acquisition (real time) :

GetRealTime = dom.getElementsByTagName("RealTimeDuration")
racineRealTime = GetRealTime[0]
filsRealTime = racineRealTime.childNodes[0]
RealTime = filsRealTime.nodeValue
RealTime = RealTime.split('.')[1]
realTime = ""
for c in RealTime:
    if c.isdigit():
        realTime = realTime + c

realTime = float(realTime)

print(colored('- Real time: ','white',attrs=['bold']))
print("\t", realTime, "s", "\n")




## Sortir le temps temps d'acquisition corrigé (live time) :

GetLiveTime = dom.getElementsByTagName("LiveTimeDuration")
racineLiveTime = GetLiveTime[0]
filsLiveTime = racineLiveTime.childNodes[0]
LiveTime = filsLiveTime.nodeValue
LiveTime = LiveTime.split('.')[1]
liveTime = ""
for c in LiveTime:
    if c.isdigit():
        liveTime = liveTime + c

liveTime = float(liveTime)
print(colored('- Live time: ','white',attrs=['bold']))
print("\t", liveTime, "s", "\n")

## Sortir les coefficients de la calibration :

GetCoeffCalib = dom.getElementsByTagName("CoefficientValues")
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

## COMMUNICATION AVEC L'UTILISATEUR ::



## Outils nécessaire au choix interactif d'une ROI :: 

## Rectangle selector :



## Sortir le spectre :
GetChannelData  = dom.getElementsByTagName("ChannelData")
racineChannelData = GetChannelData[0]
filsChannelData   = racineChannelData.childNodes[0]
textChannelData = filsChannelData.nodeValue
textChannelData2 = textChannelData.split() 
channelData = [eval(i) for i in textChannelData2]


x=list(range(1, len(channelData)+1))
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
plt.gca().ticklabel_format(useMathText=True)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.yscale('symlog')


fig1=plt.figure(1)
ax = plt.gca()
plt.plot(E,channelData)


font1 = {'family':'Arial','color':'black','size':25}
font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
# font2 = {'family':'serif','color':'darkred','size':15}
if (flag==1):
    plt.xlabel("Energy (keV)",fontdict = font1)
else:
    plt.xlabel("Channel number",fontdict = font1)
plt.title("Energy spectrum", loc = 'left',fontdict = font2)

peaks, _ = find_peaks(channelData, prominence=3000)
plt.plot(np.array(E)[peaks], np.array(channelData)[peaks], "x")
a = peak_widths(channelData, peaks, rel_height=0.5)
print(peaks)
print(a)

FWHM = coeffCalib[1]*a[0] + coeffCalib[0] # a[0] because the output of peak_widths function is four areas, and the first one -  element - is the area of the width. The three other output give information about how these widths are calculated.
print('Full width at half maximum of each peak::')
print(FWHM, 'keV')

plt.show()

