import numpy as np
from termcolor import colored
from Spectro import detectionLimit, detectionEfficiency, minimumDetectableActivity, activity

def Hello():
    print(colored('\nWELCOME!','red',attrs=['bold']))
    print(colored('Written by Dr. C. Stasser in 2024','red',attrs=['bold']))
    print(colored('This code makes possible to get acquisition information from a n.42 data file and perform different analysis.\n\n','red',attrs=['bold']))
    print(colored('Possible analysis to perform:\n','red',attrs=['bold']))
    print(colored('- Automatic peak detection, ','red',attrs=['bold']))
    print(colored('- ROI interactive selection, ','red',attrs=['bold']))
    print(colored('- Background estimation and subtraction, ','red',attrs=['bold']))
    print(colored('- Detection efficiency calculation, ','red',attrs=['bold']))
    print(colored('- Detection limit calculation, ','red',attrs=['bold']))
    print(colored('- Minimal Detectable Activity calculation, ','red',attrs=['bold']))
    print(colored('- Activity calculation. \n\n','red',attrs=['bold']))

def Bye():
    print(colored('Thank you for using this program! See you soon! \n\n','red',attrs=['bold'])) 

def Q1():

    Q = input(colored('Press "1" to draw the data spectrum, "2" to draw the data spectrum and activate the ROI selection, "3" to use the automatic detection peak algorithm: \n\n','red',attrs=['bold']))

    return Q

def Q11():

    Q = int(input(colored('Press "1" to activate the ROI interactive selection and "2" to enter the manually the ROI bounds: \n\n','red',attrs=['bold'])))

    return Q

def Q2():

    Q = int(input(colored('Do you want to perform a particular analysis on this peak? Press "1" for yes and "2" for no: \n\n','red',attrs=['bold'])))

    return Q

def Q3():

    Q = input(colored('Press "1" for detection efficiency calculation, "2" for detection limit calculation, "3" for Minimal Detectable Activity calculation or "4" for activity calculation: \n\n','red',attrs=['bold']))

    return Q

def Q4():

    Q = int(input(colored('Do you want to continue? Press "1" for yes and "2" to quit the program: \n\n','red',attrs=['bold'])))

    return Q

def Q5():

    Q = int(input(colored('Here is the spectrum to study. Do you want to detect the peaks in all the spectrum (press "1") or select a specific region (press "2")?: \n\n','red',attrs=['bold'])))

    return Q

def Q6():

    Q = int(input(colored('Press "1" to activate the ROI interactive selection to perform peak analysis and "2" for no: \n\n','red',attrs=['bold'])))
    return Q
  
def Q7():

    Q = int(input(colored('Do you want to tune the prominence of the detected peaks? The minimal and maximal prominences are displayed above. Press "1" for yes and "2" for no: \n\n','red',attrs=['bold'])))
    return Q

def askProm():

    Q1 = float(input(colored('Enter the desired minimal prominence: \n\n','red',attrs=['bold'])))
    Q2 = float(input(colored('Enter the desired maximal prominence: \n\n','red',attrs=['bold'])))
    return Q1, Q2

def printInfoPeaks (numb, en, width, minProm, maxProm):
    print(colored('Number of detected peak::','white', attrs=['bold']))
    print(numb, 'peaks')
    print(colored('Peaks'' energies::','white', attrs=['bold']))
    print(en, 'keV')
    print(colored('Full width at half maximum of each peak::', 'white', attrs=['bold']))
    print(width, 'keV')
    print(colored('The minimum and maximum prominences of detected peaks are::', 'white', attrs=['bold']))
    print(minProm,'counts and', maxProm, 'counts')

def askAnalysis(ans, liveTime, A, B, sigmaA):
    match ans:
        case "1":
            a = float(input(colored('Enter the source activity in Bq:  \n\n','white',attrs=['bold'])))
            sigmaAct = float(input(colored('Enter the uncertainty of the source activity. If you don''t know it, enter 0: \n\n','white',attrs=['bold'])))
            p = float(input(colored('Enter the branching ratio of the gamma rays of interest:  \n\n','white',attrs=['bold'])))
            sigmaP = float(input(colored('Enter the uncertainty of the branching ratio. If you don''t know it, enter 0: \n\n','white',attrs=['bold'])))
            eff = detectionEfficiency(A, sigmaA, a, sigmaAct, p, sigmaP, liveTime)


        case "2":
            detLimit = detectionLimit(B)


        case "3":
            detLimit = detectionLimit(B)
            p = float(input(colored('Enter the branching ratio in percent of the gamma rays of interest:  \n\n','white',attrs=['bold'])))
            eff = float(input(colored('Enter the detection efficiency of the gamma rays of interest in the experiment geometry:  \n\n','white',attrs=['bold'])))
            minDetAct = minimumDetectableActivity(detLimit, liveTime,eff,p)


        case "4":
            p = float(input(colored('Enter the branching ratio of the gamma rays of interest:  \n\n','white',attrs=['bold'])))
            sigmaP = float(input(colored('Enter the uncertainty of the branching ratio. If you don''t know it, enter 0: \n\n','white',attrs=['bold'])))
            eff = float(input(colored('Enter the detection efficiency of the gamma rays of interest in the experiment geometry:  \n\n','white',attrs=['bold'])))
            sigmaEff = float(input(colored('Enter the uncertainty of the detection efficiency. If you don''t know it, enter 0: \n\n','white',attrs=['bold'])))
            act = activity(A, sigmaA, eff, sigmaEff, p, sigmaP, liveTime)

def askForBounds (f):

    if (f==1):
        e1=0
        e2=0
        while(e1>=e2):
            e1 = np.float64(input(colored('Enter the lower bound in keV:  \n\n','white',attrs=['bold'])))
            e2 = np.float64(input(colored('Enter the upper bound in keV:  \n\n','white',attrs=['bold'])))
            if (e1>=e2):
                print("Please, enter plausible ROI bounds!")
        return e1, e2
    else:
        x1=0
        x2=0
        while(x1>=x2):
            x1 = np.float64(input(colored('Enter the lower bound in channel''s number  \n\n','white',attrs=['bold'])))
            x2 = np.float64(input(colored('Enter the upper bound in channel''s number:  \n\n','white',attrs=['bold'])))
            if (x1>=x2):
                print("Please, enter plausible ROI bounds!")
        return x1, x2

def askForPixeIdentification():
    Q = int(input(colored('Do you want to perform PIXE identification of the detected peaks? Press "1" for yes, "2" for no: \n\n','red',attrs=['bold'])))
    return Q
