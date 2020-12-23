from data_prepare.smooth import smooth
from data_prepare.loader import load
import numpy as np
import matplotlib.pyplot as plt

background_noise = load('./data/Measured3FBGnoise.csv')

points = 1001

start = 1545
stop = 1550

background_noise = np.array([
    np.linspace(start, stop, points),
    np.linspace(2.485e-6, 2.246e-6, points)
])

smooth_noise = smooth(background_noise[1])

if False:
    plt.plot(background_noise[1], label='backgorund noise')
    plt.plot(smooth_noise, label='smoothed')
    plt.legend()
    plt.title('smoothed background noise')
    plt.show()

noise_compensate = np.average(smooth_noise)
gain_compensate = noise_compensate / smooth_noise
