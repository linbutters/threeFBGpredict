import numpy as np
FOUR_LOG_TWO = 4*np.log(2)

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
