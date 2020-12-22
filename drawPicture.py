import numpy as np
import matplotlib.pyplot as plt
from data_prepare import loader

for i in range(1,41):
    filename = './data/Measured3FBG{:04d}.csv'.format(i)
    data=loader.load(filename)
    x=data[0]
    y=data[1]
    plt.plot(x,y)
    plt.pause(0.02)
    plt.clf()