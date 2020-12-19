import numpy as np
import matplotlib.pyplot as plt



def Gauss(peak):
    y = 0
    I = [1,0.5,0.25,0.125,0.0625]
    FWHM = [0.1968,0.1938,0.204,0.204,0.204]

    D = np.zeros(len(peak))
    for i in range(0,len(peak)):
        D[i]=((FWHM[i]/2.354820045)**2)*2
        y = y + I[i]*np.exp(-((x-peak[i])**2)/D[i])
    return y

def DE(x,y,correct,peak,FBGs):
    #DEpreset part:
    NP=50
    F=0.9
    CR=0.9
    iteration=1000
    spectrum=y

    #Initialize:
    #DE用
    X = np.random.rand(NP,FBGs)*5+1545
    #CRMSE = np.zeros(len(peak))
    if (correct != 0):
        for i in range(0,correct):
            X[i] = peak + (np.random.random_sample()*2-1)*0.05
            #for j in range(0,1):
                #CRMSE[j] = (np.random.rand()*2-1)*0.5
                #CRMSE[j] = a
                #X[i,j] = peak[j] + CRMSE[j]
    #print(X)
    #CRMSE_sum = np.sum(np.abs(CRMSE))
    #CRMSE_list.append(CRMSE_sum)
    V = np.zeros([NP,FBGs])
    U = np.zeros([NP,FBGs])

    #迭代用
    k = 0
    avgloss =[]
    itertime =[]
    
    #Iteration:
    while k <= iteration:
        #Mutate:
        for i in range(0,NP):
            rand1=np.random.randint(0,len(X)-1)
            rand2=np.random.randint(0,len(X)-1)
            rand3=np.random.randint(0,len(X)-1)
            while rand1 == rand2:
                rand2=np.random.randint(0,len(X)-1)
            while rand3 == rand2 or rand3 == rand1:
                rand3=np.random.randint(0,len(X)-1)

            r1 = X[rand1]
            r2 = X[rand2]
            r3 = X[rand3]
            V[i] = (r1 + F*(r2-r3)-1544)%5+1544
            #print(np.max(V, axis=0)) #對NP軸取最大=>axis="0"

            #Cross:
            for j in range(0,FBGs):
                if np.random.random_sample() < CR:
                    U[i,j] = V[i,j]
                else:
                    U[i,j] = X[i,j]

        #compare:
        avgpeak = np.zeros(FBGs)
        for i in range(0,NP):
            simulate1 = Gauss(X[i])
            simulate2 = Gauss(U[i])
            #plt.plot(x,simulate1)
            #plt.plot(x,simulate2)
            sum1 = np.sum(np.abs(spectrum-simulate1))
            sum2 = np.sum(np.abs(spectrum-simulate2))
            if sum1 >= sum2:
                X[i] = U[i]

        #求平均中心波長位置與loss
        avgpeak = np.mean(X,axis = 0) 
        avgloss.append(np.sum(np.abs(spectrum-Gauss(avgpeak))))
        itertime.append(k)
        k = k+1

        '''
        if k % 10  == 0:
            #畫原始光譜與最靠近光譜
            plt.clf()
            plt.subplot(2,1,1)
            plt.plot(x,spectrum)
            plt.plot(x,Gauss(avgpeak))

            #畫迭代次數
            plt.subplot(2,1,2)
            plt.plot(itertime,avgloss)
            plt.yscale('log')

            plt.pause(0.01)
        '''

        #截止條件用
        minwave=np.ones(FBGs)*1e10
        maxwave=np.zeros(FBGs)
        for j in range(0,len(peak)):
            for i in range(0,NP):
                if minwave[j] > X[i,j]:
                    minwave[j] = X[i,j]
                if maxwave[j] < X[i,j]:
                    maxwave[j] = X[i,j]

        maxerror = 0
        for i in range(0,len(peak)):
            maxerror = maxerror + maxwave[i]-minwave[i]

        if (maxerror < 1e-2):
            print("iterations:" + str(k))
            break
        
    return Gauss(avgpeak),avgpeak,k

start = 1545
stop = 1550
point = 2001

x = np.linspace(start,stop,point)
