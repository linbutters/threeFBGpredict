from data_prepare.loader import load
from data_prepare.smooth import smooth
from data_prepare.compensate import noise_compensate, gain_compensate

from algorithm.GaussianFit import fit
from algorithm.DE_FBG import optimize


import matplotlib.pyplot as plt
import numpy as np

FOUR_LOG_TWO = 4*np.log(2)

centers = []
heights = []
widths = []

for i in range(1, 40):
    filename = './data/Measured3FBG{:04d}.csv'.format(i)
    print(filename)

    data = load(filename)
    data[1] = data[1]*gain_compensate-noise_compensate
    data[1] = smooth(data[1], 50)


    center, width, height = fit(data)


    d = np.array([0.1, 0.01, 1e-7])

    center, width, height = optimize(data, center, width, height, d, 10)

    centers.append(center)
    widths.append(width)
    heights.append(height)

    if True:
        plt.plot(*data, c='black')

        for i, c in enumerate(center):
            w = width[i]
            h = height[i]
            x = data[0]
            f = h*np.exp(-((x-c)/w)**2*FOUR_LOG_TWO)
            plt.plot(x, f)

        plt.show()

for i, c in enumerate(centers):
    plt.scatter(c, heights[i])
plt.xlabel('wavelength')
plt.ylabel('intensity')
plt.show()

for i, w in enumerate(widths):
    plt.scatter(w, heights[i])
plt.xlabel('width')
plt.ylabel('intensity')
plt.show()
