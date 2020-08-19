#multicast simulation
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import matplotlib as mpl
import os

sns.set()
sns.set_context("talk")
# sns.set_style("white")
sns.set_style("ticks")
mpl.rc("figure", facecolor="white")

Nsim=1000

class multicastClass:
    #"this class defines a multicast message transport"
    # define number of multicast receiver, path_lss and packet size in byte

    def __init__(self, path_lss, N_recvr, N_pcktByte):
        self.PathLoss=path_lss
        self.Nrecvr=N_recvr
        self.NpcktByte=N_pcktByte
        self.RecvList=[]
        self.iteration=0
        self.dataSend=0
        self.totalReceived=0
        self.Nsimulations=Nsim
    def init_recv(self): #initiate the receive status of all the receiver
        for i in range(self.Nrecvr):
            self.RecvList.append(0)
        self. iteration=0
        self.dataSend=0

    def isAllrecved(self): #check whether all receiver recived the message
        total=0
        for i in range(len(self.RecvList)):
            total=total+self.RecvList[i]
        print("total received:"+str(total))
        self.totalReceived=total
        if (total==self.Nrecvr):   #when all receiver receive we will have total equaling Nreciver (Becoz recvList[i]=1 for recived case)
            return 1
        else:
            return 0
    def sendToAll(self):  #send message to all the reciver one time
        for i in range(len(self.RecvList)):
            if self.RecvList[i]==0: #only update the receiver which does not receive yet.
                number = np.random.choice([0, 1], p=[self.PathLoss, 1 - self.PathLoss])
                self.RecvList[i]=number
        print("Received List:", self.RecvList)
    def sendUntillAllRcv(self):
        while (self.isAllrecved() == 0):  # target: find number of iterations and number of byte sent into the network before packet reaches to each reciver
            self.iteration = self.iteration + 1
            self.sendToAll()
            self.dataSend = self.iteration * self.NpcktByte * self.Nrecvr
            #print("iteration", self.iteration, "dataSend", self.dataSend, "KB")
    def RunXtimes(self):
        iterationSet=[]
        datasendSet=[]
        for j in range(self.Nsimulations):
            for i in range(self.Nrecvr):
                self.RecvList[i]=0
            self.iteration = 0
            self.dataSend = 0
            self.sendUntillAllRcv()
            iterationSet.append(self.iteration)
            datasendSet.append(self.dataSend)
            print("Run", j+1, "itreation", self.iteration,"multicast data sent", self.dataSend)
        return iterationSet,datasendSet

    def info(self):  #print info for this class
        print("Number of reciver:"+str(self.Nrecvr)+" Loss Probablity:"+ str(self.PathLoss)+" Byte sent:"+ str(self.NpcktByte))
        print("Reciever Rcv Status:", self.totalReceived, str(self.RecvList))
        print("iteration", self.iteration, "dataSend", self.dataSend, "KB")

class unicastClass(multicastClass):
    def RunXtimes(self):
        iterationSet=[]
        datasendSet=[]
        for j in range(self.Nsimulations):
            for i in range(self.Nrecvr):
                self.RecvList[i]=0
            self.iteration = 0
            self.dataSend = 0
            self.sendUntillAllRcvUnicast()
            iterationSet.append(self.iteration)
            datasendSet.append(self.dataSend)
            print("Run", j+1, "itreation", self.iteration,"data sent", self.dataSend)
        return iterationSet,datasendSet

    def sendUntillAllRcvUnicast(self):
        while (self.isAllrecved() == 0):  # target: find number of iterations and number of byte sent into the network before packet reaches to each reciver
            self.iteration = self.iteration + 1
            self.sendToAll()
            self.dataSend =self.dataSend+ (self.Nrecvr-self.totalReceived) * self.NpcktByte
            print("iteration", self.iteration, "unicast dataSend", self.dataSend, "KB")

def plot_b0x(x,dl, sr):

    dlx = np.reshape(dl, (3, Nsim)) 
    srx = np.reshape(sr, (3, Nsim))
    # print(dlx.T)
    dl = pd.DataFrame(data=dlx.T, columns=['10', '20', '30'])
    ds = pd.DataFrame(data=srx.T, columns=['10', '20', '30'])

    print(dl)

    bp = sns.boxplot(x="variable", y="value", data=pd.melt(dl), linewidth=1, palette="Set3")
    bp.set(xlabel="Path Loss (%)", ylabel="Iterations")
    plt.xticks(rotation=45)
    #plt_name = file_pathx.replace('.txt', '_StallBox.pdf')
    plt.savefig(x+"_loss", bbox_inches='tight')
    plt.show()

    bp2 = sns.boxplot(x="variable", y="value", data=pd.melt(ds), linewidth=1)
    bp2.set(xlabel="Path Loss (%)", ylabel="Data Send (B)")
    plt.xticks(rotation=45)
    #plt_name = file_pathx.replace('.txt', '_SRBox.pdf')
    plt.savefig(x+"_data", bbox_inches='tight')
    plt.show()


def main():
    totalIter=[]
    totalData=[]
    multicast1= multicastClass(0.1,1000,64)  #loss(%)/100, Nreciever, PacketSize
    multicast1.init_recv()
    totalIterations, totaldataSet=multicast1.RunXtimes()
    totalIter.append(totalIterations)
    totalData.append(totaldataSet)
    print("pathLoss:10prcnt",totalIterations, totaldataSet)

    multicast2= multicastClass(0.2,1000,64)
    multicast2.init_recv()
    totalIterations, totaldataSet=multicast2.RunXtimes()
    totalIter.append(totalIterations)
    totalData.append(totaldataSet)
    print("pathLoss:20prcnt",totalIterations, totaldataSet)

    multicast3= multicastClass(0.3,1000,64)
    multicast3.init_recv()
    totalIterations, totaldataSet=multicast3.RunXtimes()
    totalIter.append(totalIterations)
    totalData.append(totaldataSet)
    print("pathLoss:30prcnt",totalIterations, totaldataSet)

    print(totalIter)
    print(totalData)
    plot_b0x("multicast",totalIter,totalData)

    totalIter = []
    totalData = []
    unicast3 = unicastClass(0.1, 1000, 64)
    unicast3.init_recv()
    totalIterations, totaldataSet = unicast3.RunXtimes()
    totalIter.append(totalIterations)
    totalData.append(totaldataSet)
    print("Unicast pathLoss:30prcnt",totalIterations, totaldataSet)

    unicast3 = unicastClass(0.2, 1000, 64)
    unicast3.init_recv()
    totalIterations, totaldataSet = unicast3.RunXtimes()
    totalIter.append(totalIterations)
    totalData.append(totaldataSet)
    print("Unicast pathLoss:30prcnt",totalIterations, totaldataSet)

    unicast3 = unicastClass(0.3, 1000, 64)
    unicast3.init_recv()
    totalIterations, totaldataSet = unicast3.RunXtimes()
    totalIter.append(totalIterations)
    totalData.append(totaldataSet)
    print("Unicast pathLoss:30prcnt",totalIterations, totaldataSet)

    print(totalIter)
    print(totalData)
    plot_b0x("unicast",totalIter,totalData)
if __name__ == "__main__":
    main()


