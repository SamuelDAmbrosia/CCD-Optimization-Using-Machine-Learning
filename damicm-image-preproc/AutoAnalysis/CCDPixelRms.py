### skip->skip rms

import numpy as np
from astropy.io import fits
import math
import scipy as sp


def mapSKrms(data, skips):

    # creates a 2d map of pixelRMS values

    vals = []

    avgRMS = 0
    rmsVar = 0
    pixels = len(data) * (len(data[0]) / skips)

    for row in range(len(data)):

        vals.append([])

        for col in range(0, len(data[row]), skips):

            rmsVar = 0

            for val in range(skips):

                rmsVar = rmsVar + (math.pow(data[row, col + val], 2)) / skips

            vals[row].append(math.sqrt(rmsVar))

    return str(len(vals)) + " " + str(len(vals[0]))


def toImage(image_array, fileName, Type):

    fileName = filename[: (len(fileName) - 5)]

    scipy.misc.imsave(fileName + Type + ".jpg", image_array)
