from algorithm.GaussianFit import fit
from algorithm.DE_FBG import optimize

from data_prepare.loader import load
from data_prepare.smooth import smooth
from data_prepare.compensate import noise_compensate, gain_compensate

import matplotlib.pyplot as plt
import numpy as np


set_height = np.array([5.3, 2.15, 0.37]) * 1e-5
set_width = np.ones(3) * 0.207
set_area = set_width * set_height

FOUR_LOG_TWO = 4*np.log(2)


def permute(n, m):
    arr = [[]]

    for i in range(n):
        narr = []
        for a in arr:
            for j in range(m):
                narr.append(a+[j])
        arr = narr
    return np.array(arr)


def fit3(data):
    data[1] = data[1]*gain_compensate-noise_compensate
    data[1] = smooth(data[1], 50)

    center, width, height = fit(data)

    print(center, width, height)

    area = np.array(width) * np.array(height)

    possibilitys = permute(len(set_area), len(area))

    Perr = None
    Ppos = None

    for p in possibilitys:
        err = 0
        for i,a in enumerate(area):
            err += (np.sum(set_area[p==i])-a)**2
        
        if Perr is None or err < Perr:
            Perr = err
            Ppos = p

    center = np.array(center)[Ppos]
    width = set_width
    height = set_height

    print(Ppos)
    d = np.array([0.1, 0, 0])

    center, width, height = optimize(data, center, width, height, d, 50)


    return center, width, height

for i in range(1, 40):
    filename = './data/Measured3FBG{:04d}.csv'.format(i)
    print(filename)

    data = load(filename)


    center, width, height = fit3(data)

    if True:
        plt.plot(*data, c='black')

        for i, c in enumerate(center):
            w = width[i]
            h = height[i]
            x = data[0]
            f = h*np.exp(-((x-c)/w)**2*FOUR_LOG_TWO)
            plt.plot(x, f)

        plt.show()

