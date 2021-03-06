import csv
import sys
import math
import re
from tqdm import tqdm

hasErr = re.compile("(.*)+/-(.*)")

def transformCSV(filepath, newcsv, DCscale = 1, Nscale = 1, CTscale = 1):
    
    with open(newcsv, 'w', newline='') as csvfile1:
            
        fieldnames = ['imgName', 'NDCMS', 'NAXIS1', 'NAXIS2', 
#dictImage                      
                      'imgQuality', 'imgNoise', 'skNoise', 'skNoiseError', 'aveImgS', 'dSdskip', 'dSdskipError', 'pixVar', 'clustVar', 'tailRatio', 'DC', 'DCError',
#inputs
                      'EXP', 'AMPL', 'HCKDIRN', 'VCKDIRN', 'ITGTIME', 'VIDGAIN', 'PRETIME', 'POSTIME', 'DGWIDTH', 'RGWIDTH', 'OGWIDTH', 'SWWIDTH', 'HWIDTH', 'HOWIDTH', 'VWIDTH', 'VOWIDTH', 'ONEVCKHI', 'ONEVCKLO', 'TWOVCKHI', 'TWOVCKLO', 'TGHI', 'TGLO', 'HUHI', 'HULO', 'HLHI', 'HLLO', 'RGHI', 'RGLO', 'SWLO', 'DGHI', 'DGLO', 'OGHI', 'OGLO', 'BATTR', 'VDD1', 'VDD2', 'DRAIN1', 'DRAIN2', 'VREF1', 'VREF2', 'OPG1', 'OPG2']

        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()

        with open(filepath, newline='') as csvfile2:

            imgreader = csv.DictReader(csvfile2, delimiter = ',', quotechar='|')
            
            for img in imgreader:

                newimg = {}

                keys = set(img.keys())

                for key in keys:

                    if(hasErr.match(img[key])):
                        newimg[key] = img[key].split("+/-")[0]
                        newimg[key + "Error"] = img[key].split("+/-")[1]

                    else:
                        newimg[key] = img[key]


                newimg['imgQuality'] = math.sqrt(math.pow(float(newimg['DC'])*DCscale,2) + math.pow(float(newimg['dSdskip'])*Nscale,2) + math.pow(float(newimg['skNoise'])*CTscale,2))
                writer.writerow(newimg)