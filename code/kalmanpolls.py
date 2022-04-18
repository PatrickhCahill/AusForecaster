'''Original Kalman From Here https://arxiv.org/ftp/arxiv/papers/1204/1204.0375.pdf'''
from numpy import diagonal, dot, sum, tile, array,diag,eye, arange
from numpy.linalg import inv, det
from math import log,exp,pi,sqrt

import datetime as dt
from pandas import read_csv
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

import numpy as np


class poll: 
    '''Defines the poll object, which has the properties outlined in __init__ All polls turned into this object'''
    def __init__(self,startDate,endDate,pollster,mode,scope,size,liberal,labor,greens,onp,ind,und,deltas):
        try: self.startDate = dt.date.fromisoformat(startDate) 
        except: self.startDate =startDate
        try: self.endDate = dt.date.fromisoformat(endDate)
        except: self.endDate =endDate        
        self.pollster = pollster
        self.mode = mode
        self.scope = scope
        self.size = int(size)
        self.labor = labor
        self.liberal = liberal
        self.greens = greens
        self.onp = onp
        self.ind = ind
        self.und =und
        self.deltas = deltas
    def __str__(self):
        return str(self.__dict__)
    def __rpr__(self):
        return str(self.__dict__)
    def getvar(self,party):
        v = self.__getattribute__(party)
        return v*(1-v)/self.size
    def converttoYs(self):
        try:
            self.corrections = self.deltas[self.pollster]["corrections"]
            for i in range(0,len(self.corrections)):
                self.corrections[i] *= self.deltas[self.pollster]["strength"]
        except:
            self.corrections= [0,0,0,0,0]
        return array([[self.liberal+self.corrections[0]],[self.labor+self.corrections[1]],[self.greens+self.corrections[2]],[self.onp+self.corrections[3]],[self.ind+self.corrections[4]]])
        # return array([[self.liberal],[self.labor],[self.greens],[self.onp],[self.ind]])

    def getvars(self):
        vars = [self.getvar(party) for party in ["liberal","labor","greens","onp","ind"]]
        return [var for var in vars]

def csvtopollss(file,deltas):
    '''Polls are entered manually into this csv filed and converted into a list of poll objects'''
    pollingdata =read_csv(file)
    natpolls = []
    for i in pollingdata.index:
        inputlist = list(pollingdata.loc[i]) + [deltas]
        natpolls.append(poll(*tuple(inputlist)))
    return natpolls

def handlepolls(simDate,polls):
    '''Takes a list of polls and returns the a new list pruned to include polls that were published after simdate'''
    outpolls = []
    for inpoll in polls:
        if (inpoll.endDate-simDate).days>=0:
            outpolls.append(inpoll)
    return(outpolls)

def initialise(results2019,config):
    '''Let's begin by Defining Our Time Step'''
    # It's important to note that we need to "dedimensionalize our step"
    '''We now initialise our matrices'''
    X = array([[i]for i in results2019]+[[0.0]for i in results2019]) #Inital State vector, all "velocities" are set to 0
    P = 0.001*eye(2*len(results2019)) #Initial covariance matrix. Set to all 0.01
    A = array([[1,0,0,0,0,config["step"],0,0,0,0],
        [0,1,0,0,0,0,config["step"],0,0,0],
        [0,0,1,0,0,0,0,config["step"],0,0],
        [0,0,0,1,0,0,0,0,config["step"],0],
        [0,0,0,0,1,0,0,0,0,config["step"]],
        [0,0,0,0,0,1,0,0,0,0 ],
        [0,0,0,0,0,0,1,0,0,0 ],
        [0,0,0,0,0,0,0,1,0,0 ],
        [0,0,0,0,0,0,0,0,1,0 ],
        [0,0,0,0,0,0,0,0,0,1 ]]) #This array defines a simple x_n = x_{n-1} + v_{n-1}*step relation. 

    Q = config["systemuncertainty"]*eye(X.shape[0])
    B = eye(X.shape[0])
    return X,P,A,Q,B

def kf_predict(X, P, A, Q, B, U):
    X = dot(A, X) + dot(B, U)
    P = dot(A, dot(P, A.T)) + Q
    return(X,P) 

def kf_update(X, P, Y, H, R):
    IM = dot(H, X)
    IS = R + dot(H, dot(P, H.T))
    K = dot(P, dot(H.T, inv(IS)))
    X = X + dot(K, (Y.converttoYs()-IM))
    P = P - dot(K, dot(IS, K.T))
    LH = gauss_pdf(Y.converttoYs(), IM, IS)
    return (X,P,K,IM,IS,LH) 

def gauss_pdf(X, M, S):
    if M.shape[1] == 1:
        DX = X - tile(M, X.shape[1])
        E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
        E = E + 0.5 * M.shape[0] * log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    elif X.shape[1] == 1:
        DX = tile(X, M.shape[1])- M
        E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
        E = E + 0.5 * M.shape[0] * log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    else:
        DX = X-M
        E = 0.5 * dot(DX.T, dot(inv(S), DX))
        E = E + 0.5 * M.shape[0] * log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    return (P,E)

def getY(theDate,Ys,X,results2019):
    currentYs = []
    for y in Ys:
        if y.endDate == theDate:
            currentYs.append(y)

    if len(currentYs)==0:
        # currentPreds = list(X.T[0])[:len(results2019)]
        # Y = poll(theDate,theDate,"Predictive","n/a","NAT",1,currentPreds[0],currentPreds[1],currentPreds[2],currentPreds[3],currentPreds[4],0)
        return False
    elif len(currentYs)==1:
        return currentYs[0]
    else:
        size = 0
        liberal = 0
        labor = 0
        greens = 0
        onp = 0
        ind=0
        und = 0
        for y in currentYs:
            size += y.size
            liberal += y.liberal/len(currentYs)
            labor += y.labor/len(currentYs)
            greens += y.greens/len(currentYs)
            onp += y.onp/len(currentYs)
            ind += y.ind/len(currentYs)
            und += y.und/len(currentYs)
        avgdPoll = poll(theDate,theDate,"Accumulated","n/a","NAT",size,liberal,labor,greens,onp,ind,und,False)
        return avgdPoll

def getU(X,naturalmeans,config):
    '''This function is where the'''

    currentPreds = list(X.T[0])
    revert_to_mean = []
    for i,val in enumerate(naturalmeans):
        revert_to_mean.append(naturalmeans[i]-currentPreds[i])
    U = array([[0] for i in naturalmeans]+[[ val*config["mean_reversion_strength"]] for val in revert_to_mean])
    return U

def makepositivedef(mat):
    for column in range(0,mat.shape[0]):
        for row in range(0,mat.shape[1]):
            if mat[row][column]<=0:
                mat[row][column]=0
            if mat[row][column]>1:
                mat[row][column]=1
        return mat

def normaliseX(X):
    norm = float(sum(X[0:5]))
    X[0:5] = X[0:5]/norm
    return X

def applyfilter(startDate,endDate,results2019,Ys,config):
    H = array([[1,0,0,0,0,0,0,0,0,0,],
    [0,1,0,0,0,0,0,0,0,0,],
    [0,0,1,0,0,0,0,0,0,0,],
    [0,0,0,1,0,0,0,0,0,0,],
    [0,0,0,0,1,0,0,0,0,0,]]
    )
    '''Number of iterations in Kalman Filter'''
    theDate = startDate
    N_iter = (endDate-theDate).days #This should eventually be len(Ys)

    
    ''' Applying the Kalman Filter'''
    X,P,A,Q,B = initialise(results2019,config) #We get the initial states   
    dates = [theDate]
    Xs = [X]
    Ps = [P]
    for i in arange(0, N_iter):
        theDate += dt.timedelta(days=config["step"])
        U = getU(X,results2019,config)
        (X, P) = kf_predict(X, P, A, Q, B, U)
        Y = getY(theDate,Ys,X,results2019)
        if Y != False: # If there is a poll on this day. Then we perform kf_update()
            R = config["polluncertaintyamplifier"]*diag(Y.getvars())
            (X, P, K, IM, IS, LH) = kf_update(X, P, Y, H, R)
        else:   #If there is no poll then we interpolate the X position like this.
            X = Xs[-1] + config["XNoPollStrength"]*(X-Xs[-1])
            P = Ps[-1] + config["PNoPollStrength"]*(P-Ps[-1])
        X = normaliseX(X)
        Xs.append(X)
        Ps.append(P)
        dates.append(theDate)

    Ss = Xs.copy()
    Ss.reverse()
    Xs.reverse()
    Ps.reverse()

    for index in range(1,len(Xs)):
        try:
            C = dot(Ps[index],dot(A.T,inv(Ps[index-1])))
        except:
            # print(Ps[index-1])
            pass
        Ss[index] += dot(C,(Ss[index-1]-Xs[index-1]))
    Ss.reverse()
    return dates,Ss,Ps

def getprimaryvote(Ss,results2019):
    primaryvote = list(Ss[0][0:len(results2019)].T[0])
    primaryvotes = [[i] for i in primaryvote]

    for S in Ss[1:]:
        primaryvote = list(S[0:len(results2019)].T[0])
        for index, value in enumerate(primaryvote):
            primaryvotes[index].append(value)


    return primaryvotes

def geterrors(Ps,results2019):
    diagP = list(diagonal(Ps[0]))
    errors = diagP[0:len(results2019)]
    errorslist = [[i] for i in errors]

    for P in Ps[1:]:
        diagP = list(diagonal(P))
        errors = diagP[0:len(results2019)]
        for index, value in enumerate(errors):
            errorslist[index].append(value)


    return errorslist

def smoothlist(primarylist):
    smoothprimarieslist = []
    for partyprimary in primarylist:
        time = list(range(0,len(partyprimary)))
        smoothed = lowess(partyprimary,time, is_sorted=True, frac=0.1, it=0)
        smoothprimarieslist.append(smoothed[:,1])
    return smoothprimarieslist

def aggregatepolls(startDate,endDate,results2019,Ys,config):
    dates,Ss, Ps = applyfilter(startDate,endDate+dt.timedelta(days=31),results2019,Ys,config)
    primaryvotes = getprimaryvote(Ss,results2019)
    primaryerrors = geterrors(Ps,results2019)

    primaryvotes,primaryerrors = smoothlist(primaryvotes),smoothlist(primaryerrors)
    primaryvotes,primaryerrors = array(primaryvotes).T,array(primaryerrors).T
    
    outdates = []
    outvotes = [[],[],[],[],[]]
    outerrors = [[],[],[],[],[]]

    for index, eachdate in enumerate(dates):
        if eachdate <= endDate:
            outdates.append(eachdate)
            for i in range(0,5):
                outvotes[i].append(primaryvotes[index][i])
                outerrors[i].append(primaryerrors[index][i])

    return  outdates, outvotes,outerrors

def plotparty(dates,primaryvotes, primaryerrors,party,Ys):
    liberalvotes = array(primaryvotes[party])
    variances = primaryerrors[party]
    confidences = []
    for var in variances:
        confidences.append(1.96*sqrt(var))
    liberalerrors = array(confidences)

    polldates = []
    colvals = []
    if party == 0:
        for Y in Ys:
            polldates.append(Y.endDate)
            colvals.append(Y.liberal)
        plt.plot(polldates,colvals,"o",color=(0,0,1,0.5))
        plt.plot(dates,primaryvotes[party],"-b")
        plt.fill_between(dates, liberalvotes-liberalerrors, liberalvotes+liberalerrors,color=(0,0,0.5,0.5))

    elif party == 1:
        for Y in Ys:
            polldates.append(Y.endDate)
            colvals.append(Y.labor)
        plt.plot(polldates,colvals,"o",color=(1,0,0,0.5))
        plt.plot(dates,primaryvotes[party],"-r")
        plt.fill_between(dates, liberalvotes-liberalerrors, liberalvotes+liberalerrors,color=(1,0,0,0.5))

    elif party == 2:
        for Y in Ys:
            polldates.append(Y.endDate)
            colvals.append(Y.greens)
        plt.plot(polldates,colvals,"o",color=(0,1,0,0.5))
        plt.plot(dates,primaryvotes[party],"-g")
        plt.fill_between(dates, liberalvotes-liberalerrors, liberalvotes+liberalerrors,color=(0,1,0,0.5))
    elif party == 3:
        for Y in Ys:
            polldates.append(Y.endDate)
            colvals.append(Y.onp)
        plt.plot(polldates,colvals,"o",color=(0.6,0.3,0.3,0.5))
        plt.plot(dates,primaryvotes[party],"-",color=(0.6,0.3,0.3,1))
        plt.fill_between(dates, liberalvotes-liberalerrors, liberalvotes+liberalerrors,color=(0.6,0.3,0.3,0.5))

    elif party == 4:
        for Y in Ys:
            polldates.append(Y.endDate)
            colvals.append(Y.ind)
        plt.plot(polldates,colvals,"o",color=(0.5,0.5,0.5,0.5))
        plt.plot(dates,primaryvotes[party],"-",color=(0.5,0.5,0.5,1))
        plt.fill_between(dates, liberalvotes-liberalerrors, liberalvotes+liberalerrors,color=(0.5,0.5,0.5,0.5))

def sortpolls(polls,endDate):
    outpolls = []
    for apoll in polls:
        if apoll.endDate <=endDate:
            outpolls.append(apoll)
    return outpolls

def sortpollspollster(polls,pollster):
    outpolls = []
    for apoll in polls:
        if apoll.pollster ==pollster:
            outpolls.append(apoll)
    return outpolls    

def getavgonday(file,endDate,config):
    results2019 = [0.4144,0.3334,0.104,0.033,0.115] #Results of the 2019 election
    results2016 = [0.4204,0.3437,0.123,0.033,0.078] #Results of the 2016 election
    
    deltas =  {"Essential" :{"strength":config["deltas"]["essentialStrength"], "corrections":[ 0.029, -0.025,  0.007, -0.029,  0.018]},
            "Newspoll"  :{"strength":config["deltas"]["newspollStrength"], "corrections":[ 0.033, -0.038,  0.013, -0.003, -0.004]},
            "Roy Morgan":{"strength":config["deltas"]["royMorganStrength"], "corrections":[ 0.056, -0.055,  0.008, -0.011,  0.002]}}

    Ys = sortpolls(csvtopollss(file,deltas),endDate)
    dates,primaryvotes, primaryerrors = aggregatepolls(dt.date.fromisoformat("2019-05-18"),endDate,results2019,Ys,config)

    return dates[-1], list(array(primaryvotes).T[-1]), list(array(primaryerrors).T[-1])

def getswingskalmanfilter(currentDate,config):
    files = ["polling_data/2022natpolls.csv","polling_data/2022nswpolls.csv","polling_data/2022vicpolls.csv","polling_data/2022qldpolls.csv","polling_data/2022wapolls.csv"]
    primaries = [getavgonday(file,currentDate,config)[1] for file in files]
    vars = [getavgonday(file,currentDate,config)[2] for file in files]
    stds = []
    for index,file in enumerate(files):
        stds.append([sqrt(abs(var)) for var in vars[index]])
    
    return primaries, stds


results2019 = [0.4144,0.3334,0.104,0.033,0.115] #Results of the 2019 election
results2016 = [0.4204,0.3437,0.123,0.033,0.078] #Results of the 2016 election
config ={
    "file":"polling_data/2022natpolls.csv",
    "step":1, #1 day,
    "PNoPollStrength":0.000,
    "XNoPollStrength":0.005  ,
    "systemuncertainty":0.05,   
    "mean_reversion_strength":0.1,
    "polluncertaintyamplifier":1,
    "deltas":{
        "essentialStrength":0.3,
        "newspollStrength":0.3,
        "royMorganStrength":0.3,
    }
}
deltas =  {"Essential" :{"strength":config["deltas"]["essentialStrength"], "corrections":[ 0.029, -0.025,  0.007, -0.029,  0.018]},
            "Newspoll"  :{"strength":config["deltas"]["newspollStrength"], "corrections":[ 0.033, -0.038,  0.013, -0.003, -0.004]},
            "Roy Morgan":{"strength":config["deltas"]["royMorganStrength"], "corrections":[ 0.056, -0.055,  0.008, -0.011,  0.002]}}
# print(getavgonday(dt.date.fromisoformat("2020-01-01"),config))


# Ys = sortpollspollster(sortpolls(csvtopollss("2019datapolls.csv",deltas),dt.date.fromisoformat("2022-05-21")),"Roy Morgan")
# Ys = csvtopollss("2019datapolls.csv",deltas)
# dates,primaryvotes, primaryerrors = aggregatepolls(dt.date.fromisoformat("2016-07-02"),dt.date.fromisoformat("2019-05-18"),results2016,Ys,config)

# Ys = csvtopollss("2022natpolls.csv",deltas)
# dates,primaryvotes, primaryerrors = aggregatepolls(dt.date.fromisoformat("2019-05-18"),dt.date.today(),results2019,Ys,config)

# # print(list(array(primaryvotes).T[-1]))


# plotparty(dates,primaryvotes, primaryerrors,0,Ys)
# plotparty(dates,primaryvotes, primaryerrors,1,Ys)
# plotparty(dates,primaryvotes, primaryerrors,2,Ys)
# plotparty(dates,primaryvotes, primaryerrors,3,Ys)
# plotparty(dates,primaryvotes, primaryerrors,4,Ys)
# plt.show()



