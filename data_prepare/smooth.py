import numpy as np

def smooth(data, n=200):
    filter_size = n*2+1
    filter_kernal = np.cos(np.linspace(-1, 1, filter_size)*np.pi)+1
    filter_kernal /= np.sum(filter_kernal)

    padded = np.pad(data, (n, n), 'edge')
    blur = np.convolve(padded, filter_kernal, 'valid')

    return blur