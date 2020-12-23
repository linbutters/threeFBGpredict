import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import json

from Fit3FBG import fit3

# VISA SETUP
rm = pyvisa.ResourceManager()
resources = rm.list_resources()
print(resources)
inst = rm.open_resource(resources[-1])
print(inst.query("*IDN?"))

x = np.linspace(1545,1550,2001)
inst.write("STA 1545 ; STO 1550 ; LLV 367NW ; MPT 2001")  #掃描起點1545 ; 終點1550 ; 線性level 367nW ; 掃描51個點


def draw(data, FBGs):
    plt.plot(*data)

    for i, f in enumerate(FBGs):
        plt.axvline(f, label="peak {:1d}".format(i+1))

    plt.grid()
    plt.legend()



from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "10.123.2.115"
serverPort = 1234

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        traceA_data = inst.query("SSI ; *WAI ; PKL ; DMA?")  # 單次掃描 ; 等待處理完畢 ; peak對齊ref level ; 回傳數據(字串)
        traceA_parsed = [float(n) for n in [s.strip() for s in traceA_data.split('\n')] if len(n)>0]
        data = np.array([x, traceA_parsed])  # 光強資料
        
        center, width, height = fit3(data)
        draw(data, center)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(center), "utf-8"))
        

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")