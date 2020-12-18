import pyvisa
import numpy as np
import csv
import matplotlib.pyplot as plt
import time

start = 1545
stop = 1550
lv = "367nw"
point = 51

x = np.linspace(start,stop,point)

rm = pyvisa.ResourceManager()
resources = rm.list_resources()
print(resources)
inst = rm.open_resource(resources[-1])
print(inst.query("*IDN?"))
inst.write("STA "+start+" ; STO "+stop+" ; LLV "+lv+" ; MPT "+point)

for i in range(0,1000):
    traceA_data = inst.query("SSI ; *WAI ; PKL ; DMA?")  #單次掃描 ; 等待處理完畢 ; peak對齊ref level ; 回傳數據(字串)
    traceA_parsed = [float(n) for n in [s.strip() for s in traceA_data.split('\n')] if len(n)>0]
    traceA = np.array(traceA_parsed)  #光強資料

    filename = 'D:/tools/github/threeFBGpredict/data/Measured3FBG{:04d}.csv'.format(i) #選放哪個資料夾
    csvfile = open(filename,'w',newline='')
    writer = csv.writer(csvfile)

    k = 0
    while (k<75):           #空75行
        writer.writerow(" ")
        k = k+1

    table = np.array([x,traceA]).T
    writer.writerows(table)