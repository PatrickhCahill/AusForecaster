'''
--- Load the polls
swings, errors = getswingskalmanfilter(theDate,model)

--- Load the seats
seats = csvtoseats()

--- Load the model and the cormatrix
model = tppregression()
rmatrix = cormatrix(seats)
'''
import numpy as np
import math
import os
import pandas as pd
from sklearn import linear_model
import datetime as dt
import kalmanpolls as k
from multiprocessing import Pool

# import cProfile
# import pstats
import time

def normalise(vec):
    return vec/sum(vec)

def makeprimaries(avgprimaries,stds):
    '''For each state (including NAT) this takes the avgprimary votes in that state and randomise them according to the error in std. Then it normalises the vector to sum to 1.'''
    outswings = []
    for statenum, state in enumerate(avgprimaries):
        stateprimaries = []
        for index,val in enumerate(state):
            if index <2:
                stateprimaries.append(min(max(np.random.normal(val,stds[statenum][index]),0.3),0.5))
            elif index==2:
                stateprimaries.append(min(max(np.random.normal(val,stds[statenum][index]),0.05),0.2))
            else:
                stateprimaries.append(min(max(np.random.normal(val,stds[statenum][index]),0.01),0.2))

        outswings.append(normalise(np.array(stateprimaries)))
    return np.array(outswings)

def getxsandys(n,polling_data):
    '''Expects Data to be of the form [Lib,Lab,Greens,ONP,IND,LibTPP,LabTPP] and converts this into the xs which are the primary votes and the ys 
    which are the tpp votes.'''
    xs=[float(i) for i in polling_data.iloc[n][:5]]
    ys=[float(i) for i in polling_data.iloc[n][6:]]
    return xs,ys

def tppregression():
    '''Create the linear regression model from the 2019 data'''
    dir_path = os.path.dirname(os.path.realpath(__file__)).removesuffix("\code")
    polling_data_2019 = pd.read_csv(dir_path+"/polling_data/2019polling.csv")
    x=[]
    y=[]
    for poll in polling_data_2019.index:
        xs,ys=getxsandys(poll,polling_data_2019)
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

def getswings(primaries,model):
    tpps = []
    for state in primaries:
        labortpp = model.intercept_[0]
        for index,party in enumerate(state):
            labortpp += model.coef_[0][index]*party
        tpps.append(labortpp)
    swings = {'natswing':tpps[0]-0.4847,'NSW':tpps[1]-0.4822,'VIC':tpps[2]-0.5314,'QLD':tpps[3]-0.4156,'WA':tpps[4]-0.4445}
    return swings

def gettppserrors(stds,model):
    tpps = []
    for state in stds:
        labortpp = 0
        for index,party in enumerate(state):
            labortpp += abs(model.coef_[0][index])*party
        tpps.append(labortpp)
    dict_errors = {'naterror':tpps[0],'NSW':tpps[1],'VIC':tpps[2],'QLD':tpps[3],'WA':tpps[4]}
    return dict_errors

# Define a seat class
class seat:
    def __init__(self,name,prevResults,state,region,tppcontest):
        self.name = name
        self.prevResults = np.array(prevResults)
        self.state = state
        self.region = region
        self.tppcontest = tppcontest
        self.avgPrev = sum(self.prevResults)/len(self.prevResults)
        self.stdPrev = np.std(self.prevResults)
    def __str__(self):
        return "Seat: "+self.name
    def __repr__(self):
        return str(self.__dict__)

class resolvedSeat:
    def __init__(self,theSeat,outcome):
        self.name = theSeat.name
        self.prevResults = theSeat.prevResults
        self.state = theSeat.state
        self.region = theSeat.region
        self.tppcontest = theSeat.tppcontest
        self.avgPrev = theSeat.avgPrev
        self.stdPrev = theSeat.stdPrev
        self.outcome = outcome
 
        if self.tppcontest=="Yes" and self.outcome > 0.5:
            self.winner = "Labor"
        elif self.tppcontest=="Yes" and self.outcome <= 0.5:
            self.winner = "Coalition"
        else:
            self.winner = "Independent"
        self.simple = self.winner
        if self.tppcontest=="Yes":
            self.simple += ": " + str(round(self.outcome,3))

    def __str__(self):
        return self.simple
    def __repr__(self):
        return str(self.__dict__)        

# Define a function that reads csv data and creates a list of seats
def csvtoseats():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path.removesuffix("\code")+'/historical_data/Indata.csv')
    seats = []
    for i in df.index:
        unparsed = list(df.loc[i])
        name = unparsed[0]
        prevResults = [unparsed[index] for index in range(1,4)]
        state = unparsed[4]
        region = unparsed[5]
        tppcontest = unparsed[6]
        seats.append(seat(name,prevResults,state,region,tppcontest))
    return np.array(seats)

def cormatrix(seats):
    names = [i.name for i in seats]
    result13s = [i.prevResults[0] for i in seats]
    result16s = [i.prevResults[1] for i in seats]
    result19s = [i.prevResults[2] for i in seats]
    
    d = {'result13s':result13s,'result16s':result16s,'result19s':result19s}
    df = pd.DataFrame(data=d,index=names)

    return df.transpose().corr()

def updatemustuff(seatUndecided,seatDecided,rmatrix):
    '''y= r*SDy/SDx (x-xmean)+ymean'''
    return rmatrix[seatDecided.name][seatUndecided.name]*seatUndecided.stdPrev/seatDecided.stdPrev, seatDecided.avgPrev, seatUndecided.avgPrev

def simSeat(swings,aSeat,errors,outcome,index,rmatrix):
    natswing = swings['natswing']
    naterror = errors['naterror']
    try:
        stateswing = swings[aSeat.state]
        stateerror = errors[aSeat.state]
    except:
        # print("Couldn't find " + aSeat.name + "'s location.")
        stateswing = natswing
        stateerror = naterror

    totalswing = (natswing*(1/naterror**2)+stateswing*(1/stateerror**2))/((1/naterror**2)+(1/stateerror**2))
    totalerror = math.sqrt(1/((1/naterror**2)+(1/stateerror**2)))
    if aSeat.region=="Regional":
        regionalswingfactor = 0.8
    elif aSeat.region=="Suburban":
        regionalswingfactor = 0.9
    else:
        regionalswingfactor = 1
    
    totalswing *= regionalswingfactor

    avgSeatmu = aSeat.prevResults[2] + totalswing
    for i in range(0,index):
        factor, mux, muy = updatemustuff(aSeat,outcome[i],rmatrix)
        avgSeatmu += (1/150/3)*factor*(outcome[i].outcome-mux)
    outcomevalue =  np.random.normal(avgSeatmu,totalerror)
    return resolvedSeat(aSeat,outcomevalue)

def simulateelection(swings,seats,errors,rmatrix):
    permuteSeats = np.random.permutation(seats) #This randomly shuffles the seats without changing seats
    outcome = list(range(0,len(permuteSeats)))
    for index,aSeat in enumerate(permuteSeats):
        outcome[index] = simSeat(swings,aSeat,errors,outcome,index,rmatrix)
    return sorted(outcome,key=lambda a: a.name)

def multisimelection(args):
    primaries = makeprimaries(args[0],args[1]) #Or something to this effect
    swings = getswings(primaries,args[2])
    errors = gettppserrors(args[1],args[2])
    return simulateelection(swings,args[3],errors,args[4])

def manysims(num,avgprimaries,stds,seats,model,rmatrix):
    '''
    1. A for loop that writes to the i-th index, will allow for multithreading.
    2. We will simplify calculation and attempt to have a more "functional" approach. Don't change variables that don't have to be changed.
    '''

    results = [0 for i in range(0,num)]
    for i in range(0,num):
        print(i)
        primaries = makeprimaries(avgprimaries,stds) #Or something to this effect
        swings = getswings(primaries,model)
        errors = gettppserrors(stds,model)
        results[i] = simulateelection(swings,seats,errors,rmatrix)
    return results

def multimanysims(num,avgprimaries,stds,seats,model,rmatrix):
    '''
    1. A for loop that writes to the i-th index, will allow for multithreading.
    2. We will simplify calculation and attempt to have a more "functional" approach. Don't change variables that don't have to be changed.
    '''

    # results = [0 for i in range(0,num)]
    args = (avgprimaries,stds,model,seats,rmatrix)
    with Pool(5) as p:
        results = p.map(multisimelection,[args]*num)
    # for i in range(0,num):
    #     results[i] = multisimelection(args)
    return results

def main(num,thedate):
    seats = csvtoseats()
    model = tppregression()
    avgprimaries, stds = k.getswingskalmanfilter(thedate,k.config)
    rmatrix = cormatrix(seats)
    s = multimanysims(num,avgprimaries,stds,seats,model,rmatrix)
    return s

def getfacts(df,num):
    nlab = 0
    nlib = 0
    nind = 0
    plab = 0
    plib = 0
    phung= 0
    for index in range(0,num):
        testlist = df.loc[index]
        labseats= sum([d.winner=="Labor" for d in testlist])
        libseats= sum([d.winner=="Coalition" for d in testlist])
        indseats= sum([d.winner=="Independent" for d in testlist])
        nlab   +=labseats/num
        nlib   +=libseats/num
        nind   +=indseats/num
        if labseats>=76:
            plab += 1/num
        elif libseats>=76:
            plib += 1/num
        else:
            phung+= 1/num
    print(nlab)
    print(nlib)
    print(nind)
    print(plab)
    print(plib)
    print(phung)

def handledata(theDate,df,num):
    dir_path = os.path.dirname(os.path.realpath(__file__)).removesuffix("\code")
    #Probdata
    labseats = []
    libseats = []
    indseats = []
    labwins = []
    libwins = []
    hungwins = []
    tpps = []
    for index in range(0,num):
        testlist = df.loc[index]
        labseats.append(sum([d.winner=="Labor" for d in testlist]))
        libseats.append(sum([d.winner=="Coalition" for d in testlist]))
        indseats.append(sum([d.winner=="Independent" for d in testlist]))
        tpps.append(sum([d.outcome for d in testlist])/151)

        if labseats[-1]>=76:
            labwins.append(1)
            libwins.append(0)
            hungwins.append(0)
        elif libseats[-1]>=76:
            labwins.append(0)
            libwins.append(1)
            hungwins.append(0)
        else:
            labwins.append(0)
            libwins.append(0)
            hungwins.append(1)
    
    nlab =np.mean(labseats)
    nlib =np.mean(libseats)
    nind =np.mean(indseats)
    nlabErorr = 1.96*np.std(labseats)
    nlibErorr = 1.96*np.std(libseats)
    nindErorr = 1.96*np.std(indseats)
    plab =np.mean(labwins)
    plib =np.mean(libwins)
    phung =np.mean(hungwins)
    # plabErorr = 1.96*np.std(labwins)/num
    # plibErorr = 1.96*np.std(libwins)/num
    # phungErorr = 1.96*np.std(hungwins)/num
    tppavg = np.mean(tpps)
    tppError = np.std(tpps)

    probstringlabor = dt.date.isoformat(theDate)+","+"Labor"+","+str(round(plab,2))+",0"
    probstringlib = dt.date.isoformat(theDate)+","+"Coalition"+","+str(round(plib,2))+",0"
    probstringhung = dt.date.isoformat(theDate)+","+"Others"+","+str(round(phung,2))+",0"

    with open(dir_path + "/docs/page_data/testing1.csv",'a') as f:
        f.write("\n"+probstringlabor)
        f.write("\n"+probstringlib)
        f.write("\n"+probstringhung)
    #SeatData
    seatstringlabor = dt.date.isoformat(theDate)+","+"Labor"+","+str(round(nlab,1))+","+str(round(nlabErorr,1))
    seatstringlib = dt.date.isoformat(theDate)+","+"Coalition"+","+str(round(nlib,1))+","+str(round(nlibErorr,1))
    seatstringothers = dt.date.isoformat(theDate)+","+"Others"+","+str(round(nind,1))+","+str(round(nindErorr,1))

    with open(dir_path + "/docs/page_data/testing2.csv",'a') as f:
        f.write("\n"+seatstringlabor)
        f.write("\n"+seatstringlib)
        f.write("\n"+seatstringothers)

    #TppData
    tppstringlabor = dt.date.isoformat(theDate)+","+"Labor"+","+str(round(tppavg,3))+","+str(tppError)
    tppstringlib = dt.date.isoformat(theDate)+","+"Coalition"+","+str(round(1-tppavg,3))+","+str(tppError)

    with open(dir_path + "/docs/page_data/testing3.csv",'a') as f:
        f.write("\n"+tppstringlabor)
        f.write("\n"+tppstringlib)

def backrun():
    startdate = '2020-01-01'
    rundate = dt.date.fromisoformat(startdate)
    delta = dt.timedelta(days=7)
    while rundate <= dt.date.today():
        print(dt.date.isoformat(rundate))
        num = 10000
        data = main(num,rundate)
        names = [aSeat.name for aSeat in data[0]]
        df = pd.DataFrame(data, columns=names)
        handledata(rundate,df,num)
        rundate += delta


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__)).removesuffix("\code")
    df = pd.read_csv(dir_path + "/docs/page_data/testing3.csv")
    for index in range(6,len(df)):
        df.at[index,'tpp'] = round((1/3)*(df.loc[index-6].tpp+df.loc[index-3].tpp+df.loc[index].tpp),3)
    
    df.to_csv(dir_path + "/docs/page_data/testing6.csv")

    # with cProfile.Profile() as pr:
    #         data = main(100)
    #         names = [aSeat.name for aSeat in data[0]]
    #         df = pd.DataFrame(data, columns=names)
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

