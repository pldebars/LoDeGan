import numpy as np
from termcolor import colored
from Spectro import detectionLimit, detectionEfficiency, minimumDetectableActivity, activity, applyCalib, plotSpectrum, ROIselection, findPeaks, areaSelection
from N42 import Readn42, printInfoRun, getCoeffCalib, GetChannelData
from User import Q1, Q2, Q3, Q4, Q5, Q6, Q7, askAnalysis, printInfoPeaks, askProm, Hello, Bye

## INTRODUCTION DU CODE ##

Hello()

dom = Readn42("CH1@DT5724B_1274_EspectrumR_run_1_20240917_180910")
liveTime = printInfoRun(dom)
c0, c1, flag = getCoeffCalib(dom)

## COMMUNICATION AVEC L'UTILISATEUR ::

choice1=Q1()

## Outils nécessaire au choix interactif d'une ROI :: 

## Rectangle selector :
match choice1:
    case "1":

        channelData = GetChannelData(dom)
        x, E = applyCalib(c1, c0, channelData)
        fig1 = plotSpectrum(x,E, channelData, flag)
        
    case "2":
       
        channelData = GetChannelData(dom)
        x, E = applyCalib(c1, c0, channelData)
        fig1, ROI, A, B, sigmaA = ROIselection(x, E, channelData, flag)
        ## Analyses possibles :: 
        choice2 = Q2()
        while choice2==1:          
            choice3=Q3()
            askAnalysis(choice3, liveTime, A, B, sigmaA)
            choice2 = Q2()    
          
    case "3":
        channelData = GetChannelData(dom)
        x, E = applyCalib(c1, c0, channelData)
        fig1 = plotSpectrum(x,E, channelData, flag)
        choice5 = Q5()
        if (choice5 == 1):
            fig2,n, p, e, w, pmin, pmax = findPeaks(x,E, channelData, 800, c1, c0, flag)
            printInfoPeaks (n, e, w, pmin, pmax)
            tune = Q7()
            while (tune==1):
                fig2.clf()
                prom = askProm()
                fig2,n, p, e, w, pmin, pmax = findPeaks(x,E, channelData, prom, c1, c0, flag)
                printInfoPeaks (n, e, w, pmin, pmax)
                tune = Q7()

         
        else:
            fig2, i1, i2 = areaSelection(x, E, channelData, flag)
            fig3, n, p, e, w, pmin, pmax  = findPeaks(x[i1:i2],E[i1:i2], channelData[i1:i2], 800, c1, c0, flag)
            printInfoPeaks (n, e, w, pmin, pmax)
            choice6 = Q6()
            if (choice6==1):
                fig3, ROI, A, B, sigmaA = ROIselection(x[i1:i2], E[i1:i2], channelData[i1:i2], flag)
                choice7=Q2()
                ## Analyses possibles :: 
                while choice7==1:    
                    choice3=Q3()
                    askAnalysis(choice3, liveTime, A, B, sigmaA)
                    choice7 = Q2() 

choice4=Q4()

while choice4==1:
    choice8=Q1()

    match choice8:
        case "1":

            channelData = GetChannelData(dom)
            x, E = applyCalib(c1, c0, channelData)
            fig1 = plotSpectrum(x,E, channelData, flag)
            
        case "2":
        
            channelData = GetChannelData(dom)
            x, E = applyCalib(c1, c0, channelData)
            fig1, ROI, A, B, sigmaA = ROIselection(x, E, channelData, flag)
            ## Analyses possibles :: 
            choice2 = Q2()
            while choice2==1:          
                choice3=Q3()
                askAnalysis(choice3, liveTime, A, B, sigmaA)
                choice2 = Q2()    
            
        case "3":
            channelData = GetChannelData(dom)
            x, E = applyCalib(c1, c0, channelData)
            fig1 = plotSpectrum(x,E, channelData, flag)
            choice5 = Q5()
            if (choice5 == 1):
                fig2,n, p, e, w, pmin, pmax = findPeaks(x,E, channelData, 800, c1, c0, flag)
                printInfoPeaks (n, e, w, pmin, pmax)
            else:
                fig2, i1, i2 = areaSelection(x, E, channelData, flag)
                fig3, n, p, e, w, pmin, pmax  = findPeaks(x[i1:i2],E[i1:i2], channelData[i1:i2], 800, c1, c0, flag)
                printInfoPeaks (n, e, w, pmin, pmax)
                choice6 = Q6()
                if (choice6==1):
                    fig3, ROI, A, B, sigmaA = ROIselection(x[i1:i2], E[i1:i2], channelData[i1:i2], flag)
                    choice7=Q2()
                    ## Analyses possibles :: 
                    while choice7==1:    
                        choice3=Q3()
                        askAnalysis(choice3, liveTime, A, B, sigmaA)
                        choice7 = Q2() 

    choice4= Q4() 

Bye()

