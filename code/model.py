from asyncio import run
import os
import datetime as dt
from re import S
from unittest.mock import NonCallableMagicMock
import pandas as pd
from sklearn import datasets, linear_model
from random import shuffle
from numpy.random import normal
from numpy import std
from math import floor
# Define a poll class
class poll:
    def __init__(self,theDate,labor,liberal,greens,onp,ind):
        self.theDate = dt.date.fromisoformat(theDate)
        self.labor = labor
        self.liberal = liberal
        self.greens = greens
        self.onp = onp
        self.ind = ind
    def __str__(self):
        return str(self.__dict__)
    def __rpr__(self):
        return str(self.__dict__)

# Define a function that reads csv data and creates a list of polls
def csvtopollss():
    dir_path = os.path.dirname(os.path.realpath(__file__)).removesuffix("\code")
    pollingdata =pd.read_csv(dir_path+"/polling_data/testingdata.csv")
    natpolls = [poll(*tuple(pollingdata.loc[i])) for i in pollingdata.index]
    
    pollingdata =pd.read_csv(dir_path+"/polling_data/testingdatansw.csv")
    nswpolls = [poll(*tuple(pollingdata.loc[i])) for i in pollingdata.index]

    pollingdata =pd.read_csv(dir_path+"/polling_data/testingdatavic.csv")
    vicpolls = [poll(*tuple(pollingdata.loc[i])) for i in pollingdata.index]   

    pollingdata =pd.read_csv(dir_path+"/polling_data/testingdataqld.csv")
    qldpolls = [poll(*tuple(pollingdata.loc[i])) for i in pollingdata.index]    

    pollingdata =pd.read_csv(dir_path+"/polling_data/testingdatawa.csv")
    wapolls = [poll(*tuple(pollingdata.loc[i])) for i in pollingdata.index]
    return [natpolls,nswpolls,vicpolls,qldpolls,wapolls]

# Handles 2019data for pollregression()
def getxsandys(n,polling_data):
    '''Expects Data to be of the form [Lib,Lab,Greens,ONP,IND,LibTPP,LabTPP] and converts this into the xs which are the primary votes and the ys 
    which are the tpp votes.'''
    xs=[float(i) for i in polling_data.iloc[n][:5]]
    ys=[float(i) for i in polling_data.iloc[n][6:]]
    return xs,ys

# Creates a regression model using 2019 data to find preference flows.
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

# Takes a poll and a model and calculates predicted tpp results
def labtpp(poll,model):
    labor = model.intercept_[0]
    labor += model.coef_[0][0]*poll.liberal
    labor += model.coef_[0][1]*poll.labor
    labor += model.coef_[0][2]*poll.greens
    labor += model.coef_[0][3]*poll.onp
    labor += model.coef_[0][4]*poll.ind
    return labor

# Finds the average for a list of polls of labtpp(poll,model)
def predlab(currentDate,polls,model):
    polllist = []
    for index, value in enumerate(polls):
        if (currentDate-value.theDate).days >=0:
            polllist.append(value)
    if len(polllist)==0:
        polllist.append(polls[0])

    labtpps = [labtpp(polll,model) for polll in polllist]
    dts = [((currentDate-polll.theDate).days+21)/7 for polll in polllist]
    oneondts = [1/dt for dt in dts]
    weight = 1/sum(oneondts)
    weights = [weight*oneondt for oneondt in oneondts]
    output = 0
    for index, value in enumerate(labtpps):
        output += weights[index]*value
    return output

# Define a seat class
class seat:
    def __init__(self,name,prevResults,state,region,tppcontest):
        self.name = name
        self.prevResults = prevResults
        self.state = state
        self.region = region
        self.tppcontest = tppcontest
        self.avgPrev = sum(self.prevResults)/len(self.prevResults)
        self.predResult = prevResults[2] #2019 Result
        self.avgPred = 0
    def __str__(self):
        return "Seat: "+self.name
    def __repr__(self):
        return str(self.__dict__)
    def reset(self): 
        self.predResult = self.prevResults[2]



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
    return seats

# Takes a list of seats and creates a cormatrix
def cormatrix(seats):
    names = [i.name for i in seats]
    result13s = [i.prevResults[0] for i in seats]
    result16s = [i.prevResults[1] for i in seats]
    result19s = [i.prevResults[2] for i in seats]
    
    d = {'result13s':result13s,'result16s':result16s,'result19s':result19s}
    df = pd.DataFrame(data=d,index=names)

    return df.transpose().corr()

def getswings(currentDate,pollss,model):
    swings = [predlab(currentDate,polls,model) for polls in pollss]
    swings = {'natswing':swings[0]-0.4847,'nswswing':swings[1]-0.4822,'vicswing':swings[2]-0.5314,'qldswing':swings[3]-0.4156,'waswing':swings[4]-0.5071}
    return swings

def simSeat(division,swings):
    natswing = swings['natswing']
    if division.state=="NSW":
        stateswing = swings['nswswing']
    elif division.state=="VIC":
        stateswing = swings['vicswing']
    elif division.state=="QLD":
        stateswing = swings['qldswing']
    elif division.state=="WA":
        stateswing = swings['waswing']
    else:
        stateswing = natswing
    
    stateweight = 0.4

    totalSwing = stateweight*stateswing+(1-stateweight)*natswing
    if division.region=="Regional":
        regionalswingfactor = 0.8
    elif division.region=="Suburban":
        regionalswingfactor = 0.9
    else:
        regionalswingfactor = 1
    totalSwing *= regionalswingfactor

    division.predResult += totalSwing
    sigma = 0.1
    division.predResult = normal(division.predResult,sigma,1)[0]

def updatemus(index,division,seats,rmatrix):
    for i in range(index+1,len(seats)):
        updatingDivision = seats[i]
        sdysdx = std(updatingDivision.prevResults)/std(division.prevResults)
        r = rmatrix[division.name][updatingDivision.name]
        rsdysdx = r*sdysdx
        predChange = rsdysdx*(division.predResult-division.avgPrev)+updatingDivision.avgPrev
        
        if rsdysdx>= 0:
            corweight = 0.01
        else:
            corweight = 0

        updatingDivision.predResult = (1-corweight)*updatingDivision.predResult + corweight*predChange

def simElection(swings,seats,rmatrix):
    shuffle(seats)
    for index, division in enumerate(seats):
        simSeat(division,swings)
        updatemus(index,division,seats,rmatrix)
    return seats

def simfacts(seats):
    
    nLabor = 0
    nLib = 0
    nThird = 0
    for division in seats:
        if division.predResult>=0.5 and division.tppcontest=='Yes':
            nLabor +=1
        elif division.predResult<0.5 and division.tppcontest=='Yes':
            nLib +=1
        elif division.tppcontest=='No':
            nThird +=1
    if nLabor >= 76:
        winner='Labor'
    elif nLib >= 76:
        winner='Coalition'
    else:
        winner='Hung'       
    d = {'nLabor':nLabor,'nLib':nLib,'nThird':nThird,'Winner':winner}
    return d

def main(theDate,num):
    model = tppregression()
    pollss = csvtopollss()
    seats = csvtoseats()
    rmatrix = cormatrix(seats)
    swings = getswings(theDate,pollss,model)
    nLabor = []
    nLib = []
    nThird = []
    winner = []
    for iter in range(0,num):
        print(iter)
        simElection(swings,seats,rmatrix)
        facts = simfacts(seats)

        nLabor.append(facts['nLabor'])
        nLib.append(facts['nLib'])
        nThird.append(facts['nThird'])
        winner.append(facts['Winner'])
        for division in seats:
            division.avgPred += division.predResult/num
            division.reset()
    d = {'nLabor':nLabor,'nLib':nLib,'nThird':nThird,'Winner':winner}
    df = pd.DataFrame(d)
    return theDate,df,seats

def handledata(theDate,df,seats):
    dir_path = os.path.dirname(os.path.realpath(__file__)).removesuffix("\code")
    #Probdata
    labcolumn =  list(df.loc[:,"nLabor"])
    labprob = sum(i>=76 for i in labcolumn)/len(labcolumn)

    libcolumn =  list(df.loc[:,"nLib"])
    libprob = sum(i>=76 for i in libcolumn)/len(libcolumn)
    hungprob = 1-labprob-libprob

    probs = [dt.date.isoformat(theDate),round(100*labprob),round(100*libprob),round(100*hungprob)]
    probstring = ','.join([str(i) for i in probs])
    with open(dir_path + "/docs/page_data/timechart1data.csv",'a') as f:
        f.write("\n"+probstring)

    #SeatData
    labseats = sum(i for i in labcolumn)/len(labcolumn)
    libseats = sum(i for i in libcolumn)/len(libcolumn)
    hungseats = 151-labseats-libseats
    seatslist = [dt.date.isoformat(theDate),round(labseats),round(libseats),round(hungseats)]
    seatsstring = ','.join([str(i) for i in seatslist])
    with open(dir_path + "/docs/page_data/timechart2data.csv",'a') as f:
        f.write("\n"+seatsstring)
    #TppData
    labtpps = [division.avgPred for division in seats]
    labtpp = sum(labtpps)/len(labtpps)
    libtpp = 1-labtpp

    tpplist = [dt.date.isoformat(theDate),round(labtpp*100,1),round(libtpp*100,1)]
    tppstring = ','.join([str(i) for i in tpplist])
    with open(dir_path + "/docs/page_data/timechart3data.csv",'a') as f:
        f.write("\n"+tppstring)
    #Beedata
    df.to_csv(dir_path+"/docs/page_data/beedata.csv")

def backrun():
    startdate = '2020-01-01'
    rundate = dt.date.fromisoformat(startdate)
    delta = dt.timedelta(days=7)
    while rundate <= dt.date.today():
        theDate,df,seats = main(rundate,100)
        handledata(theDate,df,seats)
        rundate += delta

def senatestate(currentDate,pollss,state):
    pollsaus_unparsed = pollss[0]
    if state == 'NSW':
        state=1
    elif state == 'VIC':
        state=2
    elif state == 'QLD':
        state=3
    elif state == 'WA':
        state=2
    else:
        state=0
    pollsstate_unparsed = pollss[state]
    
    pollsaus = []
    for index, value in enumerate(pollsaus_unparsed):
        if (currentDate-value.theDate).days >=0:
            pollsaus.append(value)
    if len(pollsaus)==0:
        pollsaus.append(pollsaus_unparsed[0])
    
    dtsaus = [((currentDate-polll.theDate).days+21)/7 for polll in pollsaus]
    oneondtsaus = [1/dt for dt in dtsaus]
    weightaus = 1/sum(oneondtsaus)
    weightsaus = [weightaus*oneondt for oneondt in oneondtsaus]

    aus_avg = [0,0,0,0,0]
    for index, value in enumerate(pollsaus):
        aus_avg[0]+=value.labor*weightsaus[index]
        aus_avg[1]+=value.liberal*weightsaus[index]
        aus_avg[2]+=value.greens*weightsaus[index]
        aus_avg[3]+=value.onp*weightsaus[index]
        aus_avg[4]+=value.ind*weightsaus[index]

    pollsstate = []
    for index, value in enumerate(pollsstate_unparsed):
        if (currentDate-value.theDate).days >=0:
            pollsstate.append(value)
    if len(pollsstate)==0:
        pollsstate.append(pollsstate_unparsed[0])

    dtsstate = [((currentDate-polll.theDate).days+21)/7 for polll in pollsstate]
    oneondtsstate = [1/dt for dt in dtsstate]
    weightstate = 1/sum(oneondtsstate)
    weightsstate = [weightstate*oneondt for oneondt in oneondtsstate]

    state_avg = [0,0,0,0,0]
    for index, value in enumerate(pollsstate):
        state_avg[0]+=value.labor*weightsstate[index]
        state_avg[1]+=value.liberal*weightsstate[index]
        state_avg[2]+=value.greens*weightsstate[index]
        state_avg[3]+=value.onp*weightsstate[index]
        state_avg[4]+=value.ind*weightsstate[index]



    nsw2019 = [0.3456,0.4254,0.0871,0.0131,0.128]
    aus2019 = [0.3334,0.4144,0.104,0.054,0.094]
    vic2019 = [0.3686,0.3858,0.1189,0.0095,0.117]
    qld2019 = [0.437,0.2668,0.1032,0.0886,0.104]
    wa2019 = [0.4522,0.2980,0.1162,0.0531,0.0805]
    results19 = [aus2019,nsw2019,vic2019,qld2019,wa2019]
    state2019 = results19[state]

    swingaus = [aus_avg[i]-aus2019[i] for i in range(len(aus2019))]
    swingstate = [state_avg[i]-state2019[i] for i in range(len(aus2019))]

    averagedswings = [0.6*swingaus[i]+0.4*swingstate[i] for i in range(len(swingstate))]
    prednsw = [averagedswings[i]+state2019[i] for i in range(len(state2019))]
    return(prednsw)

def senatemodel(currentDate):
    pollss = csvtopollss()
    # This is 2019 data for testing. Model is correct within one seat.
    # auspoll = poll(*(dt.date.today().isoformat(),0.3334,0.4144,0.104,0.01,0.14))
    # nswpoll =poll(*(dt.date.today().isoformat(),0.3456,0.4254,0.0871,0.0131,0.128))
    # vicpoll =poll(*(dt.date.today().isoformat(),0.3686,0.3858,0.1189,0.0095,0.117))
    # qldpoll =poll(*(dt.date.today().isoformat(),0.267,0.437,0.1032,0.086,0.106))
    # wapoll =poll(*(dt.date.today().isoformat(),0.2980,0.4522,0.1162,0.0541,0.78))
    # pollss = [[auspoll],[nswpoll],[vicpoll],[qldpoll],[wapoll]]

    states = ["NSW","VIC","QLD","WA","SA","TAS"]
    stateresults = [senatestate(currentDate,pollss,state) for state in states]
    quota = 1/6
    guaranteedquotas = [[floor(party/quota) for party in state] for state in stateresults]

    leftovers = [[(party/quota)%1 for party in state] for state in stateresults]
    
    for index,state in enumerate(leftovers):
        while sum(guaranteedquotas[index])<6:
            if index!=4:
                state[4]=0
            party = state.index(max(state))
            guaranteedquotas[index][party]+=1
            state[party] = 0
    prediction = [0,0,0,0,0]
    for state in guaranteedquotas:
        for index, party in enumerate(state):
            prediction[index]+=party
    return prediction

today = dt.date.today()
theDate, df, seats = main(today,100)
handledata(theDate, df, seats)