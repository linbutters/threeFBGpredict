import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import threading
import time

import gauss_fit
import ML_fit
# import winsound


rm = pyvisa.ResourceManager()
resources = rm.list_resources()
print(resources)
inst = rm.open_resource(resources[-1])
print(inst.query("*IDN?"))

x = np.linspace(1545,1550,51)

inst.write("STA 1545 ; STO 1550 ; LLV 367NW ; MPT 51")  #掃描起點1545 ; 終點1550 ; 線性level 367nW ; 掃描51個點

drawing = False
ready = False

center_log = []
center_ml_log = []

center_store = []
center_ml_store = []

traceA = []




def draw():
    global drawing, ready

    while True:
        if not ready:
            time.sleep(0.01)
            continue

        ready = False

        plt.clf()
        #光譜圖與兩種方法找中心波長
        plt.subplot(211)
        plt.plot(x, traceA)
        #print(center_log)
        #print(center_ml_log)
        plt.axvline(center_log[-1], c='blue', label="Gaussian fit")
        plt.axvline(center_ml_log[-1], c='red', label="ML fit")
        plt.grid()
        plt.legend()

        
        plt.subplot(212)
        plt.plot(center_log, c='blue', label="Gaussian fit")
        plt.plot(center_ml_log, c='red', label="ML fit")
        plt.grid()
        plt.legend()
        
        plt.tight_layout()
        plt.pause(0.01)

        drawing = False
    

drawing_thread = threading.Thread(target = draw)

drawing_thread.start()


while True:
    
    traceA_data = inst.query("SSI ; *WAI ; PKL ; DMA?")  # 單次掃描 ; 等待處理完畢 ; peak對齊ref level ; 回傳數據(字串)
    traceA_parsed = [float(n) for n in [s.strip() for s in traceA_data.split('\n')] if len(n)>0]
    traceA = np.array(traceA_parsed)  # 光強資料

    # 兩種方法找到的中心波長位置漂移情形
    center = gauss_fit.find_peak(traceA)
    center_ml = ML_fit.find_peak(traceA)

    center_store.append(center)
    center_ml_store.append(center_ml)
    
    # print(center_ml_store)

    if len(center_store) > 50:
        center_store = center_store[-50:]
    if len(center_ml_store) > 50:
        center_ml_store = center_ml_store[-50:]

    ready = False
    center_log = np.array(center_store)
    center_ml_log = np.array(center_ml_store)
    ready = True
