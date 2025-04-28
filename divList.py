import math
import decimal
import xml.dom 
import numpy as np

def divList(list1,list2): 

    
    if (len(list1) == len(list2)):
       
        r=list()
        print(len(list1))
        for i in range(0,len(list1)):
           
            if (list2[i]==0):
                continue
            else:
                r.append(list1[i]/list2[i])
               
        return r
       
    else: 

        print("Error! The two lists must have the same size!")
        quit ()
         
    
