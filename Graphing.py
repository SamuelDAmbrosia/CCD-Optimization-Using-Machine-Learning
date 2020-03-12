import matplotlib.pyplot as plt
import sys
import csv
import numpy as np
import pandas as pd
import math

inf = math.inf

args = sys.argv

def graph1D(imgcsv, setting, output, smin=-inf, smax=inf, omin=-inf, omax=inf):
    '''
    Generates a scatter plot showing relationship between one setting var and one output var
    '''
    
    #apply constraints to data set
    imgdat = pd.read_csv(imgcsv).query('('+str(smin)+' < '+str(setting)+' < '+str(smax)+') and ('+str(omin)+' < '+str(output)+' < '+str(omax)+')')
    
    colors = 'blue'
    area = 7

    #create graph
    plt.scatter(imgdat[setting], imgdat[output], s=area, c=colors, alpha=0.5)
    plt.title(setting + " to " + output)
    plt.xlabel(setting)
    plt.ylabel(output)
    plt.show()
    
def main(args):
    graph1D(args[1], args[2], int(args[3]), int(args[4]), args[5], int(args[6]), int(args[7]))

if(args[0] == 'Graphing.py'):
    main(args)