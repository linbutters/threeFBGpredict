from algorithm.DE import DE
import numpy as np
from algorithm.FBG import simulate

def optimize(data, center, width, height, d, iterations=20, F=.5, CR=0.1, NP=50):
    x = np.array([center, width, height])

    down_lim = x - d[:, np.newaxis]
    up_lim = x + d[:, np.newaxis]

    de = DE(F, CR, NP)

    X = de.init(down_lim, up_lim)

    Perror = None
    PX = None

    
    for t in range(iterations):
        if PX is not None:
            X = de.mutate(PX)
        spectra = simulate(data[0], X)
        error = np.sum((spectra - data[1, np.newaxis, :])**2, 1)

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

    return average