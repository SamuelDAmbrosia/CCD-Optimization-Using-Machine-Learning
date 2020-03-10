# Finds pertinent values of a single pixel

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit

# Shifts the column position to the start of the first skip
offset = 2
# allows more pixels to be seen
multiplier = 1


def plotPixel(data, row, column, skips, ImgFile):

    # plots all the measurments of a single pixel
    # skips x charge

    charges = []

    for col in range(
        offset + column * skips, offset + column * skips + skips * multiplier, 1
    ):
        charges.append(data[row, col])

    plt.plot(charges)
    plt.xlabel("Measurments")
    plt.ylabel("Charge/Voltage")
    plt.title(
        "Charge/Voltage per Measurement of a Single Pixel "
        + "("
        + str(row)
        + ","
        + str(column)
        + ")\n"
        + ImgFile
    )
    plt.show()


def plotCurveFit(data, row, column, skips, start, end, function):
    # fits the data to an arbitrary function between start and end

    xdata = []
    ydata = []

    # determine which function to choose
    if function == "cap":
        func = cap
    elif function == "sin":
        func = sin
    elif function == "line":
        func = line
    else:
        print("no such function")

    # fill data
    count = 0
    for col in range(offset + column * skips + start, offset + column * skips + end, 1):
        ydata.append(int(data[row, col]))
        xdata.append(count)
        count = count + 1

    xdata = np.array(xdata)
    ydata = np.array(ydata)

    # generate best fit and plot data
    plt.plot(xdata, ydata, "b-", label="data", linestyle="None", marker="o")

    popt, pcov = curve_fit(func, xdata, ydata)

    plt.plot(
        xdata,
        func(xdata, *popt),
        "r-",
        label="Trend: " + str(popt) + "\nError: " + str(pcov[0]),
    )

    print("error" + str(pcov))

    plt.xlabel("Measurement")
    plt.ylabel("Charge")
    plt.legend()
    plt.show()


def cap(x, C, V, b):
    # capacitance equation

    return C * V * (1 - np.exp(-(x) / C)) + b


def sin(x, C, P, b):

    return C * np.sin(P * x) + b


def line(x, m, b):

    return m * x + b
