#FITS Generator CCD Simulator for DAMIC-M Machine Learning
#by Pitam Mitra
#pitamm@uw.edu

import Parameters
import numpy as np 
import scipy
from astropy.io import fits
import sys
from scipy.stats import poisson


import matplotlib.pyplot as plt



#Globals
DCPerVClk = 2.0
DCPerHClk = 0.4

NoisePerSW = 0.5


#

def SimulatedDarkCurrent():
    DarkCurrentElectron = 0

    #Penalty for V-clock differences being too high
    V1Delta = np.abs(Parameters.V1[1]-Parameters.V1[0])
    V2Delta = np.abs(Parameters.V2[1]-Parameters.V2[0])
    V3Delta = np.abs(Parameters.V3[1]-Parameters.V3[0])

    DarkCurrentElectron += DCPerVClk*(V1Delta+V2Delta+V3Delta)

    #Penalty for H-clock diffences being too high

    H1Delta = np.abs(Parameters.H1[1]-Parameters.H1[0])
    H2Delta = np.abs(Parameters.H2[1]-Parameters.H2[0])
    H3Delta = np.abs(Parameters.H3[1]-Parameters.H3[0])

    DarkCurrentElectron += DCPerHClk*(H1Delta+H2Delta+H3Delta)

    DarkCurrentADU = DarkCurrentElectron*Parameters.peak_sep
    return DarkCurrentADU


def SimulatedNoisePenalty():

    NoiseElectron = 0

    SWDelta = np.abs(Parameters.SW[1]-Parameters.SW[0])
    
    NoiseElectron += NoisePerSW*SWDelta

    return NoiseElectron


def ImageSpectrum(OutFileName):

    pixel_list = np.array([],dtype=float)
    num_gen = Parameters.image_x*Parameters.image_y//(Parameters.num_peaks-1)

    #DC and Noise penalties
    SimulatedDCPenalty = SimulatedDarkCurrent()

    #poisson_pmf_electrons = poisson.pmf(np.array([0,1,2,3,4,5]),np.random.default_rng().uniform(0, 0.7))
    #print(poisson_pmf_electrons)

    for i in range(Parameters.num_peaks):
        mu = (Parameters.peak_zero-SimulatedDCPenalty)+i*Parameters.peak_sep
        sigma = Parameters.sigma_zero/np.sqrt(Parameters.NDCMS)     

        peak = np.random.default_rng().normal(mu, sigma, num_gen)  

        pixel_list = np.append(pixel_list,peak)

    
    np.random.default_rng().shuffle(pixel_list)
    pixel_list.resize(1,Parameters.image_x*Parameters.image_y)
    pixel_list.resize(Parameters.image_x,Parameters.image_y)

    #plt.imshow(pixel_list)

    #plt.hist(pixel_list,bins=100)
    #plt.plot()
    #plt.show()

    hdu = fits.PrimaryHDU(pixel_list)
    hdul = fits.HDUList([hdu])

    if OutFileName[-4:] != "fits":
        OutFileName+=".fits"
    hdul.writeto(OutFileName)



if __name__ == "__main__":

    OutFileName = sys.argv[1]
    ImageSpectrum(OutFileName)