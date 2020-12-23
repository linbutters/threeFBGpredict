import numpy as np
import matplotlib.pyplot as plt
FOUR_LOG_TWO = 4*np.log(2)

def fit(data):

    d1 = data[1, 1:] - data[1, :-1]
    d2 = d1[1:] - d1[:-1]

    if False:
        plt.plot(d2)
        plt.show()

    threshold = d2 < -2e-9

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

        section_x = data[0, lp:rp+1]
        section_y = data[1, lp:rp+1]

        if False:
            plt.plot(section_x, section_y)
            plt.show()

        a = np.polyfit(section_x, np.log(section_y), 2)

        fit = np.exp(section_x**2 * a[0] + section_x * a[1] + a[2])


        c = -a[1]/a[0]/2
        w = 1/np.sqrt(-a[0]/FOUR_LOG_TWO)
        h = np.exp(a[2]+c**2/w**2*FOUR_LOG_TWO)

        center.append(c)
        width.append(w)
        height.append(h)

        if False:
            plt.plot(section_x, section_y)
            plt.plot(section_x, fit)
            plt.show()

    print(center)
    return center, width, height