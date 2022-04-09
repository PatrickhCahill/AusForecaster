'''
model.py is a library. model.py only contains functions that relate to the direct modelling. See regression_model.py for functions that relate
to the regression analysis. The typical way to interact with this library to is two-fold.

Use multisaveandrun(model_type,number of sims) which will automatically simulate the results and write them to a file.
Use multisaveandrun(specific data file to simulate on) which can the specify the datafile.

'''
import os
import sys
import pandas as pd
from pandas import DataFrame
import numpy as np
import math
from multiprocessing import Process, Manager

import cProfile
import pstats

### Makes sure the model knows where it is being stored and then locates the polling_data, historical_data, and the regression_model

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path += [dir_path]
import regression_model as regrmodel
DATAFILE = dir_path.removesuffix("\code")+'/historical_data/Indata.csv'



def getdivisions(location=DATAFILE):
    '''Takes the datafile which stores division data in a csv and transforms it into a pandas dataframe'''
    division_data = pd.read_csv(location,index_col=["Division"])
    #division_data.transose()
    return division_data
#DIVISIONDATA is the default dataframe and shouldn't be changed unless playing around with other data :)
DIVISIONDATA = getdivisions(DATAFILE).sample(frac = 1)

def multipartyseat():
    '''This will eventually be a function that runs in seats which are not TPP contests. i.e seats where Greens, ONP, SFF, UAP, or independents have a chance of winning.'''
    print("Multiparty Seat - Not yet modelled")

def getcormatrix(division_data=DIVISIONDATA,columns=["Result19","Result16","Result13"]):
    '''This generates the correlation matrix of the divisions - which is step 2 in the readme.md'''
    df = division_data.copy()
    for i in list(df.columns):
        if i not in columns:
            df = df.drop(i,axis=1)
    return df.transpose().corr()

#Default correlation matrix    
CORMATRIX = getcormatrix()

def regionalswingfactor(seat,divisiondata=DIVISIONDATA):
    '''As per https://openresearch-repository.anu.edu.au/bitstream/1885/125156/4/b12292035_Cunningham_R.pdf, swings are generally larger in municipal areas.
    This is represented by the regionswingfactor which at the moment is a hardcoded value that reduces swing. More sophisticated models will be added later.'''
    if divisiondata.loc[seat]["Region"]=="Regional":
        return 0.8
    elif divisiondata.loc[seat]["Region"] == "Suburban":
        return 0.9
    else:
        return 1

def getstateweight(seat,divisiondata=DIVISIONDATA):
    '''Returns a weight for state polls based off the number of polls for that state. Ranges from 0 to 5. Will need separate csv with polling data by national and by state (with sample sizes)'''
    #Currently we say that states polls are weighted 40% and federal polls are weighted 60%
    return 0.4

def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            cache[args] = func(*args)
            return cache[args]
    return wrapper
def getseatdatastd(seat,divisiondata=DIVISIONDATA):
    '''This gets the seats standard deviation over the past three elections which is then used in conjunction with the correlation matrix
    in order to calculate the linear regression between more seats.'''
    return np.std([divisiondata.loc[seat]["Result19"],divisiondata.loc[seat]["Result16"],divisiondata.loc[seat]["Result13"]])
getseatdatastd=memoize(getseatdatastd)

def getcorfactor(changingseat,setseat,r,divisiondata=DIVISIONDATA ):
    '''For an updating simulation this returns the strength of the correlation factor. 
    Current model reduces the strength of negative correlations.
    If seats are in different states then the correlation factor is further reduced.'''
    
    #Corweight is initially weak, set to 0.1. Then further weakened.
    corweight = 0.01
    if r<= 0:
        corweight *= 0
    if divisiondata.loc[setseat]["State"] != divisiondata.loc[changingseat]["State"]:
        corweight *= 0.5
    return corweight
getcorfactor=memoize(getcorfactor)
def updatemu(mu,changingseat,setseat,decidedseatframe,cormatrix=CORMATRIX,divisiondata=DIVISIONDATA):
    '''Updates the mu of seat based off the correlation between the changing seat and the set seat'''
    seat = decidedseatframe.loc[setseat]
    seatdata = divisiondata.loc[setseat]
    changingseatdata = divisiondata.loc[changingseat]
    r=cormatrix[changingseat][setseat]
    
    rsdysdx = min(getseatdatastd(changingseat)/getseatdatastd(setseat),1)*r
    cormu1 = np.mean([seatdata["Result19"],seatdata["Result16"],seatdata["Result13"]])
    cormu2 = np.mean([changingseatdata["Result19"],changingseatdata["Result16"],changingseatdata["Result13"]])
    corpredict = rsdysdx*(seat["predResult"]-cormu1)+cormu2

    corweight = getcorfactor(changingseat,setseat,r)

    return max(min((1-corweight)*mu + corweight*corpredict,1),0)
regrmodel.getpollpreds=memoize(regrmodel.getpollpreds)
def simseat(seat:str,updating: bool,decidedseatframenotcopied,divisiondata=DIVISIONDATA,cormatrix= CORMATRIX):
    '''Simulates the election result of seat. Takes the seat to be simulate and the list of seats already decided'''
    decidedseatframe = decidedseatframenotcopied.copy()
    #Check if seat is in decidedseat list
    if seat in decidedseatframe: return decidedseatframe
    seatfacts =divisiondata.loc[seat]
    stateswings = regrmodel.getpollpreds()
    #Check if Green/Independents are competitive in this seat.
    #if divisiondata.loc[seat]["2-Party-Contest"]=="No": return multipartyseat()
    
    # If checks are passed then proceeds to calculate the expected result
    # First we find mu, the expected result without taking seat correlations into account. This is based national environment, the seat's state and regionality of the seat
    r19=divisiondata.loc[seat]["Result19"]
    if seatfacts["State"]=="TAS":
        mu =  r19 + regionalswingfactor(seat)*(stateswings["AUS"])
    elif seatfacts["State"]=="ACT":
        mu =  r19 + regionalswingfactor(seat)*(stateswings["AUS"])
    elif seatfacts["State"]=="NT":
        mu =  r19 + regionalswingfactor(seat)*(stateswings["AUS"])
    else:
        mu =  r19 + regionalswingfactor(seat)*((1-getstateweight(seat))*stateswings["AUS"] + getstateweight(seat)*stateswings[seatfacts["State"]])
    sigma = 0.05 #This is the uncertainty in the mu. Currently hardcoded to be twice the margin of error on polling average. Will implement more sophisticated techniques later
    

    # Now we check if this is a non-correlationg run using the updating input of this function
    if not updating or len(decidedseatframe)==0:
        #We return the appended decidedseat list by simulating a random election. np.random.normal randomly chooses the election Result from a normal distribution that has mean mu and std sigma.
        Result = np.random.normal(mu,sigma,1)[0]
        appendage = DataFrame([[seat,seatfacts["Result19"],mu,sigma,Result,Result - seatfacts["Result19"],seatfacts["2-Party-Contest"]]],columns=["Division","Result19","mu","sigma","predResult","swing","2-Party-Contest"]).set_index("Division")
        return decidedseatframe.append(appendage)

    # The function is updating. Hence, we need to generate take the cormatrix.
    for i in list(decidedseatframe.index):
        mu = updatemu(mu,seat,i,decidedseatframe)
    Result = min(max(np.random.normal(mu,sigma,1)[0],0),1)
    appendage = DataFrame([[seat,seatfacts["Result19"],mu,sigma,Result,Result - seatfacts["Result19"],seatfacts["2-Party-Contest"]]],columns=["Division","Result19","mu","sigma","predResult","swing","2-Party-Contest"]).set_index("Division")
    
    return decidedseatframe.append(appendage)
def simulateelection(updating:bool,divisiondata=DIVISIONDATA, cormatrix=CORMATRIX)->DataFrame:
    divisiondata = divisiondata.sample(frac=1)
    '''Simulates An Entire Election. Updating boolean determines whether to include correlation caclulations or not'''
    decidedseatframe = DataFrame(columns=["Division","Result19","mu","sigma","predResult","swing","2-Party-Contest"]).set_index("Division")
    for seat in list(divisiondata.index):
        decidedseatframe = simseat(seat,updating,decidedseatframe,divisiondata,cormatrix)
    return decidedseatframe
def run(updating:bool,num_sims:int,divisiondata=DIVISIONDATA,cormatrix=CORMATRIX):
    electionsimulationslist = []
    for i in range((num_sims)):
        print(i)
        electionsimulationslist.append(simulateelection(updating, divisiondata,cormatrix)) #Contains All Electionsimulations
    


    winsframe = DataFrame(columns = ["nLabor","nLib","nThird","Winner"])
    for sim in electionsimulationslist:
        liberalseats = 0
        laborseats = 0
        thirdpartyseats = 0
        for seat in list(sim.index):
            seatfacts = sim.loc[seat]
            if seatfacts["2-Party-Contest"]=="Yes" and seatfacts["predResult"]>=0.5: laborseats += 1 
            elif seatfacts["2-Party-Contest"]=="Yes" and seatfacts["predResult"]<0.5: liberalseats += 1 
            elif seatfacts["2-Party-Contest"]=="No": thirdpartyseats += 1
            else: laborseats += 1
        if laborseats >=76:
            winner="Labor"
        elif liberalseats >= 76:
            winner="Coalition"
        else:
            winner = "Hung Parliament"
        simwinframe = DataFrame([[laborseats,liberalseats,thirdpartyseats,winner]],columns = ["nLabor","nLib","nThird","Winner"])
        winsframe = winsframe.append(simwinframe)




    averageframe = DataFrame(columns=["Division","Incumbent","Result","Margin","predProb","predResult","predMargin","predSwing","predWinner","2-Party-Contest"]).set_index("Division")
    for seat in list(electionsimulationslist[0].index):
        seatfacts = sim.loc[seat]
        if seatfacts["2-Party-Contest"]=="Yes":
            Result19= seatfacts["Result19"]
            if Result19 >= 0.5:
                incumbent = "Labor"
                margin =abs(Result19-0.5)
            elif Result19 <0.5 and seatfacts["2-Party-Contest"]=="Yes":
                incumbent = "Coalition"
                margin =abs(Result19-0.5)
            elif seat=="Melbourne":
                incumbent = "Greens"
                margin =-1
            else:
                pass
                incumbent = "Independent"
                margin =-1




            averageResult= np.mean([seatfacts["predResult"] for sim in electionsimulationslist])
            averageswing= np.mean([seatfacts["swing"] for sim in electionsimulationslist])
            predmargin = abs(0.5-averageResult)
            contestval = electionsimulationslist[0].loc[seat]["2-Party-Contest"]

            if averageResult >0.5:
                predWinner ="Labor"
            elif averageResult <= 0.5 and contestval == "Yes":
                predWinner ="Coalition"
            elif seat == "Melbourne":
                predWinner = "Greens"
            else:
                predWinner = "Independent"

            if seatfacts["mu"] >=0.5:
                predprob = 1/2 - 1/2 * math.erf((0.5-seatfacts["mu"])/(seatfacts["sigma"]*math.sqrt(2)))
            elif seatfacts["mu"] <0.5 and seatfacts["2-Party-Contest"]=="Yes":
                predprob = 1-(1/2 - 1/2 * math.erf((0.5-seatfacts["mu"])/(seatfacts["sigma"]*math.sqrt(2))))
            else:
                predprob = -1

            average_seat_frame = DataFrame([[seat,incumbent,Result19,margin,predprob,averageResult,predmargin,averageswing,predWinner,contestval]],columns=["Division","Incumbent","Result","Margin","predProb","predResult","predMargin","predSwing","predWinner","2-Party-Contest"]).set_index("Division")
            averageframe = averageframe.append(average_seat_frame)
    
    
    return averageframe, winsframe
def getchangesframe(averageframe):
    changesframe = averageframe.copy()
    for seat in list(averageframe.index):
        seatfacts = averageframe.loc[seat]
        if seatfacts["Incumbent"] == seatfacts["predWinner"]:
            changesframe = changesframe.drop(seat,axis=0)
    return changesframe
def saveandrun(updating:bool,num_sims:int)->None:
    averageframe, winsframe = run(updating,num_sims)
    if updating:
        getchangesframe(averageframe).to_csv(dir_path+'/OutData/UpdatingChanges.csv')
        averageframe.to_csv(dir_path+'/OutData/UpdatingOutAverages.csv')
        winsframe.to_csv(dir_path+'/OutData/UpdatingOutWins.csv')
    else:
        getchangesframe(averageframe).to_csv(dir_path+'/OutData/SimpleChanges.csv')
        averageframe.to_csv(dir_path+'/OutData/SimpleOutAverages.csv')
        winsframe.to_csv(dir_path+'/OutData/SimpleOutWins.csv')


def processingrun(updating:bool,electionsimulationslist:list,x:int):
    electionsimulationslist.append(simulateelection(updating, DIVISIONDATA,CORMATRIX)) #Contains All Electionsimulations


def multirun(updating:bool,num_sims:int):
    electionsimulationslist = []
    num_cycles = math.floor(num_sims/8)
    for i in range(num_cycles):
        with Manager() as manager:
            multiproclist = manager.list()  # <-- can be shared between processes.
            processes = []
            for x in range(8):
                p = Process(target=processingrun, args=(updating,multiproclist,x))  # Passing the list
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            additionlist = multiproclist[:]
            electionsimulationslist += additionlist
    winsframe = DataFrame(columns = ["nLabor","nLib","nThird","Winner"])
    for sim in electionsimulationslist:
        liberalseats = 0
        laborseats = 0
        thirdpartyseats = 0
        for seat in list(sim.index):
            seatfacts = sim.loc[seat]
            if seatfacts["2-Party-Contest"]=="Yes" and seatfacts["predResult"]>=0.5: laborseats += 1 
            elif seatfacts["2-Party-Contest"]=="Yes" and seatfacts["predResult"]<0.5: liberalseats += 1 
            elif seatfacts["2-Party-Contest"]=="No": thirdpartyseats += 1
            else: laborseats += 1
        if laborseats >=76:
            winner="Labor"
        elif liberalseats >= 76:
            winner="Coalition"
        else:
            winner = "Hung Parliament"
        simwinframe = DataFrame([[laborseats,liberalseats,thirdpartyseats,winner]],columns = ["nLabor","nLib","nThird","Winner"])
        winsframe = winsframe.append(simwinframe)

        averageframe = DataFrame(columns=["Division","Incumbent","Result","Margin","predProb","predResult","predMargin","predSwing","predWinner","2-Party-Contest"]).set_index("Division")
    for seat in list(electionsimulationslist[0].index):
        seatfacts = sim.loc[seat]
        if seatfacts["2-Party-Contest"]=="Yes":
            Result19= seatfacts["Result19"]
            if Result19 >= 0.5:
                incumbent = "Labor"
                margin =abs(Result19-0.5)
            elif Result19 <0.5 and seatfacts["2-Party-Contest"]=="Yes":
                incumbent = "Coalition"
                margin =abs(Result19-0.5)
            elif seat=="Melbourne":
                incumbent = "Greens"
                margin =-1
            else:
                pass
                incumbent = "Independent"
                margin =-1
            averageResult= np.mean([seatfacts["predResult"] for sim in electionsimulationslist])
            averageswing= np.mean([seatfacts["swing"] for sim in electionsimulationslist])
            predmargin = abs(0.5-averageResult)
            contestval = electionsimulationslist[0].loc[seat]["2-Party-Contest"]

            if averageResult >0.5:
                predWinner ="Labor"
            elif averageResult <= 0.5 and contestval == "Yes":
                predWinner ="Coalition"
            elif seat == "Melbourne":
                predWinner = "Greens"
            else:
                predWinner = "Independent"

            if seatfacts["mu"] >=0.5:
                predprob = 1/2 - 1/2 * math.erf((0.5-seatfacts["mu"])/(seatfacts["sigma"]*math.sqrt(2)))
            elif seatfacts["mu"] <0.5 and seatfacts["2-Party-Contest"]=="Yes":
                predprob = 1-(1/2 - 1/2 * math.erf((0.5-seatfacts["mu"])/(seatfacts["sigma"]*math.sqrt(2))))
            else:
                predprob = -1

            average_seat_frame = DataFrame([[seat,incumbent,Result19,margin,predprob,averageResult,predmargin,averageswing,predWinner,contestval]],columns=["Division","Incumbent","Result","Margin","predProb","predResult","predMargin","predSwing","predWinner","2-Party-Contest"]).set_index("Division")
            averageframe = averageframe.append(average_seat_frame)
    return winsframe,averageframe
def multisaveandrun(updating:bool,num_sims:int)->None:
    winsframe,averageframe = multirun(updating,num_sims)
    if updating:
        getchangesframe(averageframe).to_csv(dir_path+'/OutData/MultiUpdatingChanges.csv')
        averageframe.to_csv(dir_path+'/OutData/MultiUpdatingOutAverages.csv')
        winsframe.to_csv(dir_path+'/OutData/MultiUpdatingOutWins.csv')
    else:
        getchangesframe(averageframe).to_csv(dir_path+'/OutData/MultiSimpleChanges.csv')
        averageframe.to_csv(dir_path+'/OutData/MultiSimpleOutAverages.csv')
        winsframe.to_csv(dir_path+'/OutData/MultiSimpleOutWins.csv')

    

