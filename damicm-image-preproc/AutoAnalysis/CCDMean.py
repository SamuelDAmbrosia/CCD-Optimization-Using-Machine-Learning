# Mean of each pixel

import matplotlib
import numpy as np
from astropy.io import fits

# Shifts the column position to the start of the first skip
offset = 2


def meanImage(data, row, column, start, end, skips, ImgFile):

    # plots all the measurments of a single pixel
    # skips x charge

    # write means to a 2d array

    charges = []

    for row in data:

        chargerow = []

        for column in range(0, int(len(row) / skips) - 1, 1):

            measurements = []

            for col in range(
                offset + start + column * skips,
                offset + end + column * skips + skips,
                1,
            ):
                measurements.append(row[col])

            chargerow.append(np.mean(measurements))

        charges.append(chargerow)

    # write data to a new fits file

    hdu = fits.PrimaryHDU(charges)

    hdul = fits.HDUList([hdu])
    hdul.writeto("Mean" + ImgFile)
