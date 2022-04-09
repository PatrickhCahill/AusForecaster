import os

from logging import exception
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.io.parsers import read_csv
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

## Read the data from the last election and this election


dir_path = os.path.dirname(os.path.realpath(__file__)).removesuffix("\code")
POLLINGDATA2019 = pd.read_csv(dir_path+"/polling_data/2019polling.csv")
POLLINGDATA2022 =pd.read_csv(dir_path+"/polling_data/2022PollingData.csv")
NSWPOLLINGDATA2022 =pd.read_csv(dir_path+"/polling_data/2022NSWPollingData.csv")
VICPOLLINGDATA2022 =pd.read_csv(dir_path+"/polling_data/2022VICPollingData.csv")
QLDPOLLINGDATA2022 =pd.read_csv(dir_path+"/polling_data/2022QLDPollingData.csv")
SAPOLLINGDATA2022 =pd.read_csv(dir_path+"/polling_data/2022SAPollingData.csv")
WAPOLLINGDATA2022 =pd.read_csv(dir_path+"/polling_data/2022WAPollingData.csv")






def getxsandys(n,polling_data=POLLINGDATA2019):
    '''Expects Data to be of the form [Lib,Lab,Greens,ONP,IND,LibTPP,LabTPP] and converts this into the xs which are the primary votes and the ys 
    which are the tpp votes.'''
    xs=[float(i) for i in polling_data.iloc[n][:5]]
    ys=[float(i) for i in polling_data.iloc[n][6:]]
    return xs,ys
def makefloats(lst:list):
    '''Tries to make a list all floats'''
    try:
        return [float(i) for i in lst]
    except:
        print("Make Floats Failed")
        return lst

def weights(pollarray,power):
    '''Creates a set of weights based on a power law'''
    npolls = len(list(pollarray[0]))
    weightlist = list(range(1,npolls+1))
    # Turn this into a power law
    weightlist = [i**power for i in weightlist]
    # Normalises the weightlist
    weightlist = [i/sum(weightlist) for i in weightlist]
    
    ### Need To Update This Function To Include Samplesize. Should look something like this:
    # weightlist = [weightlist[i]*pollarray["samplesize"][i] for i in range(len((weightlist)))]
    # Normalise again, and then return

    return weightlist[::-1]

def weightedaverage(values,weights):
    '''Takes the weighted average of some list of values and weights'''
    try:
        average = 0
        for i in range(len(values)):
            average += values[i]*weights[i]
        return average
    except:
        print("Unable to take weighted average - check if the lists are all numbers or of equal length. Using simple mean instead")
        return np.mean(values)

def dotproduct(a,b):
    product = 0
    try:
        for i in range(len(a)):
            product += a[i]*b[i]
        return product
    except:
        print("Unable to take dotproduct - check if the lists are all numbers or of equal length. Using simple mean instead")
        return 0

def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            cache[args] = func(*args)
            return cache[args]
    return wrapper


def pollregression(polling_data=POLLINGDATA2019):
    '''Create the linear regression model from the 2019 data'''
    x=[]
    y=[]
    for poll in polling_data.index:
        xs,ys=getxsandys(poll)
        x.append(xs)
        y.append(ys)

    model =  linear_model.LinearRegression().fit(x, y)
    #This linear_model takes the xs (which is pimary vote data),
    # and then it creates a regression model by fitting the xs to the ys (the TPP data).
    # i.e this model uses election data and polling data from 2019 to create preference flows.
    # This model will be averaged out later.
    
    
    r_sq = model.score(x, y)
    # This is the r squared value for the regression model - the closer to 1 the better.
    
    #Some more potentially useful functions if you want to investigate this model.
    # print('coefficient of determination:', r_sq)
    # print('intercept:', model.intercept_)
    # print('slope:', model.coef_)
    return model
pollregression=memoize(pollregression)

def getnatswing(predlab,location="AUS"):
    '''Finds the tpp swing based off a predicted labor tpp share and the 2019 lab tpp share'''
    
    #This simply sets the 2019 result depending on which state is which.
    if location == "AUS":
        lab2019=0.4847
    elif location == "NSW":
        lab2019=0.4822
    elif location == "VIC":
        lab2019=0.5314
    elif location == "QLD":
        lab2019=0.4156
    elif location == "SA":
        lab2019=0.5071
    elif location == "WA":
        lab2019=0.4445
    elif location == "TAS":
        lab2019=0.5596 
    else:
        print("Invalid location. Assuming location is Australia. ie federal")
        lab2019=0.4847
    #Returns the difference of the predicted Lab and the 2019 Lab based of the location.
    return predlab - lab2019
 
def weightpower(pollingmodel=pollregression(),polling_data=POLLINGDATA2019,power=0.5):
    '''Uses the 2019 polling data in order to determine the best power distribution for the weights. i.e Polls
    are weighted based off how recent they are. The older the poll the less it is weighted. This function quantifies that
    by fitting the averages to a power law.'''

    polling_array = [makefloats(list(polling_data[i])) for i in polling_data.columns]
    weightlist = weights(polling_array,power)
    ## Getting polling averages
    average2019polls = [weightedaverage(polling_array[i],weightlist) for i in range(len(polling_array))]
    #print(average2022polls)
    natlab2019 = pollingmodel.intercept_[0] + dotproduct(pollingmodel.coef_[0],average2019polls)
    if abs(getnatswing(predlab=natlab2019))<=0.005:
        pass
    #    print("Convergence achieved!")
    #    print("In Reality, Labor's 2019 TPP Was 0.4847")
    #    print("Labor's Predicted TPP 2019 Voteshare: ",natlab2019)
    else:
        #print(power+0.1)
        power = weightpower(power=power+0.05)
    return power


def wranglecurrentdata(pollingmodel=pollregression(),polling_data=POLLINGDATA2022):
    '''Wrangling the 2022 data and creating the weights list for a weighted average (recent polls count more).'''
    polling_array = [makefloats(list(polling_data[i])) for i in polling_data.columns]
    weightlist = weights(polling_array,weightpower())

    ## Getting polling averages
    average2022polls = [weightedaverage(polling_array[i],weightlist) for i in range(len(polling_array))]
    #print(average2022polls)

    natlab2022 = pollingmodel.intercept_[0] + dotproduct(pollingmodel.coef_[0],average2022polls)
    return natlab2022

def datewrangle(date,pollingmodel=pollregression(),polling_data=POLLINGDATA2022):
    '''Wrangling the 2022 data and creating the weights list for a weighted average (recent polls count more) for all polls up to a certain date.'''
    dates = list(polling_data[:,"Date"])
    polling_data = polling_data.copy().drop(columns="Date")
    
    polling_array = [makefloats(list(polling_data[i])) for i in polling_data.columns]
    weightlist = weights(polling_array,weightpower())

    ## Getting polling averages
    average2022polls = [weightedaverage(polling_array[i],weightlist) for i in range(len(polling_array))]
    #print(average2022polls)

    natlab2022 = pollingmodel.intercept_[0] + dotproduct(pollingmodel.coef_[0],average2022polls)
    return natlab2022    



def getpollpreds():
    natlab2022 = wranglecurrentdata()
    # print("National Stats:")
    # print("Labor TPP: ", natlab2022, " and Predicted Swing: ", getnatswing(natlab2022,location="AUS"))
    nswlab2022 = wranglecurrentdata(polling_data=NSWPOLLINGDATA2022)
    # print("NSW Stats:")
    # print("Labor TPP: ", nswlab2022, " and Predicted Swing: ", getnatswing(nswlab2022,location="NSW"))
    viclab2022 = wranglecurrentdata(polling_data=VICPOLLINGDATA2022)
    # print("VIC Stats:")
    # print("Labor TPP: ", viclab2022, " and Predicted Swing: ", getnatswing(viclab2022,location="VIC"))
    qldlab2022 = wranglecurrentdata(polling_data=QLDPOLLINGDATA2022)
    # print("QLD Stats:")
    # print("Labor TPP: ", qldlab2022, " and Predicted Swing: ", getnatswing(qldlab2022,location="QLD"))
    salab2022 = wranglecurrentdata(polling_data=SAPOLLINGDATA2022)
    # print("SA Stats:")
    # print("Labor TPP: ", salab2022, " and Predicted Swing: ", getnatswing(salab2022,location="SA"))
    walab2022 = wranglecurrentdata(polling_data=WAPOLLINGDATA2022)
    # print("WA Stats:")
    # print("Labor TPP: ", walab2022, "and Predicted Swing: ", getnatswing(walab2022,location="WA"))
    stateswings = {"AUS":getnatswing(natlab2022,location="AUS"),"NSW":getnatswing(nswlab2022,location="NSW"),"VIC":getnatswing(viclab2022,location="VIC"),"QLD":getnatswing(qldlab2022,location="QLD"),"SA":getnatswing(salab2022,location="SA"),"WA":getnatswing(walab2022,location="WA")}
    return stateswings

def testing(pollingmodel=pollregression(),polling_data=POLLINGDATA2022):
    '''Wrangling the 2022 data and creating the weights list for a weighted average (recent polls count more).'''


    ## Getting polling averages
    ##      LNP | ALP|GRN |ONP |OTH
    poll = [0.365,0.363,0.08,0.03,0.11]
    #print(average2022polls)
    print(sum(poll))
    natlab2022 = pollingmodel.intercept_[0] + dotproduct(pollingmodel.coef_[0],poll)
    return natlab2022