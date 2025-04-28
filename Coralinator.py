import numpy as np
import os
os.system('cls')
#print(sys.path)
from termcolor import colored
from Spectro import applyCalib, calib, plotSpectrum, ROIselection, ROIselection2, findPeaks, areaSelection
from N42 import Readn42, printInfoRun, getCoeffCalib, getChannelData
from User import Q1, Q11, Q2, Q3, Q4, Q5, Q6, Q7, askAnalysis, printInfoPeaks, askProm, Hello, Bye, askForBounds, askForPixeIdentification
import pandas as pd

## INTRODUCTION DU CODE ##

PIXE_data = pd.read_excel('PIXE.xlsx', sheet_name = 0, index_col = (0,1))
Hello()

dom = Readn42("CH1@DT5724B_1274_EspectrumR_run_1_20240917_180910")
liveTime = printInfoRun(dom)
c0, c1, flag = getCoeffCalib(dom)

## COMMUNICATION AVEC L'UTILISATEUR ::

choice1=Q1()

## Outils nécessaire au choix interactif d'une ROI :: 

## Rectangle selector :
match choice1:
    case "0":  
       PIXE_data = pd.read_excel('PIXE.xlsx', sheet_name = 0, index_col = (0,1))
       test = [54.3, 3589.6]
       for i in range(len(test)):
        print(PIXE_data.where(PIXE_data==test[i]).dropna(how='all').dropna(axis=1))
        
     

      


    case "1":
        channelData = getChannelData(dom)
        x, E = applyCalib(c1, c0, channelData)
        fig1 = plotSpectrum(x,E, channelData, flag)

        
    case "2":
        choice11 = Q11()
        channelData = getChannelData(dom)
        x, E = applyCalib(c1, c0, channelData)
        if (choice11==1):
            fig1, ROI, A, B, sigmaA = ROIselection(x, E, channelData, flag)
            if ROI != (-1):
            ## Analyses possibles :: 
                choice2 = Q2()
                while choice2==1:          
                    choice3=Q3()
                    askAnalysis(choice3, liveTime, A, B, sigmaA)
                    choice2 = Q2()    
            else:
                print ("You didn't choose any ROI... Please, do it again and select an ROI this time!")  
        if (choice11==2):
            fig1 = plotSpectrum(x,E, channelData, flag)
            b1, b2 = askForBounds (flag)
            ROI11, A11, B11, sigmaA11 = ROIselection2(x, E, channelData, flag, b1, b2)
            ## Analyses possibles :: 
            choice2 = Q2()
            while choice2==1:          
                choice3=Q3()
                askAnalysis(choice3, liveTime, A11, B11, sigmaA11)
                choice2 = Q2()  

    case "3":
        channelData = getChannelData(dom)
        x, E = applyCalib(c1, c0, channelData)
        fig1 = plotSpectrum(x,E, channelData, flag)
        pr = 250
        choice5 = Q5()
        if (choice5 == 1):
            fig2,n, p, e, w, pmin, pmax = findPeaks(x,E, channelData, pr, c1, c0, flag)
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
            fig3, n, p, e, w, pmin, pmax  = findPeaks(x[i1:i2],E[i1:i2], channelData[i1:i2], pr, c1, c0, flag)
            printInfoPeaks (n, e, w, pmin, pmax)
            tune = Q7()
            while (tune==1):
                prom = askProm()
                fig3,n, p, e, w, pmin, pmax = findPeaks(x[i1:i2],E[i1:i2], channelData[i1:i2], prom, c1, c0, flag)
                printInfoPeaks (n, e, w, pmin, pmax)
                tune = Q7()
                fig3.clf()
            choice6 = Q6()
            if (choice6==1):
                fig3, ROI, A, B, sigmaA = ROIselection(x[i1:i2], E[i1:i2], channelData[i1:i2], flag)
                if ROI != (-1):
                    choice7=Q2()
                    ## Analyses possibles :: 
                    while choice7==1:    
                        choice3=Q3()
                        askAnalysis(choice3, liveTime, A, B, sigmaA)
                        choice7 = Q2() 
                else:
                    print ("You didn't choose any ROI... Please, do it again and select an ROI this time!")
            else:
                print ("You didn't choose any area... Please, do it again and select the right area this time!")

        Pixe = askForPixeIdentification()
        if (Pixe == 1):
            for i in range(len(e)):
                id = PIXE_data.where(PIXE_data==e[i]).dropna(how='all').dropna(axis=1)
                print(id)
        
            
choice4=Q4()

while choice4==1:
    choice8=Q1()

    match choice8:
        case "1":

            channelData = getChannelData(dom)
            x, E = applyCalib(c1, c0, channelData)
            fig1 = plotSpectrum(x,E, channelData, flag)
            
        case "2":       
            choice11 = Q11()
            channelData = getChannelData(dom)
            x, E = applyCalib(c1, c0, channelData)
            if (choice11==1):
                fig1, ROI, A, B, sigmaA = ROIselection(x, E, channelData, flag)
                if ROI != (-1):
                ## Analyses possibles :: 
                    choice2 = Q2()
                    while choice2==1:          
                        choice3=Q3()
                        askAnalysis(choice3, liveTime, A, B, sigmaA)
                        choice2 = Q2()    
                else:
                    print ("You didn't choose any ROI... Please, do it again and select an ROI this time!")  
            if (choice11==2):
                fig1 = plotSpectrum(x,E, channelData, flag)
                b1, b2 = askForBounds (flag)
                ROI11, A11, B11, sigmaA11 = ROIselection2(x, E, channelData, flag, b1, b2)
                ## Analyses possibles :: 
                choice2 = Q2()
                while choice2==1:          
                    choice3=Q3()
                    askAnalysis(choice3, liveTime, A11, B11, sigmaA11)
                    choice2 = Q2()  
        case "3":
            channelData = getChannelData(dom)
            x, E = applyCalib(c1, c0, channelData)
            fig1 = plotSpectrum(x,E, channelData, flag)
            choice5 = Q5()
            if (choice5 == 1):
                fig2,n, p, e, w, pmin, pmax = findPeaks(x,E, channelData, pr, c1, c0, flag)
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
                if i1 != (-1):
                    fig3, n, p, e, w, pmin, pmax  = findPeaks(x[i1:i2],E[i1:i2], channelData[i1:i2], 100, c1, c0, flag)
                    printInfoPeaks (n, e, w, pmin, pmax)
                    tune = Q7()
                    while (tune==1):
                        prom = askProm()
                        fig3,n, p, e, w, pmin, pmax = findPeaks(x[i1:i2],E[i1:i2], channelData[i1:i2], prom, c1, c0, flag)
                        printInfoPeaks (n, e, w, pmin, pmax)
                        tune = Q7()
                        fig3.clf()
                    choice6 = Q6()
                    if (choice6==1):
                        fig3, ROI, A, B, sigmaA = ROIselection(x[i1:i2], E[i1:i2], channelData[i1:i2], flag)
                        if ROI != (-1):
                            choice7=Q2()
                            ## Analyses possibles :: 
                            while choice7==1:    
                                choice3=Q3()
                                askAnalysis(choice3, liveTime, A, B, sigmaA)
                                choice7 = Q2() 
                        else: 
                            print ("You didn't choose any ROI... Please, do it again and select an ROI this time!")
                else:
                    print ("You didn't choose any area... Please, do it again and select the right area this time!")
    choice4= Q4() 

Bye()

