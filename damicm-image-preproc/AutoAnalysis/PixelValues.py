# Finds pertinent values of a single pixel

import numpy as np
import math

# Shifts the column position to the start of the first skip
offset = 2
# allows more pixels to be seen
multiplier = 1


def findStDev(data, row, column, skips):

    # Finds the st. dev of one pixel's measurement values

    stdev = 0
    mean = findMean(data, row, column, skips)

    for col in range(
        offset + column * skips, offset + column * skips + skips * multiplier, 1
    ):
        stdev = stdev + math.pow((mean - data[row, col]), 2) / (skips * multiplier)

    return math.sqrt(stdev)


def findMAD(data, row, column, skips):

    # Finds the mean absolute deviation of one pixel's measurement values

    MAD = 0
    mean = findMean(data, row, column, skips)

    for col in range(
        offset + column * skips, offset + column * skips + skips * multiplier, 1
    ):
        MAD = MAD + abs(data[row, col] - mean) / (skips * multiplier)

    return MAD


def findMean(data, row, column, skips):

    # Finds the mean of one pixel's measurement values

    mean = 0

    for col in range(
        offset + column * skips, offset + column * skips + skips * multiplier, 1
    ):
        mean = mean + data[row, col] / (skips * multiplier)

    return mean


def findDiff(data, row, column, skips, first, second):

    # Finds the difference between two measurment values

    return int(data[row, offset + column * skips + second]) - int(
        data[row, offset + column * skips + first]
    )


def findSlope(data, row, column, skips, start, end):

    # finds the trend slope of a given section of measurements

    xmean = float(skips) / 2
    ymean = findMean(data, row, column, skips)

    xydiffsum = 0
    xsquaresum = 0
    count = 0

    for col in range(offset + column * skips + start, offset + column * skips + end, 1):
        xydiffsum = xydiffsum + (count - xmean) * (data[row, col] - ymean)
        xsquaresum = xsquaresum + math.pow((count - xmean), 2)
        count = count + 1

    return (xydiffsum) / (xsquaresum)
