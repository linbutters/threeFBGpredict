import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import json

from Fit3FBG_TF import fit3

# VISA SETUP
rm = pyvisa.ResourceManager()
resources = rm.list_resources()
print(resources)
inst = rm.open_resource(resources[-1])
print(inst.query("*IDN?"))


x = np.linspace(1545,1550,51)
inst.write("STA 1545 ; STO 1550 ; LLV 367NW ; MPT 51")  #掃描起點1545 ; 終點1550 ; 線性level 367nW ; 掃描51個點


def draw(data, FBGs):
    plt.clf()
    plt.plot(*data)
    for i, f in enumerate(FBGs):
        plt.axvline(f, label="peak {:1d} = {:.2f}".format(i+1, f), c=['blue', 'orange', 'green'][i])

    plt.yscale('log')
    plt.xlabel("wavelength")
    plt.grid()
    plt.legend()
    plt.tight_layout()



from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "10.123.6.60"
serverPort = 1234


def get():
    traceA_data = inst.query("SSI ; *WAI ; PKL ; DMA?")  # 單次掃描 ; 等待處理完畢 ; peak對齊ref level ; 回傳數據(字串)
    traceA_parsed = [float(n) for n in [s.strip() for s in traceA_data.split('\n')] if len(n)>0]
    data = np.array([x, traceA_parsed])  # 光強資料
    
    center = [1550,1550,1550]
    # center, width, height = fit3(data)
    center = np.array(center)
    # draw(data, center)
    # plt.pause(0.01)
    # plt.show()
    return data, center

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/data':

            data, center = get()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            obj = {
                "data": data.tolist(),
                "center": center.tolist()
            }

            self.wfile.write(bytes(json.dumps(obj), "utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open('./index.html', 'r') as f:
                self.wfile.write("\n".join(f.readlines()).encode())

if __name__ == "__main__":        

    # while True:
    #     get()


    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    
    
    try:
        webServer.serve_forever()
        pass
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")