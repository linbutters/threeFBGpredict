from data_prepare.smooth import smooth
from data_prepare.loader import load
import numpy as np

background_noise = load('./data/Measured3FBGnoise.csv')
smooth_noise = smooth(background_noise[1])

if False:
    plt.plot(background_noise[1], label='backgorund noise')
    plt.plot(smooth_noise, label='smoothed')
    plt.legend()
    plt.title('smoothed background noise')
    plt.show()

noise_compensate = np.average(smooth_noise)
gain_compensate = noise_compensate / smooth_noise
