import csv
import numpy as np
import matplotlib.pyplot as plt

for i in range(1,41):
    filename = 'D:/tools/github/threeFBGpredict/data/Measured3FBG{:04d}.csv'.format(i)
    csvfile = open(filename,'r')
    reader = list(csv.reader(csvfile))

    data=np.array(reader[75:]).astype(float)[:,:2].T  #第一列全部、第一二行 轉置
    x=data[0]
    y=data[1]
    plt.plot(x,y)
    plt.yscale("log")
    plt.pause(0.5)
    plt.clf()