# Fourier analysis of a pixel

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.fftpack import fft

# Shifts the column position to the start of the first skip
offset = 2
# allows more pixels to be seen
multiplier = 1


def plotFourier(data, row, column, skips, start, end):
    # Plots Fourier transform of a set of measurements

    ydata = []

    # fill data
    count = 0
    for col in range(offset + column * skips + start, offset + column * skips + end, 1):
        ydata.append(int(data[row, col]))

    ydata = np.array(ydata) - np.mean(ydata)

    N = end - start
    xdata = np.linspace(start, end, N)
    yf = fft(ydata)
    print(np.abs(yf[0 : N // 2]))
    xf = np.linspace(0.0, 1.0 / 2.0, N // 2)

    plt.plot(xf, 2.0 / N * np.abs(yf[0 : N // 2]))
    plt.title("Fourier")
    plt.grid()
    plt.show()
