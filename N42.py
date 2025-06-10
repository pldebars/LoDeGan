import math
import decimal
import xml.dom 
from xml.dom.minidom import parse 
from termcolor import colored


def Readn42(name):

    path = r"C:\Users\pldebars\OneDrive - Université de Namur\Documents\programmation\Python Scripts\LoDeGaN"
    #path = r"E:\LoDeGaN\Compass\Traitement\Python\LoDeGaN"
    pathAndName = path + "\\" + name + ".N42"
    #print(pathAndName)
    dom=parse(pathAndName)
    return dom

def printInfoRun(dom):
    
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

    return liveTime

def getCoeffCalib(dom):
     ## Sortir les coefficients de la calibration :

    GetCoeffCalib = dom.getElementsByTagName("CoefficientValues")
    racineCalib = GetCoeffCalib[0]
    filsCalib = racineCalib.childNodes[0]
    textCalib = filsCalib.nodeValue
    textCalib2 = textCalib.split()
    coeffCalib=[eval(i) for i in textCalib2]
    print(colored('- Calibration coefficients: ','white',attrs=['bold']))
    #c1=coeffCalib[1]
    #c2=coeffCalib[0]
    print("\t", "a : ", coeffCalib[1], "keV/ch", "\n")
    print("\t", "b : ", coeffCalib[0], "keV", "\n")

    if (coeffCalib[0]==0 and coeffCalib[1]==1):
        print("\t", "There is no calibration for these data.", "\n")
        flag=0
    else:
        flag=1
    return coeffCalib[0], coeffCalib[1], flag

def applyCalib (a,b,c):
    
    ch=list(range(1, len(c)+1))
    en=list()
    for i in range(0,len(ch)):
        en.append(a*ch[i]+b)
    return ch, en

def getChannelData(dom):

    ## Sortir le spectre :
    readChannelData  = dom.getElementsByTagName("ChannelData")
    racineChannelData = readChannelData[0]
    filsChannelData   = racineChannelData.childNodes[0]
    textChannelData = filsChannelData.nodeValue
    textChannelData2 = textChannelData.split() 
    C = [eval(i) for i in textChannelData2]
    return C