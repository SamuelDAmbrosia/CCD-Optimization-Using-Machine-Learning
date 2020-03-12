import matplotlib.pyplot as plt
import sys
import csv
import numpy as np
import pandas as pd

args = sys.argv

def graph1D(imgcsv, setting, smin, smax, output, omin, omax):
    '''
    Generates a scatter plot showing relationship between one setting var and one output var
    '''
    
    imgdat = pd.read_csv(imgcsv)
    
    sets = []
    outs = []
    
    for i in range(len(imgdat)):
        if((smin < float(imgdat[setting][i]) < smax) and (omin < float(i) < omax)):
            sets.append(float(imgdat[setting][i]))
            outs.append(float(imgdat[output][i]))
    
    colors = 'blue'
    area = 7

    plt.scatter(sets, outs, s=area, c=colors, alpha=0.5)
    plt.title(setting + " to " + output)
    plt.xlabel(setting)
    plt.ylabel(output)
    plt.show()
    
def main(args):
    graph1D(args[1], args[2], int(args[3]), int(args[4]), args[5], int(args[6]), int(args[7]))
    
if(len(args) == 8):
    main(args)