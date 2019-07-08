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

file_header = "/home/wyao/workspace/ot-aws-new/data/football_all_odds_data/"

from src.win007.observers.same_direction.qualification_check_test_efficiency import QualificationCheck

roundsPnl = {}
allRoundPnl = []
allQualifiedGames = {}
#bookie = 'pinnacle'
#bookie = 'bet365'
#bookie = 'macau_slot'
#bookie = 'hkjc'
#bookie = 'will_hill'
bookie = 'china'

def LoadData(file_name):
    #print("Loading ", file_name)
    with open(file_name) as json_file:
        allMatches = {}
        matches = json.load(json_file)
        for match in matches:
            #time = match['kickoff'] + match['home_team_id']
            #allMatches[float(time)] = match
            allQualifiedGames[int(match['game_id'])] = match

def Method1(match, myList):
    benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][bookie].items())).values())[-1]
    myList.append(float(benchmarkOdds['1']))
    myList.append(float(benchmarkOdds['x']))
    myList.append(float(benchmarkOdds['2']))
    benchmarkProb = list(collections.OrderedDict(sorted(match['probabilities'][bookie].items())).values())[-1]
    myList.append(float(benchmarkProb['1']))
    myList.append(float(benchmarkProb['x']))
    myList.append(float(benchmarkProb['2']))

def Method2(match, myList):
    benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][bookie].items())).values())[-1]
    home = float(benchmarkOdds['1'])
    draw = float(benchmarkOdds['x'])
    away = float(benchmarkOdds['2'])
    origReturnRate = home * draw * away / (home * draw + draw * away + home * away)
    returnRate = origReturnRate
    while returnRate < 0.999999:
        home = (3 * home) / (3 - ((1 - returnRate) * home))
        draw = (3 * draw) / (3 - ((1 - returnRate) * draw))
        away = (3 * away) / (3 - ((1 - returnRate) * away))
        returnRate = home * draw * away / (home * draw + draw * away + home * away)

    myList.append(home)
    myList.append(draw)
    myList.append(away)
    returnRate = home * draw * away / (home * draw + draw * away + home * away)
    if returnRate > 1:
        print("ERROR:", match["game_id"], ",", returnRate, ",", origReturnRate)

def GetAverage(localList):
    number = 0
    for data in localList:
        number = number + data
    return number / len(localList)

def Method3(match, myList):
    pickedBookie = []
    pickedBookie.append('pinnacle')
    pickedBookie.append('bet365')
    localListHome = []
    localListDraw = []
    localListAway = []
    for bookie in pickedBookie:
        benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][bookie].items())).values())[-1]
        home = float(benchmarkOdds['1'])
        draw = float(benchmarkOdds['x'])
        away = float(benchmarkOdds['2'])
        origReturnRate = home * draw * away / (home * draw + draw * away + home * away)
        returnRate = origReturnRate
        while returnRate < 0.999999:
            home = (3 * home) / (3 - ((1 - returnRate) * home))
            draw = (3 * draw) / (3 - ((1 - returnRate) * draw))
            away = (3 * away) / (3 - ((1 - returnRate) * away))
            returnRate = home * draw * away / (home * draw + draw * away + home * away)
        localListHome.append(returnRate / home)
        localListDraw.append(returnRate / draw)
        localListAway.append(returnRate / away)

    myList.append(1 / GetAverage(localListHome))
    myList.append(1 / GetAverage(localListDraw))
    myList.append(1 / GetAverage(localListAway))
    returnRate = myList[0] * myList[1] * myList[2] / (myList[0] * myList[1] + myList[1] * myList[2] + myList[0] * myList[2])
    if returnRate > 1.0001:
        print("ERROR:", match["game_id"], ",", returnRate, ",", origReturnRate)

def Method4(match, myList):
    benchmarkOdds = list(collections.OrderedDict(sorted(match['odds'][bookie].items())).values())[-1]
    home = 1 / float(benchmarkOdds['1'])
    draw = 1 / float(benchmarkOdds['x'])
    away = 1 / float(benchmarkOdds['2'])
    overround = home + draw + away
    k = 1.0
    step = 0.00002
    returnRate = pow(home, k) + pow(draw, k)+ pow(away, k)
    while returnRate > 1.0000001:
        k = k + step
        returnRate = pow(home, k) + pow(draw, k)+ pow(away, k)
    myList.append(1 / pow(home, k))
    myList.append(1 / pow(draw, k))
    myList.append(1 / pow(away, k))
    #print(match["game_id"], ",", returnRate, ",", k, ",", myList, benchmarkOdds)

def CalcOddsProb(match, myList):
    #Method1(match, myList) # use original odds
    #Method2(match, myList) # use odds calc from Margin to Odds
    #Method3(match, myList)
    Method4(match, myList)

totalNumber = 0
def IsGameQualified(roundsPnl):
    allMatches = {}
    for match in allQualifiedGames.values():
        #match['kickoff'] = int(match['kickoff'])
        curTime = str(match['kickoff']) + str(match['home_team_id'])
        allMatches[float(curTime)] = match
    allMatchesInSeq = collections.OrderedDict(sorted(allMatches.items()))
    global totalNumber
    for curTime, match in allMatchesInSeq.items():
        predict = QualificationCheck().is_qualified(match, bookie)
        #print(match['game_id'], predict)
        if predict == 'x':
            continue
        myList = []
        CalcOddsProb(match, myList)
        returns = 0
        myPredict = []

        myPredict.append('1')
        myPredict.append('x')
        myPredict.append('2')

        #x = random.randint(1,3)
        #if x == 2:
            #myPredict.append('x')
        #elif x == 3:
            #myPredict.append('2')
        #elif x == 1:
            #myPredict.append('1')
        #else:
            #print("ERROR!")

        for currentPredict in myPredict:
            totalNumber = totalNumber + 1
            if match['result'] == currentPredict:
                if match['result'] == '1':
                    returns = myList[0] - 1
                elif match['result'] == 'x':
                    returns = myList[1] - 1
                elif match['result'] == '2':
                    returns = myList[2] - 1
            else:
                returns = -1

            match['date'] = int(time.strftime('%Y%m%d', time.localtime(float(match['kickoff']))))
            curDate = int(match['date'])
            #print(match['game_id'],match['date'],myPredict,returns)
            if curDate in roundsPnl:
                roundsPnl[curDate] = roundsPnl[curDate] + returns
            else:
                roundsPnl[curDate] = returns

leagues = []
leagues.append('English Premier League-')
leagues.append('Italian Serie A-')
leagues.append('German Bundesliga-')
leagues.append('Holland Eredivisie-')
leagues.append('France Ligue 1-')
leagues.append('Spanish La Liga-')
leagues.append('Scottish Premier League-')
leagues.append('Russia Premier League-')
leagues.append('Portugal Primera Liga-')
leagues.append('England Championship-')
leagues.append('Spanish Segunda Division-')
leagues.append('Turkish Super Liga-')
leagues.append('England League 1-')
leagues.append('England League 2-')
leagues.append('Belgian Pro League-')
leagues.append('France Ligue 2-')
leagues.append('Australia A-League-')
leagues.append('Holland Jupiler League-')
leagues.append('German Bundesliga 2-')

seasons = []
seasons.append('2018-2019')
seasons.append('2017-2018')
seasons.append('2016-2017')
seasons.append('2015-2016')
seasons.append('2014-2015')
seasons.append('2013-2014')

for league in leagues:
    #print(league)
    for season in seasons:
        if (league == 'Belgian Pro League-' or league == 'Russia Premier League-') and season == '2013-2014':
            continue
        file_name = file_header + league + season + ".json"
        LoadData(file_name)

leagues1 = []
leagues1.append('USA Major League Soccer-')
leagues1.append('J-League Division 2-')
leagues1.append('Chinese Super League-')
leagues1.append('J-League Division 1-')
leagues1.append('Brazil Serie A-')
leagues1.append('Brazil Serie B-')
leagues1.append('Korea League-')
leagues1.append('Norwegian Tippeligaen-')
leagues1.append('Swedish Allsvenskan-')

seasons1 = []
seasons1.append('2019')
seasons1.append('2018')
seasons1.append('2017')
seasons1.append('2016')
seasons1.append('2015')
seasons1.append('2014')

for league in leagues1:
    #print(league)
    for season in seasons1:
        if league == 'J-League Division 1-' and (season == '2014' or season == '2015' or season == '2016'):
            continue
        if league == 'USA Major League Soccer-' and season == '2019':
            continue
        file_name = file_header + league + season + ".json"
        LoadData(file_name)

IsGameQualified(roundsPnl)

finalRoundsPnl = collections.OrderedDict(sorted(roundsPnl.items()))
curPnl = 0
for date, data in finalRoundsPnl.items():
    data1 = data / totalNumber
    curPnl = curPnl + data1

    #curPnl = curPnl + data
    allRoundPnl.append(curPnl)

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

plt.figure(1)
plt.plot(allRoundPnl, 'r-')
plt.xlabel('time (physical days)', fontdict=font)
plt.ylabel('pnl', fontdict=font)
plt.ylim(top=0.01)
plt.ylim(bottom=-0.01)
plt.show()