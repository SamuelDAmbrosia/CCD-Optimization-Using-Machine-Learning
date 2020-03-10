### Automatically analyzes CCD images
### Reads a FITS file and returns
### st.deviation and
### skip->skip rms

import sys
import numpy as np
from astropy.io import fits
import math

import CCDPixelRms as RMS
import PixelValues as VAL
import PixelPlots as PIX
import PixelFourier as FOR
import CCDMean as MEAN

### Main

# Take image as an arg and open image

ImgFile = str(sys.argv[1])

if len(sys.argv) > 2:
    row = int(sys.argv[2])
    col = int(sys.argv[3])

if len(sys.argv) > 4:
    if sys.argv[4] == "diff":
        first = int(sys.argv[5])
        second = int(sys.argv[6])
    if (sys.argv[4] == "trend") or (sys.argv[4] == "fourier"):
        start = int(sys.argv[5])
        end = int(sys.argv[6])


with fits.open(ImgFile) as hduImg:

    # general image data

    print("Skips: " + str(hduImg[0].header["NDCMS"]))
    print("Rows:  " + str(hduImg[0].header["NAXIS2"]))
    print("Cols:  " + str(hduImg[0].header["NAXIS1"] / hduImg[0].header["NDCMS"]))

    skips = hduImg[0].header["NDCMS"]

    # extract image data

    data = hduImg[0].data

    print("Point Val: " + str(data[row, col]))

    if len(sys.argv) > 2:
        print("Pixel Mean: " + str(VAL.findMean(data, row, col, skips)))
        print("Pixel MAD: " + str(VAL.findMAD(data, row, col, skips)))
        print("Pixel St. Dev: " + str(VAL.findStDev(data, row, col, skips)))

        if len(sys.argv) > 4:
            if sys.argv[4] == "diff":
                print(
                    "Difference between Measurements "
                    + str(first)
                    + " and "
                    + str(second)
                    + ": "
                    + str(VAL.findDiff(data, row, col, skips, first, second))
                )
            if sys.argv[4] == "trend":
                print(
                    "Slope of Measurements "
                    + str(start)
                    + " to "
                    + str(end)
                    + ": "
                    + str(VAL.findSlope(data, row, col, skips, start, end))
                )
                if len(sys.argv) > 7:
                    print("blah")
                    # PIX.plotCurveFit(data, row, col, skips, start, end, sys.argv[7])
            if sys.argv[4] == "fourier":
                print("efa")
                FOR.plotFourier(data, row, col, skips, start, end)

        # PIX.plotPixel(data, row, col, skips, ImgFile)
        MEAN.meanImage(data, row, col, start, end, skips, ImgFile)

    # print(RMS.mapSKrms(data, skips))
