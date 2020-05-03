import sys
import os
import re
import csv
import time
from tqdm import tqdm

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "damicm-image-preproc/AutoAnalysis"))
import PixelDistribution as pd
import PixelStats as ps
import DamicImage
import constants as c
import readFits
import lmfit

#Formatting for directories and images
CCDFull = re.compile("UW\\d{4}S")
CCDDay = re.compile("\\d{4}-\\d{2}-\\d{2}")
ImgForm = re.compile("Img_\\d+.fits")

def imageToDict(filepath):
    """
    Function to get the output data from an image
    """
    
    header, data = readFits.read(filepath)
    
    reverseHistogram = (1, 0)["Avg" in filepath]
    image = DamicImage.DamicImage(data[:, :, -1], reverse=reverseHistogram)

    dictImage = {}

    ### Define name, skips, size

    dictImage['imgName'] = os.path.basename(filepath)
    dictImage['NDCMS'] = header['NDCMS']
    dictImage['NAXIS1'] = header['NAXIS1']
    dictImage['NAXIS2'] = header['NAXIS2']

    ### Define output variables

    #find image noise
    dictImage['imgNoise'] = pd.computeImageNoise(data[:, :, :-1])

    #find individual peak noise
    nSmoothing = 4 if int(header['NDCMS']) > 1 else 12 # need less agressive moving average on skipper images
    skImageNoise, skImageNoiseErr = pd.computeSkImageNoise(image, nMovingAverage=nSmoothing)
    dictImage['skNoise'] = float(skImageNoise)
    dictImage['skNoiseError'] = float(skImageNoiseErr)

    #find entropy of the average image
    dictImage['aveImgS'] = pd.imageEntropy(data[:, :, -1])

    #find rate of entropy change as a function of skips
    entropySlope, entropySlopeErr, _ = pd.imageEntropySlope(data[:, :, :-1])
    dictImage['dSdskip'] = entropySlope
    dictImage['dSdskipError'] = entropySlopeErr

    #find dark current
    
    darkCurrent, darkCurrentErr = pd.computeDarkCurrent(
        image, nMovingAverage=nSmoothing)
    dictImage['DC'] = float(darkCurrent)
    dictImage['DCError'] = float(darkCurrentErr)


    # Compute pixel noise metrics
    ntrials = 10000
    singlePixelVariance, _ = ps.singlePixelVariance(data[:, :, :-1], ntrials=ntrials)
    imageNoiseVariance, _ = ps.imageNoiseVariance(
        data[:, :, :-1], header['NDCMS'] - c.SKIPPER_OFFSET, ntrials=ntrials
    )

    #find variance of random pixels
    dictImage['pixVar'] = singlePixelVariance

    #find variance of random clusters of pixels
    dictImage['clustVar'] = imageNoiseVariance

    #find tail ratio
    dictImage['tailRatio'] = pd.computeImageTailRatio(image)

    ### Define input variables

    headervars = ['EXP', 'AMPL', 'HCKDIRN', 'VCKDIRN', 'ITGTIME', 'VIDGAIN', 'PRETIME', 'POSTIME', 'DGWIDTH', 'RGWIDTH', 'OGWIDTH', 'SWWIDTH', 'HWIDTH', 'HOWIDTH', 'VWIDTH', 'VOWIDTH', 'ONEVCKHI', 'ONEVCKLO', 'TWOVCKHI', 'TWOVCKLO', 'TGHI', 'TGLO', 'HUHI', 'HULO', 'HLHI', 'HLLO', 'RGHI', 'RGLO', 'SWLO', 'DGHI', 'DGLO', 'OGHI', 'OGLO', 'BATTR', 'VDD1', 'VDD2', 'DRAIN1', 'DRAIN2', 'VREF1', 'VREF2', 'OPG1', 'OPG2']

    for var in headervars:
        try:
            dictImage[var] = header[var]
        except:
            dictImage[var] = -1

    return dictImage
    
    
def main(directory):
    """
    Program used to generate a CSV file from every image that has been taken on a given CCD.
    It should take a file which looks like "UW1605S", for example.
    """
    #Create CSV
    with open(os.path.basename(directory) + ".csv", 'w', newline='') as csvfile:
        
        #Fields correspond to variables - name, skips, size then output variables first, then input variables
        fieldnames = ['imgName', 'NDCMS', 'NAXIS1', 'NAXIS2', 
#dictImage                      
                      'imgNoise', 'skNoise', 'skNoiseError', 'aveImgS', 'dSdskip', 'dSdskipError', 'pixVar', 'clustVar', 'tailRatio', 'DC', 'DCError',
#inputs
                      'EXP', 'AMPL', 'HCKDIRN', 'VCKDIRN', 'ITGTIME', 'VIDGAIN', 'PRETIME', 'POSTIME', 'DGWIDTH', 'RGWIDTH', 'OGWIDTH', 'SWWIDTH', 'HWIDTH', 'HOWIDTH', 'VWIDTH', 'VOWIDTH', 'ONEVCKHI', 'ONEVCKLO', 'TWOVCKHI', 'TWOVCKLO', 'TGHI', 'TGLO', 'HUHI', 'HULO', 'HLHI', 'HLLO', 'RGHI', 'RGLO', 'SWLO', 'DGHI', 'DGLO', 'OGHI', 'OGLO', 'BATTR', 'VDD1', 'VDD2', 'DRAIN1', 'DRAIN2', 'VREF1', 'VREF2', 'OPG1', 'OPG2']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        #iterate through all files in the specified directory and its subdirectories
        
        for subdir, dirs, files in os.walk(directory):
            
            print(directory)
        
            #use a progress bar for each directory being re
        
            with tqdm(total = len(files)) as pbar:

                print("Reading images from: " + str(subdir))

                for image in files:

                    filepath = subdir + os.sep + image
                    pbar.update(1)

                    try:
                        writer.writerow(imageToDict(filepath))
                    except:
                        print("Error on image: " + subdir + "/" + image)
                
    
#Check correct formatting for input directory

try:
    directory = sys.argv[1]
    if not (os.path.isdir(directory)):
        print("Cannot find directory!")
        assert(os.path.isdir(directory))
    main(sys.argv[1])
except AssertionError:
    print("Error reading directory")
except IndexError:
    print("Please input a directory")
    