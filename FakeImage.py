import numpy as np
from astropy.nddata import CCDData
from astropy.nddata import fits_ccddata_writer
import sys
import matplotlib.pyplot as plt

import PoissonGausFit as poisgaus 
from scipy.stats import rv_continuous
import scipy

from IPython.display import display
from ipywidgets import interactive_output, fixed, FloatSlider, IntSlider, HBox

def FS(name, minn, maxx, val):
    
    '''
    Generate a FloatSlider to our specifications
    '''
    
    return FloatSlider(description = name, min=minn, max=maxx, value = val, step=0.01, continuous_update=False)

def IS(name, minn, maxx, val):
    
    '''
    Generate a FloatSlider to our specifications
    '''
    
    return IntSlider(description = name, min=minn, max=maxx, value = val, continuous_update=False)

class PoissonGausDistribution(rv_continuous):
	"""docstring for PoissonGausDistribution"""
	def __init__(self, arg):
		super(PoissonGausDistribution, self).__init__()
		self.arg = arg

	def _pdf(self, x):
		return poisgaus.fGausPoisson(x, *self.arg)

	def _cdf(self, x):
		return poisgaus.fCDFGausPoisson(x, *self.arg)

	def rvs(self, size=1):
		return np.random.normal(0, self.arg[0], size=size) + self.arg[3] * np.random.poisson(self.arg[1], size=size) + self.arg[2] 

def generate_Image(sig, lam, ADU):
    '''
    Generates an image with 
    '''
    # Define parameters to draw from
    # par = [sigma, lambda, offset, ADU conv, scaling, npoiss terms]
    par = [np.random.uniform(1, 2), np.random.uniform(0, 0.7), 20, np.random.uniform(8, 12), 1, 10]
    par = [sig, lam, 20, ADU, 1, 10]
    poisGausRV = PoissonGausDistribution(par)


    # Generate data
    data = poisGausRV.rvs(size=(2000,4000))

    # Return as "CCD image"
    return CCDData(data=data, unit='adu')

def img_hist(sig, lam, ADU, binss):
    '''
    Generates a histogram of all bins on the image
    '''
    plt.figure()
    
    plt.hist((np.asarray(generate_Image(sig, lam, ADU))).flatten(), bins=binss, label = "Img histogram")
    plt.legend()
    plt.show()

def interact_Img():
    '''
    Generates sliders to play around with image parameters
    '''
    
    sig_s = FS("Sigma", 0, 7, 1.5)
    lam_s = FS("Lambda", 0, 0.9, 0.4)
    ADU_s = FS("ADU conv", 6, 14, 10)
    bin_s = IS("Bins", 5, 500, 100)
    
    display(HBox([sig_s, lam_s, ADU_s, bin_s]))
    
    return interactive_output(img_hist, {"sig" : sig_s, "lam" : lam_s, "ADU" : ADU_s, "binss" : bin_s})

