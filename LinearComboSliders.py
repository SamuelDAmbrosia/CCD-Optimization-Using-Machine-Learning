import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from ipywidgets import interactive_output, fixed, FloatSlider, HBox

def FS(name):
    
    '''
    Generate a FloatSlider to our specifications
    '''
    
    return FloatSlider(description = name, min=-1, max=1, value = 0, step=0.01, continuous_update=False)

def generate_combo(imgdf, VCKDIRN, ITGTIME, VIDGAIN, PRETIME, POSTIME, DGWIDTH, RGWIDTH, OGWIDTH, SWWIDTH, HWIDTH, HOWIDTH, VWIDTH, VOWIDTH, ONEVKHI, ONEVKLO, TWOVKHI, TWOVKLO, TGHI, TGLO, HUHI, HULO, HLHI, HLLO, RGHI, RGLO, SWLO, DGHI, DGLO, OGHI, OGLO, BATTR, VDD1, VDD2, DRAIN1, DRAIN2, VREF1, VREF2, OPG1, OPG2):
    '''
    Generates a chart showing correlation between image quality metrics and the specified combination of settings
    '''
    
    #Generate an array containing the specified linear combination for each image
    
    comboarr = [VCKDIRN*imgdf['VCKDIRN'][i] + ITGTIME*imgdf['ITGTIME'][i] + VIDGAIN*imgdf['VIDGAIN'][i] + PRETIME*imgdf['PRETIME'][i] + POSTIME*imgdf['POSTIME'][i] + DGWIDTH*imgdf['DGWIDTH'][i] + RGWIDTH*imgdf['RGWIDTH'][i] + OGWIDTH*imgdf['OGWIDTH'][i] + SWWIDTH*imgdf['SWWIDTH'][i] + HWIDTH*imgdf['HWIDTH'][i]  + HOWIDTH*imgdf['HOWIDTH'][i] + VWIDTH*imgdf['VWIDTH'][i]  + VOWIDTH*imgdf['VOWIDTH'][i] + ONEVKHI*imgdf['ONEVCKHI'][i] + ONEVKLO*imgdf['ONEVCKLO'][i] + TWOVKHI*imgdf['TWOVCKHI'][i] + TWOVKLO*imgdf['TWOVCKLO'][i] + TGHI*imgdf['TGHI'][i]    + TGLO*imgdf['TGLO'][i]    + HUHI*imgdf['HUHI'][i]    + HULO*imgdf['HULO'][i]    + HLHI*imgdf['HLHI'][i]    + HLLO*imgdf['HLLO'][i]    + RGHI*imgdf['RGHI'][i]    + RGLO*imgdf['RGLO'][i]    + SWLO*imgdf['SWLO'][i]    + DGHI*imgdf['DGHI'][i]    + DGLO*imgdf['DGLO'][i]    + OGHI*imgdf['OGHI'][i]    + OGLO*imgdf['OGLO'][i]    + BATTR*imgdf['BATTR'][i]   + VDD1*imgdf['VDD1'][i]    + VDD2*imgdf['VDD2'][i]    + DRAIN1*imgdf['DRAIN1'][i]  + DRAIN2*imgdf['DRAIN2'][i]  + VREF1*imgdf['VREF1'][i]   + VREF2*imgdf['VREF2'][i]   + OPG1*imgdf['OPG1'][i]    + OPG2*imgdf['OPG2'][i] for i in range(len(imgdf))]
    
    #Create arrays of the output variables
    
    DCarr = imgdf['DC']
    CTarr = imgdf['dSdskip']
    SNarr = imgdf['skNoise']
    INarr = imgdf['imgNoise']
    
    #Generate correlation matrix from a dataframe for the linear combos and the output variables
    
    corr = pd.DataFrame(np.array([comboarr, SNarr, INarr, CTarr, DCarr]).transpose(), columns = ['combo', 'skNoise', 'imgNoise', 'dSdskip', 'DC']).corr()
    
    #specify how the plot should look
    
    sns.set(style = 'white')
    
    f, ax = plt.subplots(figsize=(11, 9))
    
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    mask = np.triu(np.ones_like(corr, dtype=np.bool))
    
    sns.heatmap(corr,cmap = cmap, mask = mask, annot=True, vmin=-1, vmax=1,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
def interact_combo(imgdf):
    
    '''
    Creates an interactive set of sliders to play around with different combos
    '''
    
    #generate floatsliders
    
    VCKDIRN_s = FS('VCKDIRN')
    ITGTIME_s = FS('ITGTIME')
    VIDGAIN_s = FS('VIDGAIN')
    PRETIME_s = FS('PRETIME')
    POSTIME_s = FS('POSTIME')
    DGWIDTH_s = FS('DGWIDTH')
    RGWIDTH_s = FS('RGWIDTH')
    OGWIDTH_s = FS('OGWIDTH')
    SWWIDTH_s = FS('SWWIDTH')
    HWIDTH_s = FS('HWIDTH')
    HOWIDTH_s = FS('HOWIDTH')
    VWIDTH_s = FS('VWIDTH')
    VOWIDTH_s = FS('VOWIDTH')
    ONEVKHI_s = FS('ONEVKHI')
    ONEVKLO_s = FS('ONEVKLO')
    TWOVKHI_s = FS('TWOVKHI')
    TWOVKLO_s = FS('TWOVKLO')
    TGHI_s = FS('TGHI')
    TGLO_s = FS('TGLO')
    HUHI_s = FS('HUHI')
    HULO_s = FS('HULO')
    HLHI_s = FS('HLHI')
    HLLO_s = FS('HLLO')
    RGHI_s = FS('RGHI')
    RGLO_s = FS('RGLO')
    SWLO_s = FS('SWLO')
    DGHI_s = FS('DGHI')
    DGLO_s = FS('DGLO')
    OGHI_s = FS('OGHI')
    OGLO_s = FS('OGLO')
    BATTR_s = FS('BATTR')
    VDD1_s = FS('VDD1')
    VDD2_s = FS('VDD2')
    DRAIN1_s = FS('DRAIN1')
    DRAIN2_s = FS('DRAIN2')
    VREF1_s = FS('VREF1')
    VREF2_s = FS('VREF2')
    OPG1_s = FS('OPG1')
    OPG2_s = FS('OPG2')
    
    #arrange in rows of 3
    
    display(HBox([VCKDIRN_s, ITGTIME_s, VIDGAIN_s]))
    display(HBox([PRETIME_s, POSTIME_s, DGWIDTH_s]))
    display(HBox([RGWIDTH_s, OGWIDTH_s, SWWIDTH_s]))
    display(HBox([HWIDTH_s, HOWIDTH_s, VWIDTH_s]))
    display(HBox([VOWIDTH_s, ONEVKHI_s, ONEVKLO_s]))
    display(HBox([TWOVKHI_s, TWOVKLO_s, TGHI_s]))
    display(HBox([TGLO_s, HUHI_s, HULO_s]))
    display(HBox([HLHI_s, HLLO_s, RGHI_s]))
    display(HBox([RGLO_s, SWLO_s, DGHI_s]))
    display(HBox([DGLO_s, OGHI_s, OGLO_s]))
    display(HBox([BATTR_s, VDD1_s, VDD2_s]))
    display(HBox([DRAIN1_s, DRAIN2_s, VREF1_s]))
    display(HBox([VREF2_s, OPG1_s, OPG2_s]))

    #generate output
    
    return interactive_output(generate_combo, {'imgdf' : fixed(imgdf),'VCKDIRN' : VCKDIRN_s, 'ITGTIME' : ITGTIME_s, 'VIDGAIN' : VIDGAIN_s, 'PRETIME' : PRETIME_s, 'POSTIME' : POSTIME_s, 'DGWIDTH' : DGWIDTH_s, 'RGWIDTH' : RGWIDTH_s, 'OGWIDTH' : OGWIDTH_s, 'SWWIDTH' : SWWIDTH_s, 'HWIDTH' : HWIDTH_s, 'HOWIDTH' : HOWIDTH_s, 'VWIDTH' : VWIDTH_s, 'VOWIDTH' : VOWIDTH_s, 'ONEVKHI' : ONEVKHI_s, 'ONEVKLO' : ONEVKLO_s, 'TWOVKHI' : TWOVKHI_s, 'TWOVKLO' : TWOVKLO_s, 'TGHI' : TGHI_s, 'TGLO' : TGLO_s, 'HUHI' : HUHI_s, 'HULO' : HULO_s, 'HLHI' : HLHI_s, 'HLLO' : HLLO_s, 'RGHI' : RGHI_s, 'RGLO' : RGLO_s, 'SWLO' : SWLO_s, 'DGHI' : DGHI_s, 'DGLO' : DGLO_s, 'OGHI' : OGHI_s, 'OGLO' : OGLO_s, 'BATTR' : BATTR_s, 'VDD1' : VDD1_s, 'VDD2' : VDD2_s, 'DRAIN1' : DRAIN1_s, 'DRAIN2' : DRAIN2_s, 'VREF1' : VREF1_s, 'VREF2' : VREF2_s, 'OPG1' : OPG1_s, 'OPG2' : OPG2_s})
    
    
    