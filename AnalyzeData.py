from data_prepare import loader
from algorithm import DE
import matplotlib.pyplot as plt
import numpy as np

background_noise = loader.load('./data/Measured3FBGnoise.csv')

FOUR_LOG_TWO = 4*np.log(2)


def smooth(data, n=200):
    filter_size = n*2+1
    filter_kernal = np.cos(np.linspace(-1, 1, filter_size)*np.pi)+1
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
noise_compensate = np.average(smooth_noise)
gain_compensate = noise_compensate / smooth_noise

centers = []
heights = []
widths = []


def simulate(x_coord, X):
    """
    X = (NP, c/w/h, nFBG)
    """
    x_coord = np.tile(x_coord, [X.shape[0], X.shape[2],1])
    c = X[:, 0][:, :, np.newaxis]
    w = X[:, 1][:, :, np.newaxis]
    h = X[:, 2][:, :, np.newaxis]
    y = np.exp(-((x_coord-c)/w)**2*FOUR_LOG_TWO)*h
    return np.sum(y, 1)


for i in range(1, 40):
    filename = './data/Measured3FBG{:04d}.csv'.format(i)

    data = loader.load(filename)
    print(data.shape)

    compensated = data[1]*gain_compensate-noise_compensate
    smoothed = smooth(compensated, 50)
    d1 = smoothed[1:] - smoothed[:-1]
    d2 = d1[1:] - d1[:-1]

    threshold = d2 < -1e-9

    leftp = threshold[1:] > threshold[:-1]
    rightp = threshold[1:] < threshold[:-1]
    left = data[0, 2:-1][leftp]
    right = data[0, 2:-1][rightp]
    width = (right-left)

    center = []
    height = []
    width = []

    for i, m in enumerate(left):
        lp = np.arange(len(data[0])-3)[leftp][i]+2
        rp = np.arange(len(data[0])-3)[rightp][i]+2

        print(lp, rp)
        section_x = data[0, lp:rp+1]
        section_y = compensated[lp:rp+1]
        a = np.polyfit(section_x, np.log(section_y), 2)

        fit = np.exp(section_x**2 * a[0] + section_x * a[1] + a[2])

        print(a)

        c = -a[1]/a[0]/2
        w = 1/np.sqrt(-a[0]/FOUR_LOG_TWO)
        h = np.exp(a[2]+c**2/w**2*FOUR_LOG_TWO)
        print(c, w, h)

        center.append(c)
        width.append(w)
        height.append(h)

        if False:
            plt.plot(section_x, section_y)
            plt.plot(section_x, fit)
            plt.show()

    x = np.array([center, width, height])
    d = np.array([0.1, 0.01, 1e-7])[:,np.newaxis]
    down_lim = x - d
    up_lim = x + d

    de = DE.DE(.5, 0.1, 50)

    X = de.init(down_lim, up_lim)

    Perror = None
    PX = None

    for t in range(50):
        if PX is not None:
            X = de.mutate(PX)
        spectra = simulate(data[0], X)
        error = np.sum((spectra - compensated[np.newaxis, :])**2, 1)

        if Perror is not None:
            compare = error < Perror
            PX += (X-PX) * compare[:, np.newaxis, np.newaxis]
            Perror += (error-Perror) * compare
        else:
            Perror = error
            PX = X
        


        # plt.plot(spectra.T)
        # plt.show()

        # plt.plot(error)
        # plt.show()
    
    average = np.average(PX, 0)

    center, width, height = average

    centers.append(center)
    widths.append(width)
    heights.append(height)


    if True:
        plt.plot(data[0], compensated, c='black')

        for i, c in enumerate(center):
            w = width[i]
            h = height[i]
            x = data[0]
            fit = h*np.exp(-((x-c)/w)**2*FOUR_LOG_TWO)
            plt.plot(x, fit)

        plt.show()

for i, c in enumerate(centers):
    plt.scatter(c, heights[i])
plt.show()

for i, w in enumerate(widths):
    plt.scatter(w, heights[i])
plt.show()
