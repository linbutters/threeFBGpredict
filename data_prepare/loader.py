import csv
import numpy as np

def load(file):
    """
    讀取光譜儀量測到的數據
    """
    with open(file) as f:
        data = np.array(list(csv.reader(f))[75:]).astype(float)
    return data.T
