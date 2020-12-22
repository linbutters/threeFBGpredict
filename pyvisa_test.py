import pyvisa
import numpy as np
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
resources = rm.list_resources()
print(resources)
inst = rm.open_resource(resources[-1])
print(inst.query("*IDN?"))

x = np.linspace(1545,1550,2001)
inst.write("STA 1545 ; STO 1550 ; LLV 367NW ; MPT 2001")  #掃描起點1545 ; 終點1550 ; 線性level 367nW ; 掃描51個點

def DE(traceA):
    #FBGs = [peak1,peak2,peak3]
    return FBGs    

def catch_data():
    traceA_data = inst.query("SSI ; *WAI ; PKL ; DMA?")  # 單次掃描 ; 等待處理完畢 ; peak對齊ref level ; 回傳數據(字串)
    traceA_parsed = [float(n) for n in [s.strip() for s in traceA_data.split('\n')] if len(n)>0]
    traceA = np.array(traceA_parsed)  # 光強資料
    return traceA

def draw(traceA):
    FBGs = []
    FBGs = DE(traceA)
    plt.plot(x,traceA)
    for i in range(len(FBGs)):
        plt.axvline(FBGs[i],label="peak{:1d}".format(i))
    plt.grid()
    plt.legend()

traceA = catch_data()
draw(traceA)