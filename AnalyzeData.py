from data_prepare import loader
import matplotlib.pyplot as plt
import numpy as np

background_noise = loader.load('./data/Measured3FBGnoise.csv')

def smooth(data, n=200):
    filter_size = n*2+1
    filter_kernal = np.cos(np.linspace(-1,1,filter_size)*np.pi)+1
    filter_kernal /= np.sum(filter_kernal)

    padded = np.pad(data, (n, n), 'edge')
    blur = np.convolve(padded, filter_kernal, 'valid')
    
    return blur

# smooth the background noise
smooth_noise = smooth(background_noise[1])
if False:
    plt.plot(background_noise[1], label='backgorund noise')
    plt.plot(smooth_noise, label='smoothed')
    plt.legend()
    plt.title('smoothed background noise')
    plt.show()

# gain compensation
gain_compensate =  np.average(smooth_noise) / smooth_noise


for i in range(1, 40):
    filename = './data/Measured3FBG{:04d}.csv'.format(i)

    data = loader.load(filename)
    print(data.shape)
    
    compensated = data[1]*gain_compensate
    smoothed = smooth(compensated, 50)
    d1 = smoothed[1:] - smoothed[:-1]
    d2 = d1[1:] - d1[:-1]

    threshold = d2 < -1e-9

    left = data[0,2:-1][threshold[1:] > threshold[:-1]]
    right = data[0,2:-1][threshold[1:] < threshold[:-1]]
    middle = (left+right)/2

    plt.plot(data[0], compensated)

    for m in middle:
        height = np.interp(m, data[0], compensated)
        plt.axvline(m, c='red')
        plt.axhline(height, c='red')

    plt.show()




