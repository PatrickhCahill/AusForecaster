import os
import sys
import pandas as pd
import numpy as np
from datetime import date

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path += [dir_path]

def getsimfacts(location):
    data = pd.read_csv(location+"/MultiUpdatingOutWins.csv")
    labprob = sum(i>=76 for i in list(data["nLabor"]))/len(list(data["nLabor"]))
    libprob = sum(i>=76 for i in list(data["nLib"]))/len(list(data["nLib"]))
    avglabor = np.mean(list(data["nLabor"]))
    avglib = np.mean(list(data["nLib"]))

    data2 = pd.read_csv(location+"/MultiUpdatingOutAverages.csv")
    tpp_swing = sum(i for i in list(data2["predSwing"]))/len(list(data2["predSwing"]))
    outstring = "LaborProb,AvgLabSeats,LibProb,AvgLibSeats,HungProb,AvgIndSeats,PredSwing\n{},{},{},{},{},{},{}".format(labprob,avglabor,libprob, avglib,(1-labprob-libprob),(151-avglabor-avglib),tpp_swing)
    return outstring

def getsimprobs(location):
    data = pd.read_csv(location+"/MultiUpdatingOutWins.csv")
    today = date.today().strftime("%Y-%m-%d")
    labprob = sum(i>=76 for i in list(data["nLabor"]))/len(list(data["nLabor"]))
    libprob = sum(i>=76 for i in list(data["nLib"]))/len(list(data["nLib"]))
    hungprob = 1-labprob-libprob

    orderstring = "labels,labor,coalition,hung"
    outstring = "{},{},{},{}".format(today,labprob,libprob,hungprob)
    return orderstring, outstring

def getsimseats(location):
    data = pd.read_csv(location+"/MultiUpdatingOutWins.csv")
    today = date.today().strftime("%Y-%m-%d")
    labseats = sum(i for i in list(data["nLabor"]))/len(list(data["nLabor"]))
    libseats = sum(i for i in list(data["nLib"]))/len(list(data["nLib"]))
    indseats = 151-labseats-libseats

    orderstring = "labels,labor,coalition,hung"
    outstring = "{},{},{},{}".format(today,labseats,libseats,indseats)
    return orderstring, outstring


def writesims(location,func,outlocation):
    orderstring, simfacts = func(location+'/OutData')
    with open(dir_path+'/OutData'+'/'+outlocation+'.csv','a') as f:
        f.write("\n"+simfacts)
    print("____Proability:____")
    print(simfacts)


#writesims(dir_path,getsimseats,"simseats")