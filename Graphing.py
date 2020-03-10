import matplotlib.pyplot as plt
import sys
import csv
import numpy as np

args = sys.argv

def graph1D(imgcsv, setting, smin, smax, output, omin, omax):
    '''
    Generates a scatter plot showing relationship between one setting var and one output var
    '''
    
    sets = []
    outs = []
    
    with open(imgcsv, newline='') as csvfile:
        imgreader = csv.DictReader(csvfile, delimiter = ',', quotechar='|')
        for img in imgreader:
            
            #for key in img
            
            if((smin < float(img[str(setting)]) < smax) and (smin < float(img[str(output)]) < omax)):
                sets.append(float(img[str(setting)]))
                outs.append(float(img[str(output)]))
    
    colors = 'blue'
    area = 7

    plt.scatter(sets, outs, s=area, c=colors, alpha=0.5)
    plt.title(setting + " to " + output)
    plt.xlabel(setting)
    plt.ylabel(output)
    plt.show()
    
def main(args):
    graph1D(args[1], args[2], int(args[3]), int(args[4]), args[5], int(args[6]), int(args[7]))
    
print(args)
    
if(len(args) == 8):
    main(args)