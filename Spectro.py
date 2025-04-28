import math
import decimal
import numpy as np
import matplotlib.pyplot as plt
# import pyqtgraph.ROI as ROI
#from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.widgets import RectangleSelector
from termcolor import colored
from scipy.signal import chirp, find_peaks, peak_widths, peak_prominences, find_peaks_cwt
import peakutils
import pyqtgraph as pg


def detectionLimit(B): # B bruit nombre de coups dans le bruit de fond
  
    LD = 2.71 + 4.65 * math.sqrt(B)
    print("Detection limit at 95% CL: ")
    print(decimal.Decimal(LD).quantize(decimal.Decimal('1'), rounding = decimal.ROUND_UP), "counts") 
    return LD


def detectionEfficiency(N, sigmaN, A, sigmaA, P, sigmaP, t): # N est le nombre de coups net dans le pic, t le temps d'acquisition corrigé, A l'activité de la source en Bq, P la proba d'émission du gamma étudié

    eff = N/(A*P*t)
    errEff = eff*math.sqrt((sigmaN/N)**2+(sigmaA/A)**2+(sigmaP/P)**2)
    print("Detection efficiency and its error at 95% CL: ")
    print(decimal.Decimal(eff).quantize(decimal.Decimal('.01'), rounding = decimal.ROUND_UP),"+/-", decimal.Decimal(errEff).quantize(decimal.Decimal('.000001'), rounding = decimal.ROUND_UP))
    return eff


def minimumDetectableActivity(Ld,t,eff,P):  # Ld est la limite de détection, t le temps d'acquisition corrigé, eff l'efficacité de détection du pic étudié, P la proba d'émission du gamma étudié
    
    MDA = Ld/(t*eff*P)
    print("Minimum Detectable Activity (MDA): ")
    print(decimal.Decimal(MDA).quantize(decimal.Decimal('.001'), rounding = decimal.ROUND_UP), "Bq")
    return MDA

def activity(N, sigmaN, eff, sigmaEff, P, sigmaP, t):
    A = N/(eff*P*t)
    errA = A*math.sqrt((sigmaN/N)**2+(sigmaEff/eff)**2+(sigmaP/P)**2)
    print("Activity and its error at 95% CL: ")
    print(decimal.Decimal(A).quantize(decimal.Decimal('.01'), rounding = decimal.ROUND_UP), "+/-", decimal.Decimal(errA).quantize(decimal.Decimal('.000001'), rounding = decimal.ROUND_UP),"Bq")
    return A

def applyCalib (a,b,c):
    
    ch=list(range(1, len(c)+1))
    en=list()
    for i in range(0,len(ch)):
        en.append(a*ch[i]+b)
    return ch, en

def calib (c):
    
    ch=np.array(list(range(1, len(c)+1)))
    c_array = np.array(c)
    #en=list()
    global cent1, cent2, cent3

    def line_select_callback(eclick, erelease):
        global cent1
        'eclick and erelease are the press and release events'
        print("iciicicicic:")
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("")
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
        # x1 et x2 donnent les limites en énergie de la ROI.
        # Il faut maintenant relier cela au point en énergie résultant de la calibration 
        # et trouver les indexes correspondant dans E. 
        # calculate the difference array
        difference_array1 = np.absolute(ch-x1)
        difference_array2 = np.absolute(ch-x2)
        # find the index of minimum element from the array
        index1 = difference_array1.argmin()
        index2 = difference_array2.argmin()
        index = [index1 + (math.floor((index2 - index1)/2))]
        print("index1", index1) 
        print("index2", index2) 
        print("index type", type(index)) 
        print("index", index) 

        #print("Nearest element to the given values is : ", E[index1])
        #print("Index of nearest value is : ", index1)
        #print("Nearest element to the given values is : ", E[index2])
        #print("Index of nearest value is : ", index2)
        ## Définition de variables globales, afin de pouvoir avoir accès aux différentes informations du spectre ailleurs dans le programme : 
        param = peakutils.interpolate(ch, c_array, index)
        cent1 = param[:,1]
       
    
    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector desactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)

    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.linestyle'] = '-'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.gca().ticklabel_format(useMathText=True)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.yscale('symlog')
    fig1=plt.figure(1)
    mplcursors.cursor()

    font1 = {'family':'Arial','color':'black','size':25}
    font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
    # font2 = {'family':'serif','color':'darkred','size':15}
    ax = plt.gca()
    ax.set(xlim=(ch[0], ch[-1]), ylim=(0, max(c)+max(c)/20))
    plt.xlabel("Channel number",fontdict = font1)
    plt.plot(ch,c,'tab:blue')
    plt.ylabel("Counts",fontdict = font1)
    plt.title("Energy spectrum", loc = 'left',fontdict = font2)
    print("\nclick  -->  release")
    print(colored("\nSelect a region in the spectrum. Don't hesitate to zoom before for more precision.", 'red'))
    #print(colored("If you miss the right region, you can choose a new one.", 'red'))
    print(colored("To perform an analysis of a specific peak, please select the area you want to study and close the plot to continue.", 'red'))
    # drawtype is 'box' or 'line' or 'none'
    #drawtype='none'
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    font1 = {'family':'Arial','color':'black','size':25}
    font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
    # font2 = {'family':'serif','color':'darkred','size':15}
    ax = plt.gca()
    ax.set(xlim=(ch[0], ch[-1]), ylim=(0, max(c)+max(c)/20))
    plt.xlabel("Channel number",fontdict = font1)
    plt.plot(ch,c,'tab:blue')
    plt.ylabel("Counts",fontdict = font1)
    plt.title("Energy spectrum", loc = 'left',fontdict = font2)
    print("\nclick  -->  release")
    print(colored("\nSelect a region in the spectrum. Don't hesitate to zoom before for more precision.", 'red'))
    #print(colored("If you miss the right region, you can choose a new one.", 'red'))
    print(colored("To perform an analysis of a specific peak, please select the area you want to study and close the plot to continue.", 'red'))
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    font1 = {'family':'Arial','color':'black','size':25}
    font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
    # font2 = {'family':'serif','color':'darkred','size':15}
    ax = plt.gca()
    ax.set(xlim=(ch[0], ch[-1]), ylim=(0, max(c)+max(c)/20))
    plt.xlabel("Channel number",fontdict = font1)
    plt.plot(ch,c,'tab:blue')
    plt.ylabel("Counts",fontdict = font1)
    plt.title("Energy spectrum", loc = 'left',fontdict = font2)
    print("\nclick  -->  release")
    print(colored("\nSelect a region in the spectrum. Don't hesitate to zoom before for more precision.", 'red'))
    #print(colored("If you miss the right region, you can choose a new one.", 'red'))
    print(colored("To perform an analysis of a specific peak, please select the area you want to study and close the plot to continue.", 'red'))
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
   

def plotSpectrum(ch, en, c, f):

    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.linestyle'] = '-'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.gca().ticklabel_format(useMathText=True)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.yscale('symlog')

    fig=plt.figure(1)
    ax = plt.gca()
    #mplcursors.cursor()

    font1 = {'family':'Arial','color':'black','size':25}
    font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
    # font2 = {'family':'serif','color':'darkred','size':15}
    if (f==1):
        plt.xlabel("Energy (keV)",fontdict = font1)
        plt.ylabel("Counts",fontdict = font1)
        plt.plot(en,c,'tab:blue', linestyle = 'dotted')
    else:
        plt.xlabel("Channel number",fontdict = font1)
        plt.plot(ch,c,'tab:blue')
    plt.title("Energy spectrum", fontdict = font2)
    #plt.show()
    plt.show(block=False)
    #plt.figure()
    #plt.ion()
    #plt.show()
    return fig

def ROIselection(ch, en, c, f):   
    global ROI, A, B, sigmaG, sigmaA, sigmaB
    ROI = -1
    A = -1
    B = -1
    sigmaA = -1 
    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        print("iciicicicic:")
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("")
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
        # x1 et x2 donnent les limites en énergie de la ROI.
        # Il faut maintenant relier cela au point en énergie résultant de la calibration 
        # et trouver les indexes correspondant dans E. 
        # calculate the difference array
        print(type(en))
        print(type(x1))
        difference_array1 = np.absolute(en-x1)
        difference_array2 = np.absolute(en-x2)
        # find the index of minimum element from the array
        index1 = difference_array1.argmin()
        index2 = difference_array2.argmin()
        #print("Nearest element to the given values is : ", E[index1])
        #print("Index of nearest value is : ", index1)
        #print("Nearest element to the given values is : ", E[index2])
        #print("Index of nearest value is : ", index2)
        ## Définition de variables globales, afin de pouvoir avoir accès aux différentes informations du spectre ailleurs dans le programme : 
        ## ROI et erreur :
        global ROI, A, B, sigmaG, sigmaA, sigmaB
        ROI=0
        for i in range(index1,index2):
            ROI = ROI + ch[i]
        sigmaG = 1.96*math.sqrt(ROI)
        print(colored("- Number of events in the chosen ROI and its error at 95% CL: ", 'white', attrs=['bold']))
        print("\t",ROI, "counts", "+/-", decimal.Decimal(sigmaG).quantize(decimal.Decimal('.1'), rounding = decimal.ROUND_UP), "counts")
        #print("Error: ")
        #print(sigmaG*1) 
    ## Calcul du bruit sous le pic : Simple peak integration 

        n=index2-index1
        m=5 # nombre de canaux sur lequel est évalué le bruit 
        L=0 # Lower background region
        U=0 # Upper background region
        for i in range(1,m):

            L= L + ch[index1-i]
            U = U + ch[index2+i]

        B = n*(L+U)/(2*m) # Calcul du bruit comme étant la moyenne du bruit calculé sur m canaux au-dessus et en-dessous de la région du pic sélectionné.
        sigmaB = 1.96*math.sqrt(B)
        

        A = ROI - B # Nombre de coups net après soustraction du bruit de fond.
        sigmaA = 1.96*math.sqrt(A+B*(1+(n/(2*m))))
        
        print(colored("- Background under the peak and its error at 95% CL: ", 'white', attrs=['bold']))
        print("\t",B, "counts", "+/-", decimal.Decimal(sigmaB).quantize(decimal.Decimal('.1'), rounding = decimal.ROUND_UP), "counts")
        print(colored("- Net counts in the peak and its error at 95% CL: ", 'white', attrs=['bold']))
        print("\t", decimal.Decimal(A).quantize(decimal.Decimal('.1')), "counts", "+/-", decimal.Decimal(sigmaA).quantize(decimal.Decimal('.1'), rounding = decimal.ROUND_UP), "counts") 
        
        print(colored("\nIf you want, you can select a new region in the spectrum to get the informations. Don't hesitate to zoom before for more precision.", 'red'))
        print(colored("If you want to perform analysis on a specific region, please select the area you want to study and close the plot to continue.", 'red'))
        print("")
    
    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector desactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)

    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.linestyle'] = '-'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.gca().ticklabel_format(useMathText=True)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.yscale('symlog')
    fig1=plt.figure(1)
    mplcursors.cursor()

    font1 = {'family':'Arial','color':'black','size':25}
    font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
    # font2 = {'family':'serif','color':'darkred','size':15}
    if (f==1):
        ax = plt.gca()
        ax.set(xlim=(en[0], en[-1]), ylim=(0, max(c)+max(c)/20))
        plt.xlabel("Energy (keV)",fontdict = font1)
        plt.plot(en,c,'tab:blue')
    else:
        ax = plt.gca()
        ax.set(xlim=(ch[0], ch[-1]), ylim=(0, max(c)+max(c)/20))
        plt.xlabel("Channel number",fontdict = font1)
        plt.plot(ch,c,'tab:blue')

    plt.ylabel("Counts",fontdict = font1)
    plt.title("Energy spectrum", loc = 'left',fontdict = font2)
    print("\nclick  -->  release")
    print(colored("\nSelect a region in the spectrum. Don't hesitate to zoom before for more precision.", 'red'))
    #print(colored("If you miss the right region, you can choose a new one.", 'red'))
    print(colored("To perform an analysis of a specific peak, please select the area you want to study and close the plot to continue.", 'red'))
    # drawtype is 'box' or 'line' or 'none'
    #drawtype='none'
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    #plt.show(block=False)
    #plt.figure()
    return fig1, ROI, A, B, sigmaA

def ROIselection2(ch, en, c, f, b1, b2):
        # b1 et b2 donnent les limites en énergie de la ROI.
        # Il faut maintenant relier cela au point en énergie résultant de la calibration 
        # et trouver les indexes correspondant dans E. 
        # calculate the difference array
        difference_array1 = np.absolute(en-b1)
        difference_array2 = np.absolute(en-b2)
        # find the index of minimum element from the array
        index1 = difference_array1.argmin()
        index2 = difference_array2.argmin()

        ROI=0
        for i in range(index1,index2):
            ROI = ROI + ch[i]
        sigmaG = 1.96*math.sqrt(ROI)
        print(colored("- Number of events in the chosen ROI and its error at 95% CL: ", 'white', attrs=['bold']))
        print("\t",ROI, "counts", "+/-", decimal.Decimal(sigmaG).quantize(decimal.Decimal('.1'), rounding = decimal.ROUND_UP), "counts")
    ## Calcul du bruit sous le pic : Simple peak integration 
        n=index2-index1
        m=5 # nombre de canaux sur lequel est évalué le bruit 
        L=0 # Lower background region
        U=0 # Upper background region
        for i in range(1,m):

            L= L + ch[index1-i]
            U = U + ch[index2+i]

        B = n*(L+U)/(2*m) # Calcul du bruit comme étant la moyenne du bruit calculé sur m canaux au-dessus et en-dessous de la région du pic sélectionné.
        sigmaB = 1.96*math.sqrt(B)
        
        A = ROI - B # Nombre de coups net après soustraction du bruit de fond.
        sigmaA = 1.96*math.sqrt(A+B*(1+(n/(2*m))))
        
        print(colored("- Background under the peak and its error at 95% CL: ", 'white', attrs=['bold']))
        print("\t",B, "counts", "+/-", decimal.Decimal(sigmaB).quantize(decimal.Decimal('.1'), rounding = decimal.ROUND_UP), "counts")
        print(colored("- Net counts in the peak and its error at 95% CL: ", 'white', attrs=['bold']))
        print("\t", decimal.Decimal(A).quantize(decimal.Decimal('.1')), "counts", "+/-", decimal.Decimal(sigmaA).quantize(decimal.Decimal('.1'), rounding = decimal.ROUND_UP), "counts") 
        
        print(colored("\nIf you want, you can select a new region in the spectrum to get the informations. Don't hesitate to zoom before for more precision.", 'red'))
        print(colored("If you want to perform analysis on a specific region, please select the area you want to study and close the plot to continue.", 'red'))
        print("")

        return ROI, A, B, sigmaA

def findPeaks(ch, en, c, p, a, b, f):
    peaks, _ = find_peaks(c, prominence=p, threshold = None, width=(6, 10), rel_height = 0.5) # Trouve grossièrement le centroïde des pics
    # find_peaks permet d'affiner la détection des pics en modifiant la proéminance. 
    # Cela fonctionne bien, mais pour affiner la position des entroïdes, il faut fitter une gaussienne
    # dans les pics détectés. Cela peut se faire grâce à la méthode interpolate de peakutils.
    c_array = np.array(c)
    # base = peakutils.baseline(c_array)
    params, FWHM = findCentroidesAndFWHM (en, c_array, peaks)
    cent_x = params[:,1]
    Gauss (params, en, peaks)
    FWHM_1 = peak_widths(c, peaks, rel_height=0.5)
    FWHM_2 = a*FWHM_1[0] + b
    print("Energie avec peaks:")
    print(np.array(en)[peaks])
    print("FWHM avec peaks:")
    print(FWHM_2)
    prom = peak_prominences(c,peaks)
    if len(peaks)==0:
      print('No peak finds in this area.')
      mini = []
      maxi = []
    else:
      mini = min(prom[0])
      maxi = max(prom[0])   
    plt.plot(np.array(en)[peaks], np.array(c)[peaks], "x", color='red')
    fig2= plotSpectrum(ch, en, c_array, f)
    return fig2, len(peaks), peaks, cent_x, FWHM, mini, maxi

def findCentroidesAndFWHM (en, c, peaks):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(peakutils.__file__)
    en_array = np.array(en)
    param = peakutils.interpolate(en_array, c, peaks) # Affine la position des centroïdes des pics
    FWHM = np.abs(param[:,2])*2*math.sqrt(2*math.log(2))
    print("CENTROIDES avec peakutils:")
    print(param[:,1])
    print("FWHM avec peakutils:")
    print(FWHM)
    return param, FWHM

def Gauss(params, en, p):
    n = 10
    G = list()
    # G= np.array(G)
    # G = np.empty(shape=(len(p), 2*n), dtype='object')
    #print("type G: ", type(G))
    #print("G: ", G)
    for i in range(0, len(p)):
        #try: 
        slice_ = slice(p[i]-n, p[i]+n)
        en_cut = en[slice_]
        en_vector = np.arange(en_cut[0], en_cut[-1], 0.1)
        # print("len en_vector: ", len(en_vector))
        
        mig = list()
        for k in range(0,len(en_vector)):
            #print("k: ", k)
            mig.append(peakutils.gaussian(en_vector[k], params[i,0], params[i,1], params[i,2]))

        #print("type mig: ", type(mig))
        #print("mig: ", mig)
        G.append(mig)
        #print("type G: ", type(G))
        #print("G: ", G)
        G2 = np.array(G)

        plt.plot(en_vector,G2[i,:],color='red')
        en_vector = []
        #mig.clear()
        #except:
            #print("There is a problem in the slicing.")

def areaSelection(ch, en, c, f):
    global index1, index2
    index1 = -1
    index2 = -1
    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("")
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
        # x1 et x2 donnent les limites en énergie de la ROI.
        # Il faut maintenant relier cela au point en énergie résultant de la calibration 
        # et trouver les indexes correspondant dans E. 
        # calculate the difference array
        difference_array1 = np.absolute(en-x1)
        difference_array2 = np.absolute(en-x2)
        global index1, index2
        # find the index of minimum element from the array
        index1 = difference_array1.argmin()
        index2 = difference_array2.argmin()
        #print("Nearest element to the given values is : ", E[index1])
        #print("Index of nearest value is : ", index1)
        #print("Nearest element to the given values is : ", E[index2])
        #print("Index of nearest value is : ", index2)

        ## Définition de variables globales, afin de pouvoir avoir accès aux différentes informations du spectre ailleurs dans le programme :
        
    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector desactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)

    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.linestyle'] = '-'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.gca().ticklabel_format(useMathText=True)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.yscale('symlog')
    fig3=plt.figure(1)
    ax = plt.gca()
    mplcursors.cursor()

    font1 = {'family':'Arial','color':'black','size':25}
    font2 = {'family':'Arial','color':'blue','size':30, 'fontweight':'bold'}
    # font2 = {'family':'serif','color':'darkred','size':15}
    if (f==1):
        plt.xlabel("Energy (keV)",fontdict = font1)
        plt.plot(en,c,'tab:blue')
    else:
        plt.xlabel("Channel number",fontdict = font1)
        plt.plot(ch,c,'tab:blue')

    plt.ylabel("Counts",fontdict = font1)
    plt.title("Energy spectrum", loc = 'left',fontdict = font2)
    print("\nclick  -->  release")
    print(colored("\nSelect a region in the spectrum. Don't hesitate to zoom before for more precision.", 'red'))
    print(colored("If you miss the right region, you can choose a new one.", 'red'))
    print(colored("To perform an analysis of a specific region, please select the area you want to study and close the plot to continue.", 'red'))
    # drawtype is 'box' or 'line' or 'none'
    #drawtype='none'
    toggle_selector.RS = RectangleSelector(ax, line_select_callback, useblit=True, button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    return fig3, index1, index2