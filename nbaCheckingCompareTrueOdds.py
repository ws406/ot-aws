import json
import time
import pandas as pd
import numpy as np
import math
import collections
import statistics
from numpy import matrix
from numpy import array
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoLars
from sklearn.svm import SVC, LinearSVC
from scipy import stats
import random

file_header = "/home/wyao/workspace/ot-aws-new/data/basketball_all_odds_data/"

from src.win007.observers.same_direction.nbaQualification_check_test_efficiency import QualificationCheck

roundsPnl = {}
allRoundPnl = []
allQualifiedGames = {}
topPercent = 1.0
bottomPercent = 0.02
myLookbackTime = 0 * 60 + 30 * 60
exchangeReturnRate = 0.96
method = []
method.append('Method1')

compareBookie = []
#compareBookie.append('pinnacle')
#compareBookie.append('bet365')
#compareBookie.append('BWin')
#compareBookie.append('ladbroke')
#compareBookie.append('easybet')
#compareBookie.append('SNAI')
#compareBookie.append('coral')
#compareBookie.append('will_hill')
#compareBookie.append('Macauslot')
#compareBookie.append('Expekt')
#compareBookie.append('skybet')
#compareBookie.append('betvictor')
#compareBookie.append('sb')
#compareBookie.append('5Dimes')
#compareBookie.append('boylesports')

compareBookie.append('Betfair')

#benchmarkBookie = 'pinnacle'
benchmarkBookie = 'bet365'
#benchmarkBookie = 'will_hill'
#benchmarkBookie = 'Macauslot'

def FindProbWithOffsetTime(game_data, bookie, lookbackTime):
    game_data['probabilities'][bookie][str(game_data['kickoff'])] = list(collections.OrderedDict(sorted(game_data['probabilities'][bookie].items())).values())[-1]
    matchInSeq = collections.OrderedDict(sorted(game_data['probabilities'][bookie].items()))
    #print(game_data['game_id'], matchInSeq)
    kickoffTime = int(game_data['kickoff'])
    lastRecord = []
    lastRecord.append(0)
    for timeStr, prob in matchInSeq.items():
        if timeStr == "final" or timeStr == "open":
            continue
        time = int(float(timeStr))
        if time <= kickoffTime - lookbackTime:
            if time > lastRecord[0]:
                lastRecord[0] = time
    if lastRecord[0] != 0:
        return game_data['probabilities'][bookie][str(int(lastRecord[0]))]
    else:
        return None

def FindOddsWithOffsetTime(game_data, bookie, lookbackTime):
    game_data['odds'][bookie][str(int(game_data['kickoff']))] = list(collections.OrderedDict(sorted(game_data['odds'][bookie].items())).values())[-1]
    matchInSeq = collections.OrderedDict(sorted(game_data['odds'][bookie].items()))
    kickoffTime = int(game_data['kickoff'])
    lastRecord = []
    lastRecord.append(0)
    for timeStr, prob in matchInSeq.items():
        if timeStr == "final" or timeStr == "open":
            continue
        time = int(float(timeStr))
        if time <= kickoffTime - lookbackTime:
            if time > lastRecord[0]:
                lastRecord[0] = time
    #print(game_data['game_id'], matchInSeq, lastRecord[0])
    if lastRecord[0] != 0:
        return game_data['odds'][bookie][str(int(lastRecord[0]))]
    else:
        return None

def LoadData(file_name):
    #print("Loading ", file_name)
    with open(file_name) as json_file:
        allMatches = {}
        matches = json.load(json_file)
        for match in matches:
            #time = match['kickoff'] + match['home_team_id']
            #allMatches[float(time)] = match
            allQualifiedGames[int(match['game_id'])] = match

def Method1(match, myList, lookbackTime):
    benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][benchmarkBookie].items())).values())[-1]
    myList.append(float(benchmarkOdds['1']))
    myList.append(float(benchmarkOdds['2']))
    benchmarkProb = list(collections.OrderedDict(sorted(match['probabilities'][benchmarkBookie].items())).values())[-1]
    myList.append(float(benchmarkProb['1']))
    myList.append(float(benchmarkProb['2']))

def Method2(match, myList, lookbackTime):
    method[0] = 'Method2'
    #benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][benchmarkBookie].items())).values())[-1]
    benchmarkOdds = FindOddsWithOffsetTime(match, benchmarkBookie, lookbackTime)
    home = float(benchmarkOdds['1'])
    away = float(benchmarkOdds['2'])
    origReturnRate = 1 / ( 1 / home + 1 / away)
    returnRate = origReturnRate
    while returnRate < 0.999999:
        home = (2 * home) / (2 - ((1 - returnRate) * home))
        away = (2 * away) / (2 - ((1 - returnRate) * away))
        returnRate = 1 / ( 1 / home + 1 / away)

    myList.append(home)
    myList.append(away)
    returnRate = 1 / ( 1 / home + 1 / away)
    if returnRate > 1:
        print("ERROR:", match["game_id"], ",", returnRate, ",", origReturnRate)

#def GetAverage(localList):
    #number = 0
    #for data in localList:
        #number = number + data
    #return number / len(localList)

#def Method3(match, myList, lookbackTime):
    #method[0] = 'Method3'
    #pickedBookie = []
    #pickedBookie.append('pinnacle')
    #pickedBookie.append('bet365')
    #localListHome = []
    #localListDraw = []
    #localListAway = []
    #for bookie in pickedBookie:
        ##benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][bookie].items())).values())[-1]
        #benchmarkOdds = FindOddsWithOffsetTime(match, benchmarkBookie, lookbackTime)
        #home = float(benchmarkOdds['1'])
        #draw = float(benchmarkOdds['x'])
        #away = float(benchmarkOdds['2'])
        #origReturnRate = home * draw * away / (home * draw + draw * away + home * away)
        #returnRate = origReturnRate
        #while returnRate < 0.999999:
            #home = (3 * home) / (3 - ((1 - returnRate) * home))
            #draw = (3 * draw) / (3 - ((1 - returnRate) * draw))
            #away = (3 * away) / (3 - ((1 - returnRate) * away))
            #returnRate = home * draw * away / (home * draw + draw * away + home * away)
        #localListHome.append(returnRate / home)
        #localListDraw.append(returnRate / draw)
        #localListAway.append(returnRate / away)

    #myList.append(1 / GetAverage(localListHome))
    #myList.append(1 / GetAverage(localListDraw))
    #myList.append(1 / GetAverage(localListAway))
    #returnRate = myList[0] * myList[1] * myList[2] / (myList[0] * myList[1] + myList[1] * myList[2] + myList[0] * myList[2])
    #if returnRate > 1.0001:
        #print("ERROR:", match["game_id"], ",", returnRate, ",", origReturnRate)

def Method4(match, myList, lookbackTime):
    method[0] = 'Method4'
    #benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][benchmarkBookie].items())).values())[-1]
    benchmarkOdds = FindOddsWithOffsetTime(match, benchmarkBookie, lookbackTime)
    home = 1 / float(benchmarkOdds['1'])
    away = 1 / float(benchmarkOdds['2'])
    overround = home + away
    k = 1.0
    step = 0.000001
    returnRate = pow(home, k) + pow(away, k)
    while returnRate > 1.0:
        k = k + step
        returnRate = pow(home, k) + pow(away, k)
    myList.append(1 / pow(home, k))
    myList.append(1 / pow(away, k))
    #print(match["game_id"], ",", returnRate, ",", k, ",", myList, benchmarkOdds)

def CalcOddsProb(match, myList, lookbackTime):
    #Method1(match, myList, lookbackTime)
    Method2(match, myList, lookbackTime)
    #Method3(match, myList, lookbackTime)
    #Method4(match, myList, lookbackTime)

totalNumber = 0
totalWin = 0
def IsGameQualified(roundsPnl):
    allMatches = {}
    for match in allQualifiedGames.values():
        #match['kickoff'] = int(match['kickoff'])
        curTime = str(match['kickoff']) + str(match['home_team_id'])
        allMatches[float(curTime)] = match
    allMatchesInSeq = collections.OrderedDict(sorted(allMatches.items()))
    global totalNumber
    global totalWin
    for curTime, match in allMatchesInSeq.items():
        predict = QualificationCheck().is_qualified(match, benchmarkBookie)
        #print(match['game_id'], predict)
        if predict == 'x':
            continue
        try:
            myList = []
            CalcOddsProb(match, myList, myLookbackTime)
            returns = 0
            #x = random.randint(1,3)
            compareBestOdds = []
            compareBestOdds.append(0)
            compareBestOdds.append(0)
            for bookie in compareBookie:
                compareOdds = list(collections.OrderedDict(sorted(match['odds'][bookie].items())).values())[-1]
                if bookie == 'Betfair':
                    compareOdds['1'] = (float(compareOdds['1']) - 1) * exchangeReturnRate + 1
                    compareOdds['2'] = (float(compareOdds['2']) - 1) * exchangeReturnRate + 1
                if float(compareOdds['1']) > compareBestOdds[0]:
                    compareBestOdds[0] = float(compareOdds['1'])
                if float(compareOdds['2']) > compareBestOdds[1]:
                    compareBestOdds[1] = float(compareOdds['2'])
            myPredict = []
            if compareBestOdds[0] > myList[0] * (1 + bottomPercent) and compareBestOdds[0] < myList[0] * (1 + topPercent):
                if compareBestOdds[0] >= myList[0] * (1 + topPercent):
                    print(match['game_id'],compareBestOdds[0],"",myList[0])
                myPredict.append('1')
            if compareBestOdds[1] > myList[1] * (1 + bottomPercent) and compareBestOdds[1] < myList[1] * (1 + topPercent):
                if compareBestOdds[1] >= myList[1] * (1 + topPercent):
                    print(match['game_id'],compareBestOdds[1],"",myList[1])
                myPredict.append('2')
            for currentPredict in myPredict:
                totalNumber = totalNumber + 1
                if match['result'] == currentPredict:
                    if match['result'] == '1':
                        returns = compareBestOdds[0] - 1
                    elif match['result'] == '2':
                        returns = compareBestOdds[1] - 1
                else:
                    returns = -1

                if returns > 0:
                    totalWin = totalWin + 1
                match['date'] = int(time.strftime('%Y%m%d', time.localtime(float(match['kickoff']))))
                curDate = int(match['date'])
                #print(match['game_id'],match['date'],currentPredict,returns)
                if curDate in roundsPnl:
                    roundsPnl[curDate] = roundsPnl[curDate] + returns
                else:
                    roundsPnl[curDate] = returns
        except (TypeError, KeyError):
            None

leagues = []
leagues.append('National Basketball Association-')

seasons = []
seasons.append('2018-2019')
seasons.append('2017-2018')
seasons.append('2016-2017')
seasons.append('2015-2016')
seasons.append('2014-2015')

for league in leagues:
    for season in seasons:
        file_name = file_header + league + season + ".json"
        LoadData(file_name)

IsGameQualified(roundsPnl)

finalRoundsPnl = collections.OrderedDict(sorted(roundsPnl.items()))
curPnl = 0
for date, data in finalRoundsPnl.items():
    #data1 = data / totalNumber
    #curPnl = curPnl + data1

    curPnl = curPnl + data
    allRoundPnl.append(curPnl)

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

if method[0] == 'Method3':
    benchmarkBookie = 'blend'

print(compareBookie)
print(benchmarkBookie, method[0], "bottomPercent:", bottomPercent, "lookbackTime", myLookbackTime - 1800, "totalMatch:", totalNumber, "pnl:", curPnl, "winRate:", (totalWin/totalNumber) * 100, "perBetReturn:", curPnl/totalNumber)

plt.figure(1)
plt.plot(allRoundPnl, 'r-')
plt.xlabel('time (physical days)', fontdict=font)
plt.ylabel('pnl', fontdict=font)
plt.show()