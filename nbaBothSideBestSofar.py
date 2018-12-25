import json
import time
import math
import collections
import statistics
import pandas as pd
import numpy as np
from numpy import matrix
from numpy import array
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
from sklearn.datasets import load_digits
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RandomizedLogisticRegression

file_header = "./data/basketball_all_odds_data/National Basketball Association-"
file_end = ".json"

from src.win007.observers.same_direction.nba_qualification_check2 import QualificationCheck

timeBackOffset = 0
min_odds = 1.5
#max_odds = 1.0 + (2.0 / (min_odds - 1))
decayRatio = 0.618
#decayRatio = 0.65
min_odds_tobet1 = 1.0
min_odds_tobet2 = 1.0
max_odds_tobet1 = 10.8
max_odds_tobet2 = 10.8
min_pct = 0.5005
minEdge = 10 / 10000

allQualifiedGames = {}

diffPnl = {}
allDiffPnl = []

def IsPredictRight(favTeamOdds, predict, result):
    if predict == result:
        return favTeamOdds - 1
    else:
        return -1

def IsPredictRight_1(favTeamProb, favTeamOdds, predict, result, prob):
    if predict == result:
        return favTeamOdds - 1
    else:
        return -1

def Operation(data1, data2):
    if data1 == 0 or data2 == 0:
        return 0
    else:
        return (data1 - data2) / 100.0

def OperationX(data1, data2):
    if data1 == 0 or data2 == 0:
        return 0
    else:
        return np.log(data1 / data2)
        #return (data1 - data2) / 100.0

def Operation1(data1):
    if data1 > 0:
        return data1 * data1
        #return data1 / 100.0
    else:
        return data1

def IsPredictRight_2(poss, favTeamOdds, predict, result, prob):
    if favTeamOdds >= 1.5 and favTeamOdds <= 3:
        if poss <= prob[1]:
            #print(poss,"vs",prob[1],"")
            if predict == result:
                return favTeamOdds - 1
            else:
                return -1
        else:
            return 0
    else:
        return 0

def ChooseMax(odds1, odds2, odds3):
    best = odds1
    if best < odds2:
        best = odds2
    if best < odds3:
        best = odds3
    return best

def CalculateOdds(allQualifiedGames, game_id, prob, roundsPnl):
    match = allQualifiedGames[game_id]
    predict = match['predict']
    match['date'] = int(time.strftime('%Y%m%d', time.localtime(float(match['kickoff']))))
    if predict == '1':
        bestOdds = ChooseMax(match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'])
        #bestOdds = match['odds']['pinnacle']['final']['1']
        returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['1'], bestOdds, '1', match['result'], prob)
        #print(match['probabilities']['pinnacle']['final']['1']," vs", prob[1])
        #print("Game",int(game_id),"predict home, result",match['result'],"return is",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"score",match['home_score'],":",match['away_score'],"prob",prob,"odds", match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
        curDate = int(match['date'])
        if curDate in roundsPnl:
            roundsPnl[curDate] = roundsPnl[curDate] + returns
        else:
            roundsPnl[curDate] = returns
        return returns
    elif predict == '2':
        bestOdds = ChooseMax(match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'])
        #bestOdds = match['odds']['pinnacle']['final']['2']
        returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['2'], bestOdds, '2', match['result'], prob)
        #print(match['probabilities']['pinnacle']['final']['2']," vs", prob[1])
        #print("Game",int(game_id),"predict away, result",match['result'],"return is",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"score",match['home_score'],":",match['away_score'],"prob",prob,"odds", match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
        curDate = int(match['date'])
        if curDate in roundsPnl:
            roundsPnl[curDate] = roundsPnl[curDate] + returns
        else:
            roundsPnl[curDate] = returns
        return returns

def CalculateOppsiteOdds(allQualifiedGames, game_id, prob, roundsPnl):
    match = allQualifiedGames[game_id]
    predict = match['predict']
    match['date'] = int(time.strftime('%Y%m%d', time.localtime(float(match['kickoff']))))
    if predict == '1':
        bestOdds = ChooseMax(match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'])
        #bestOdds = match['odds']['pinnacle']['final']['1']
        returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['2'], bestOdds, '2', match['result'], prob)
        #print(match['probabilities']['pinnacle']['final']['1']," vs", prob[1])
        #print("Game",int(game_id),"oppo predict away, result",match['result'],"return",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"score",match['home_score'],":",match['away_score'],"prob",prob,"odds", match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
        curDate = int(match['date'])
        if curDate in roundsPnl:
            roundsPnl[curDate] = roundsPnl[curDate] + returns
        else:
            roundsPnl[curDate] = returns
        return returns
    elif predict == '2':
        bestOdds = ChooseMax(match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'])
        #bestOdds = match['odds']['pinnacle']['final']['2']
        returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['1'], bestOdds, '1', match['result'], prob)
        #print(match['probabilities']['pinnacle']['final']['2']," vs", prob[1])
        #print("Game",int(game_id),"oppo predict home, result",match['result'],"return",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"score",match['home_score'],":",match['away_score'],"prob",prob,"odds", match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
        curDate = int(match['date'])
        if curDate in roundsPnl:
            roundsPnl[curDate] = roundsPnl[curDate] + returns
        else:
            roundsPnl[curDate] = returns
        return returns

def GetAverageProb(match, side):
    #return min(match['pinnacle']['final'][side], match['will_hill']['final'][side], match['easybet']['final'][side], match['marathonbet']['final'][side], match['skybet']['final'][side], match['ladbroke']['open'][side])
    #return (match['pinnacle']['final'][side] + match['will_hill']['final'][side] + match['easybet']['final'][side] + match['marathonbet']['final'][side] + match['skybet']['final'][side] + match['ladbroke']['final'][side]) / 6.0
    return match['pinnacle']['final'][side]

def CalculateFinalOdds(allQualifiedGames, game_id, prob, roundsPnl):
    match = allQualifiedGames[game_id]
    predict = match['predict']
    match['date'] = int(time.strftime('%Y%m%d', time.localtime(float(match['kickoff']))))
    curDate = int(match['date'])
    returns = 0
    if predict == '1':
        if (OperationX(prob[1], GetAverageProb(match['probabilities'], '1')) > minEdge and match['odds']['pinnacle']['final']['1'] >= min_odds_tobet1 and match['odds']['pinnacle']['final']['1'] <= max_odds_tobet1) and prob[1] >= min_pct:
        #if ((prob[1] - match['probabilities']['pinnacle']['final']['1']) > 0 and match['odds']['pinnacle']['final']['1'] >= min_odds_tobet1 and match['odds']['pinnacle']['final']['1'] <= max_odds_tobet1) and prob[1] >= min_pct:
            bestOdds = ChooseMax(match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'])
            returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['1'], bestOdds, '1', match['result'], prob)
            #print("Game",int(game_id),curDate,"predict home, result",match['result'],"return is",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"prob",prob[1],":",prob[0],"score",match['home_score'],":",match['away_score'],"odds",match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
            if curDate in roundsPnl:
                roundsPnl[curDate] = roundsPnl[curDate] + returns
            else:
                roundsPnl[curDate] = returns
            diff = prob[1] - match['probabilities']['pinnacle']['final']['1']
            if diff in diffPnl:
                diffPnl[diff] = diffPnl[diff] + returns
            else:
                diffPnl[curDate] = returns
            return returns
        elif (OperationX(prob[0], GetAverageProb(match['probabilities'], '2')) > minEdge and match['odds']['pinnacle']['final']['2'] >= min_odds_tobet2 and match['odds']['pinnacle']['final']['2'] <= max_odds_tobet2) and prob[0] >= min_pct:
        #elif ((prob[0] - match['probabilities']['pinnacle']['final']['2']) > 0 and match['odds']['pinnacle']['final']['2'] >= min_odds_tobet2 and match['odds']['pinnacle']['final']['2'] <= max_odds_tobet2) and prob[0] >= min_pct:
            bestOdds = ChooseMax(match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'])
            returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['2'], bestOdds, '2', match['result'], prob)
            #print("Game",int(game_id),curDate,"predict oppo away, result",match['result'],"return is",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"prob",prob[1],":",prob[0],"score",match['home_score'],":",match['away_score'],"odds",match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
            if curDate in roundsPnl:
                roundsPnl[curDate] = roundsPnl[curDate] + returns
            else:
                roundsPnl[curDate] = returns
            diff = prob[0] - match['probabilities']['pinnacle']['final']['2']
            if diff in diffPnl:
                diffPnl[diff] = diffPnl[diff] + returns
            else:
                diffPnl[curDate] = returns
            return returns
        else:
            #print("Game",int(game_id),"predict void, result",match['result'],"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"prob",prob[1],":",prob[0],"score",match['home_score'],":",match['away_score'],"odds",match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
            return returns
    elif predict == '2':
        if (OperationX(prob[1], GetAverageProb(match['probabilities'], '2')) > minEdge and match['odds']['pinnacle']['final']['2'] >= min_odds_tobet1 and match['odds']['pinnacle']['final']['2'] <= max_odds_tobet1) and prob[1] >= min_pct:
        #if ((prob[1] - match['probabilities']['pinnacle']['final']['2']) > 0 and match['odds']['pinnacle']['final']['2'] >= min_odds_tobet1 and match['odds']['pinnacle']['final']['2'] <= max_odds_tobet1) and prob[1] >= min_pct:
            bestOdds = ChooseMax(match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'])
            returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['2'], bestOdds, '2', match['result'], prob)
            #print("Game",int(game_id),curDate,"predict away, result",match['result'],"return is",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"prob",prob[0],":",prob[1],"score",match['home_score'],":",match['away_score'],"odds",match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
            if curDate in roundsPnl:
                roundsPnl[curDate] = roundsPnl[curDate] + returns
            else:
                roundsPnl[curDate] = returns
            diff = prob[1] - match['probabilities']['pinnacle']['final']['2']
            if diff in diffPnl:
                diffPnl[diff] = diffPnl[diff] + returns
            else:
                diffPnl[curDate] = returns
            return returns
        elif (OperationX(prob[0], GetAverageProb(match['probabilities'], '1')) > minEdge and match['odds']['pinnacle']['final']['1'] >= min_odds_tobet2 and match['odds']['pinnacle']['final']['1'] <= max_odds_tobet2) and prob[0] >= min_pct:
        #elif ((prob[0] - match['probabilities']['pinnacle']['final']['1']) > 0 and match['odds']['pinnacle']['final']['1'] >= min_odds_tobet2 and match['odds']['pinnacle']['final']['1'] <= max_odds_tobet2) and prob[0] >= min_pct:
            bestOdds = ChooseMax(match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'])
            returns = IsPredictRight_1(match['probabilities']['pinnacle']['final']['1'], bestOdds, '1', match['result'], prob)
            #print("Game",int(game_id),curDate,"predict oppo home, result",match['result'],"return is",returns,"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"prob",prob[0],":",prob[1],"score",match['home_score'],":",match['away_score'],"odds",match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
            if curDate in roundsPnl:
                roundsPnl[curDate] = roundsPnl[curDate] + returns
            else:
                roundsPnl[curDate] = returns
            diff = prob[0] - match['probabilities']['pinnacle']['final']['1']
            if diff in diffPnl:
                diffPnl[diff] = diffPnl[diff] + returns
            else:
                diffPnl[curDate] = returns
            return returns
        else:
            #print("Game",int(game_id),"predict oppo void, result",match['result'],"dist",match['probabilities']['pinnacle']['final']['1'],":",match['probabilities']['pinnacle']['final']['2'],"prob",prob[0],":",prob[1],"score",match['home_score'],":",match['away_score'],"odds",match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['2'])
            return returns

def GenFeatures(index, side, data1, match, teamsDict, teamsRecentDict, teamsHomeDict, teamsAwayDict, teamsRecentHomeDict, teamsRecentAwayDict, teamsLastDate):
    data = []

    oppoSide = '1'
    if side == '1':
        oppoSide = '2'
    index = index + 1
    data.append(match['game_id'])

    pinnacle = GenerateProbData(match['probabilities']['pinnacle'], match['kickoff'], side)
    will_hill = GenerateProbData(match['probabilities']['will_hill'], match['kickoff'], side)
    easybet = GenerateProbData(match['probabilities']['easybet'], match['kickoff'], side)
    marathonbet = GenerateProbData(match['probabilities']['marathonbet'], match['kickoff'], side)
    skybet = GenerateProbData(match['probabilities']['skybet'], match['kickoff'], side)
    ladbroke = GenerateProbData(match['probabilities']['ladbroke'], match['kickoff'], side)

    i = 0
    while i < len(pinnacle):
        data.append (Operation (ladbroke [i], marathonbet [i]))  #
        data.append (Operation (skybet [i], easybet [i]))  #
        data.append (Operation (will_hill [i], easybet [i]))  #
        data.append (Operation (will_hill [i], skybet [i]))  #
        data.append (Operation (ladbroke [i], skybet [i]))  #
        i += 1

    data.append(Operation (will_hill[len(pinnacle) - 1], will_hill[0]))
    #for item in data:
        #data1.append(item)

    iList = []
    iList.append(0)
    iList.append(1)
    iList.append(2)
    iList.append(3)
    iList.append(4)
    iList.append(5)
    iList.append(13)
    iList.append(14)
    iList.append(18)

    index = -1
    for item in data:
        index += 1
        if index in iList:
            data1.append(item)

    #data1.append(pinnacle[0])
    #data1.append(pinnacle[len(pinnacle) - 1])
    #data1.append(Operation (will_hill[len(pinnacle) - 1], will_hill[0])) # 175.63
    #if side == '1':
        #data1.append(1)
    #else:
        #data1.append(0)

def GenerateProbData(probList, kickoffTime, side):
    kickoffTimeinLong = int(kickoffTime)
    kickoffTimeinLong = kickoffTimeinLong - (30 - timeBackOffset) * 60
    probOpenTime = 9999999999
    probOpen = 0
    probFinalTime = 0
    probFinal = 0
    prob15minTime = 0
    prob15min = 0
    prob30minTime = 0
    prob30min = 0
    prob45minTime = 0
    prob45min = 0
    prob60minTime = 0
    prob60min = 0
    prob3hourTime = 0
    prob3hour = 0
    prob6hourTime = 0
    prob6hour = 0
    prob9hourTime = 0
    prob9hour = 0
    prob12hourTime = 0
    prob12hour = 0
    prob18hourTime = 0
    prob18hour = 0
    prob24hourTime = 0
    prob24hour = 0
    prob48hourTime = 0
    prob48hour = 0
    for key, value in probList.items():
        if key == "final" or key == "open":
            continue
        itemTime = int(key)
        if probOpenTime > itemTime and itemTime <= kickoffTimeinLong:
            probOpenTime = itemTime
            probOpen = float(value[side])
        if probFinalTime < itemTime and itemTime <= kickoffTimeinLong:
            probFinalTime = itemTime
            probFinal = float(value[side])
        #print("item time", itemTime, "kick off time", kickoffTimeinLong)
        if itemTime < kickoffTimeinLong - 24 * 60 * 60:
            #print("item time1", itemTime, "kick off time", kickoffTimeinLong)
            if prob24hourTime < itemTime:
                prob24hourTime = itemTime
                prob24hour = float(value[side])
        if itemTime >= kickoffTimeinLong - 24 * 60 * 60 and itemTime < kickoffTimeinLong - 18 * 60 * 60:
            #print("item time2", itemTime, "kick off time", kickoffTimeinLong)
            if prob18hourTime < itemTime:
                prob18hourTime = itemTime
                prob18hour = float(value[side])
        if itemTime >= kickoffTimeinLong - 18 * 60 * 60 and itemTime < kickoffTimeinLong - 12 * 60 * 60:
            #print("item time3", itemTime, "kick off time", kickoffTimeinLong)
            if prob12hourTime < itemTime:
                prob12hourTime = itemTime
                prob12hour = float(value[side])
        if itemTime >= kickoffTimeinLong - 12 * 60 * 60 and itemTime < kickoffTimeinLong - 9 * 60 * 60:
            #print("item time4", itemTime, "kick off time", kickoffTimeinLong)
            if prob9hourTime < itemTime:
                #print("item time3", itemTime, "kick off time", kickoffTimeinLong)
                prob9hourTime = itemTime
                prob9hour = float(value[side])
        if itemTime >= kickoffTimeinLong - 9 * 60 * 60 and itemTime < kickoffTimeinLong - 6 * 60 * 60:
            #print("item time5", itemTime, "kick off time", kickoffTimeinLong)
            if prob6hourTime < itemTime:
                #print("item time3", itemTime, "kick off time", kickoffTimeinLong)
                prob6hourTime = itemTime
                prob6hour = float(value[side])
        if itemTime >= kickoffTimeinLong - 6 * 60 * 60 and itemTime < kickoffTimeinLong - 3 * 60 * 60:
            #print("item time6", itemTime, "kick off time", kickoffTimeinLong)
            if prob3hourTime < itemTime:
                #print("item time4", itemTime, "kick off time", kickoffTimeinLong)
                prob3hourTime = itemTime
                prob3hour = float(value[side])
        if itemTime >= kickoffTimeinLong - 3 * 60 * 60 and itemTime < kickoffTimeinLong - 60 * 60:
            #print("item time7", itemTime, "kick off time", kickoffTimeinLong)
            if prob60minTime < itemTime:
                #print("item time5", itemTime, "kick off time", kickoffTimeinLong)
                prob60minTime = itemTime
                prob60min = float(value[side])
        #if itemTime >= kickoffTimeinLong - 60 * 60 and itemTime < kickoffTimeinLong - 45 * 60:
            ##print("item time7", itemTime, "kick off time", kickoffTimeinLong)
            #if prob45minTime < itemTime:
                ##print("item time5", itemTime, "kick off time", kickoffTimeinLong)
                #prob45minTime = itemTime
                #prob45min = float(value[side])
        if itemTime >= kickoffTimeinLong - 60 * 60 and itemTime < kickoffTimeinLong - 30 * 60:
            #print("item time8", itemTime, "kick off time", kickoffTimeinLong)
            if prob30minTime < itemTime:
                #print("item time5", itemTime, "kick off time", kickoffTimeinLong)
                prob30minTime = itemTime
                prob30min = float(value[side])
        if itemTime >= kickoffTimeinLong - 30 * 60 and itemTime < kickoffTimeinLong - 15 * 60:
            #print("item time9", itemTime, "kick off time", kickoffTimeinLong)
            if prob15minTime < itemTime:
                #print("item time6", itemTime, "kick off time", kickoffTimeinLong)
                prob15minTime = itemTime
                prob15min = float(value[side])
    data = []
    #print(kickoffTimeinLong, ",", probOpenTime, ",", probFinalTime, ",", prob24hourTime, ",", prob12hourTime, ",", prob6hourTime, ",", prob60minTime, ",", prob30minTime, ",", prob15minTime, ",", prob5minTime)
    data.append(probOpen)

    index = 0

    if prob60min == 0:
        if probOpenTime > kickoffTimeinLong - 60 * 60:
            data.append(0)
        else:
            data.append(data[index])
    else:
        data.append(prob60min)
    index += 1

    if prob30min == 0:
        if probOpenTime > kickoffTimeinLong - 30 * 60:
            data.append(0)
        else:
            data.append(data[index])
    else:
        data.append(prob30min)

    data.append(probFinal)
    return data

def UpdateRecord(teamsDict, homeId, awayId, result):
    if result == '1':
        teamsDict[homeId][0] = teamsDict[homeId][0] + 1
        teamsDict[awayId][1] = teamsDict[awayId][1] + 1
    elif result == '2':
        teamsDict[homeId][1] = teamsDict[homeId][1] + 1
        teamsDict[awayId][0] = teamsDict[awayId][0] + 1
    else:
        print("This is totally wrong! There must be a winner")

def UpdateHomeRecord(curDict, curId, result):
    if result == '1':
        curDict[curId][0] = curDict[curId][0] + 1
    elif result == '2':
        curDict[curId][1] = curDict[curId][1] + 1
    else:
        print("This is totally wrong! There must be a winner")

def UpdateAwayRecord(curDict, curId, result):
    if result == '1':
        curDict[curId][1] = curDict[curId][1] + 1
    elif result == '2':
        curDict[curId][0] = curDict[curId][0] + 1
    else:
        print("This is totally wrong! There must be a winner")

def UpdateKickoffTime(teamsLastDate, homeId, awayId, time):
    teamsLastDate[homeId][0] = time
    teamsLastDate[awayId][1] = time

def UpdateRecentHomeOrAwayRecord(teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, result):
    if result == '1':
        teamsRecentHomeDict[homeId][0] = teamsRecentHomeDict[homeId][1]
        teamsRecentHomeDict[homeId][1] = teamsRecentHomeDict[homeId][2]
        teamsRecentHomeDict[homeId][2] = teamsRecentHomeDict[homeId][3]
        teamsRecentHomeDict[homeId][3] = teamsRecentHomeDict[homeId][4]
        teamsRecentHomeDict[homeId][4] = 1

        teamsRecentAwayDict[awayId][0] = teamsRecentAwayDict[awayId][1]
        teamsRecentAwayDict[awayId][1] = teamsRecentAwayDict[awayId][2]
        teamsRecentAwayDict[awayId][2] = teamsRecentAwayDict[awayId][3]
        teamsRecentAwayDict[awayId][3] = teamsRecentAwayDict[awayId][4]
        teamsRecentAwayDict[awayId][4] = 0

    elif result == '2':
        teamsRecentHomeDict[homeId][0] = teamsRecentHomeDict[homeId][1]
        teamsRecentHomeDict[homeId][1] = teamsRecentHomeDict[homeId][2]
        teamsRecentHomeDict[homeId][2] = teamsRecentHomeDict[homeId][3]
        teamsRecentHomeDict[homeId][3] = teamsRecentHomeDict[homeId][4]
        teamsRecentHomeDict[homeId][4] = 0

        teamsRecentAwayDict[awayId][0] = teamsRecentAwayDict[awayId][1]
        teamsRecentAwayDict[awayId][1] = teamsRecentAwayDict[awayId][2]
        teamsRecentAwayDict[awayId][2] = teamsRecentAwayDict[awayId][3]
        teamsRecentAwayDict[awayId][3] = teamsRecentAwayDict[awayId][4]
        teamsRecentAwayDict[awayId][4] = 1

    else:
        print("This is totally wrong! There must be a winner")

def UpdateRecentRecord(teamsRecentDict, homeId, awayId, result):
    if result == '1':
        teamsRecentDict[homeId][0] = teamsRecentDict[homeId][1]
        teamsRecentDict[homeId][1] = teamsRecentDict[homeId][2]
        teamsRecentDict[homeId][2] = teamsRecentDict[homeId][3]
        teamsRecentDict[homeId][3] = teamsRecentDict[homeId][4]
        teamsRecentDict[homeId][4] = teamsRecentDict[homeId][5]
        teamsRecentDict[homeId][5] = teamsRecentDict[homeId][6]
        teamsRecentDict[homeId][6] = teamsRecentDict[homeId][7]
        teamsRecentDict[homeId][7] = teamsRecentDict[homeId][8]
        teamsRecentDict[homeId][8] = teamsRecentDict[homeId][9]
        teamsRecentDict[homeId][9] = 1
        teamsRecentDict[awayId][0] = teamsRecentDict[awayId][1]
        teamsRecentDict[awayId][1] = teamsRecentDict[awayId][2]
        teamsRecentDict[awayId][2] = teamsRecentDict[awayId][3]
        teamsRecentDict[awayId][3] = teamsRecentDict[awayId][4]
        teamsRecentDict[awayId][4] = teamsRecentDict[awayId][5]
        teamsRecentDict[awayId][5] = teamsRecentDict[awayId][6]
        teamsRecentDict[awayId][6] = teamsRecentDict[awayId][7]
        teamsRecentDict[awayId][7] = teamsRecentDict[awayId][8]
        teamsRecentDict[awayId][8] = teamsRecentDict[awayId][9]
        teamsRecentDict[awayId][9] = 0
    elif result == '2':
        teamsRecentDict[homeId][0] = teamsRecentDict[homeId][1]
        teamsRecentDict[homeId][1] = teamsRecentDict[homeId][2]
        teamsRecentDict[homeId][2] = teamsRecentDict[homeId][3]
        teamsRecentDict[homeId][3] = teamsRecentDict[homeId][4]
        teamsRecentDict[homeId][4] = teamsRecentDict[homeId][5]
        teamsRecentDict[homeId][5] = teamsRecentDict[homeId][6]
        teamsRecentDict[homeId][6] = teamsRecentDict[homeId][7]
        teamsRecentDict[homeId][7] = teamsRecentDict[homeId][8]
        teamsRecentDict[homeId][8] = teamsRecentDict[homeId][9]
        teamsRecentDict[homeId][9] = 0
        teamsRecentDict[awayId][0] = teamsRecentDict[awayId][1]
        teamsRecentDict[awayId][1] = teamsRecentDict[awayId][2]
        teamsRecentDict[awayId][2] = teamsRecentDict[awayId][3]
        teamsRecentDict[awayId][3] = teamsRecentDict[awayId][4]
        teamsRecentDict[awayId][4] = teamsRecentDict[awayId][5]
        teamsRecentDict[awayId][5] = teamsRecentDict[awayId][6]
        teamsRecentDict[awayId][6] = teamsRecentDict[awayId][7]
        teamsRecentDict[awayId][7] = teamsRecentDict[awayId][8]
        teamsRecentDict[awayId][8] = teamsRecentDict[awayId][9]
        teamsRecentDict[awayId][9] = 1
    else:
        print("This is totally wrong! There must be a winner")

def IsGameQualified(file_name, correct_result, wrong_result, choice):
    with open(file_name) as json_file:
        matches = json.load(json_file)
        teamsDict = dict()
        teamsHomeDict = dict()
        teamsAwayDict = dict()
        teamsRecentDict = dict()
        teamsRecentHomeDict = dict()
        teamsRecentAwayDict = dict()
        teamsLastDate = dict()
        curMatchIndex = 0
        allMatches = {}
        for match in matches:
            match['kickoff'] = match['kickoff'] - timeBackOffset * 60
            time = match['kickoff'] + match['home_team_id']
            allMatches[float(time)] = match

        allMatchesInSeq = collections.OrderedDict(sorted(allMatches.items()))
        for time, match in allMatchesInSeq.items():
            #print(match['game_id'], time, match['kickoff'], match['home_team_id'], match['away_team_id'])
            predict = QualificationCheck().is_qualified(match)

            homeId = int(match['home_team_id'])
            awayId = int(match['away_team_id'])

            #if predict != '0':
                #if homeId not in teamsHeadToHead:
                    #teamHth = dict()
                    #teamHth[awayId] = match
                    #teamsHeadToHead[homeId] = teamHth
                #else:
                    #teamsHeadToHead[homeId][awayId] = match
            kickoffTime = float(match['kickoff'])
            if homeId not in teamsLastDate:
                results = []
                results.append(0)
                results.append(0)
                teamsLastDate[homeId] = results
            if awayId not in teamsLastDate:
                results = []
                results.append(0)
                results.append(0)
                teamsLastDate[awayId] = results
            if homeId not in teamsDict:
                results = []
                results.append(0)
                results.append(0)
                teamsDict[homeId] = results
            if awayId not in teamsDict:
                results = []
                results.append(0)
                results.append(0)
                teamsDict[awayId] = results
            if homeId not in teamsHomeDict:
                results = []
                results.append(0)
                results.append(0)
                teamsHomeDict[homeId] = results
            if awayId not in teamsAwayDict:
                results = []
                results.append(0)
                results.append(0)
                teamsAwayDict[awayId] = results
            if homeId not in teamsRecentHomeDict:
                results = []
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                teamsRecentHomeDict[homeId] = results
            if awayId not in teamsRecentAwayDict:
                results = []
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                teamsRecentAwayDict[awayId] = results
            if homeId not in teamsRecentDict:
                results = []
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                teamsRecentDict[homeId] = results
            if awayId not in teamsRecentDict:
                results = []
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                results.append(-1)
                teamsRecentDict[awayId] = results
            if choice == 'bottom' and curMatchIndex < 615:
                UpdateRecord(teamsDict, homeId, awayId, match['result'])
                UpdateHomeRecord(teamsHomeDict, homeId, match['result'])
                UpdateAwayRecord(teamsAwayDict, awayId, match['result'])
                UpdateRecentHomeOrAwayRecord(teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, match['result'])
                UpdateRecentRecord(teamsRecentDict, homeId, awayId, match['result'])
                UpdateKickoffTime(teamsLastDate, homeId, awayId, kickoffTime)
                curMatchIndex = curMatchIndex + 1
                continue
            if choice == 'top' and curMatchIndex >= 615:
                curMatchIndex = curMatchIndex + 1
                continue
            curMatchIndex = curMatchIndex + 1
            if predict == 'x':
                UpdateRecord(teamsDict, homeId, awayId, match['result'])
                UpdateHomeRecord(teamsHomeDict, homeId, match['result'])
                UpdateAwayRecord(teamsAwayDict, awayId, match['result'])
                UpdateRecentHomeOrAwayRecord(teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, match['result'])
                UpdateRecentRecord(teamsRecentDict, homeId, awayId, match['result'])
                UpdateKickoffTime(teamsLastDate, homeId, awayId, kickoffTime)
                continue
            if predict == '1':
                if match['odds']['pinnacle']['final']['1'] < min_odds or match['odds']['pinnacle']['final']['2'] < min_odds:
                    UpdateRecord(teamsDict, homeId, awayId, match['result'])
                    UpdateHomeRecord(teamsHomeDict, homeId, match['result'])
                    UpdateAwayRecord(teamsAwayDict, awayId, match['result'])
                    UpdateRecentHomeOrAwayRecord(teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, match['result'])
                    UpdateRecentRecord(teamsRecentDict, homeId, awayId, match['result'])
                    UpdateKickoffTime(teamsLastDate, homeId, awayId, kickoffTime)
                    continue
            if predict == '2':
                if match['odds']['pinnacle']['final']['2'] < min_odds or match['odds']['pinnacle']['final']['1'] < min_odds:
                    UpdateRecord(teamsDict, homeId, awayId, match['result'])
                    UpdateHomeRecord(teamsHomeDict, homeId, match['result'])
                    UpdateAwayRecord(teamsAwayDict, awayId, match['result'])
                    UpdateRecentHomeOrAwayRecord(teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, match['result'])
                    UpdateRecentRecord(teamsRecentDict, homeId, awayId, match['result'])
                    UpdateKickoffTime(teamsLastDate, homeId, awayId, kickoffTime)
                    continue
            #print("Game ", match['game_id'], " qualified")
            #data = [0 for x in range(number_of_features)]
            data = []
            if predict == '1':
                match['predict'] = '1'
                result = IsPredictRight(match['odds']['pinnacle']['final']['1'], '1', match['result'])
                index = 0
                if result > 0:
                    correct_result.append(data)
                    #data[index] = 1
                    data.append(1)
                elif result < 0:
                    wrong_result.append(data)
                    #data[index] = 0
                    data.append(0)
                GenFeatures(index, '1', data, match, teamsDict, teamsRecentDict, teamsHomeDict, teamsAwayDict, teamsRecentHomeDict, teamsRecentAwayDict, teamsLastDate)
                #print(data)
                UpdateRecord(teamsDict, homeId, awayId, match['result'])
                UpdateHomeRecord(teamsHomeDict, homeId, match['result'])
                UpdateAwayRecord(teamsAwayDict, awayId, match['result'])
                UpdateRecentHomeOrAwayRecord(teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, match['result'])
                UpdateRecentRecord(teamsRecentDict, homeId, awayId, match['result'])
                UpdateKickoffTime(teamsLastDate, homeId, awayId, kickoffTime)
            elif predict == '2':
                match['predict'] = '2'
                result = IsPredictRight(match['odds']['pinnacle']['final']['2'], '2', match['result'])
                index = 0
                if result > 0:
                    correct_result.append(data)
                    data.append(1)
                elif result < 0:
                    wrong_result.append(data)
                    data.append(0)
                GenFeatures(index, '2', data, match, teamsDict, teamsRecentDict, teamsHomeDict, teamsAwayDict, teamsRecentHomeDict, teamsRecentAwayDict, teamsLastDate)
                #print(data)
                UpdateRecord(teamsDict, homeId, awayId, match['result'])
                UpdateHomeRecord(teamsHomeDict, homeId, match['result'])
                UpdateAwayRecord(teamsAwayDict, awayId, match['result'])
                UpdateRecentHomeOrAwayRecord(teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, match['result'])
                UpdateRecentRecord(teamsRecentDict, homeId, awayId, match['result'])
                UpdateKickoffTime(teamsLastDate, homeId, awayId, kickoffTime)
            allQualifiedGames[int(match['game_id'])] = match

years = []
#years.append("2016-2017")
#years.append("2017-")
#years.append("2017-2018")
years.append("2018-2019")

halves = []
halves.append('top')
halves.append('bottom')

tree_size = 1000
totalPnl = 0
perMatchPnl = []
winRate = []
for year in years:
    for half in halves:
        correct_predict_result = []
        wrong_predict_result = []
        test_result = []
        file_name = file_header + "2014-2015" + file_end
        IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'full')
        file_name = file_header + "2015-2016" + file_end
        IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'full')
        if year == "2016-2017" and half == "top":
            None
        if year == "2016-2017" and half == "bottom":
            file_name = file_header + "2016-2017" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'top')
            None
        if year == "2017-" and half == "top":
            None
        if year == "2017-" and half == "bottom":
            file_name = file_header + "2017-2018" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'top')
        if year == "2017-2018" and half == "top":
            file_name = file_header + "2016-2017" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'full')
            None
        if year == "2017-2018" and half == "bottom":
            file_name = file_header + "2016-2017" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'full')
            file_name = file_header + "2017-2018" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'top')
        if year == "2018-2019" and half == "top":
            #continue
            file_name = file_header + "2016-2017" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'full')
            file_name = file_header + "2017-2018" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'full')
            file_name = file_header + "2018-2019" + file_end
            IsGameQualified(file_name, correct_predict_result, wrong_predict_result, 'full')
        if year == "2018-2019" and half == "bottom":
            continue
        allowedSamples1 = max(len(correct_predict_result), len(wrong_predict_result))
        allowedSamples2 = max(len(correct_predict_result), len(wrong_predict_result))
        allResult = []
        index = 0
        for game in correct_predict_result:
            if index < allowedSamples2:
                allResult.append(game)
            else:
                continue
            index = index + 1

        index = 0
        for game in wrong_predict_result:
            if index < allowedSamples1:
                allResult.append(game)
            else:
                continue
            index = index + 1
        this_year = year
        if year == "2017-":
            this_year = year + "2018"
        test_file_name = file_header + this_year + file_end
        print("game size is ", len(correct_predict_result), ", and ", len(wrong_predict_result), ", and ", len(allResult))
        trainData = matrix(allResult)
        trainRes = array(trainData[:,0])
        trainArr = trainData[:,2:]
        rf = RandomForestClassifier(n_estimators=tree_size, min_samples_leaf=1, random_state = 0, n_jobs=-1) #criterion='entropy',
        #rf = KNeighborsClassifier(n_neighbors=len(correct_predict_result), algorithm='brute', n_jobs=-1) #metric='minkowski', 
        #rf = svm.SVC(gamma='scale')
        #rf = SGDClassifier(loss="log", penalty="l2", max_iter=50)
        rf.fit(trainArr, trainRes.ravel())

        #importances = rf.feature_importances_
        #std = np.std([tree.feature_importances_ for tree in rf.estimators_],
        #     axis=0)
        #indices = np.argsort(importances)[::-1]
        #for f in range(trainArr.shape[1]):
        #    print("%d. feature %d (%f)" % (f + 1, indices[f] + 1, importances[indices[f]]))

        clf = RandomizedLogisticRegression()
        clf.fit(trainArr, trainRes.ravel())
        print(clf.scores_)

        IsGameQualified(test_file_name, test_result, test_result, half)
        testData = matrix(test_result)
        testRes = array(testData[:,0])
        testArr = testData[:,2:]
        output = rf.predict(testArr)
        a = np.asarray(output)
        probability = rf.predict_proba(testArr)
        score1 = rf.score(trainArr, trainRes.ravel())
        score2 = rf.score(testArr, testRes.ravel())
        print("Score is", score1, "and", score2, "roc", roc_auc_score(testRes, probability[:,1]),",",testArr.shape)
        index = 0
        right = 0
        wrong = 0
        odds = 0

        roundsPnl = {}
        allRoundPnl = []

        benmarkProb1 = 0.5
        benmarkProb2 = 1.6
        benmarkProb3 = 0.5
        benmarkProb4 = 1.6

        if year == "2018-2019" and half == "top":
          joblib.dump(rf, './src/ops/game_qualifier/nba.pkl')

        for prob in probability:
            result_odds = 0

            result_odds = CalculateFinalOdds(allQualifiedGames, testData[index, 1], prob, roundsPnl)
            if result_odds > 0:
               right = right + 1
            elif result_odds < 0:
               wrong = wrong + 1
            odds = odds + result_odds
            index = index + 1

            #if prob[1] >= 0.5 and prob[1] <= 1.0:
                #result_odds = CalculateOdds(allQualifiedGames, testData[index, 1], prob, roundsPnl)
                #if result_odds > 0:
                    #right = right + 1
                #elif result_odds < 0:
                    #wrong = wrong + 1
                #odds = odds + result_odds
            #elif prob[0] > 0.5 and prob[0] <= 1.0:
                #result_odds = CalculateOppsiteOdds(allQualifiedGames, testData[index, 1], prob, roundsPnl)
                #if result_odds > 0:
                    #right = right + 1
                #elif result_odds < 0:
                    #wrong = wrong + 1
                #odds = odds + result_odds
            #index = index + 1

        finalRoundsPnl = collections.OrderedDict(sorted(roundsPnl.items()))
        curPnl = 0
        for date, data in finalRoundsPnl.items():
           curPnl = curPnl + data
           allRoundPnl.append(curPnl)

        plt.figure(1)
        plt.plot(allRoundPnl, 'r-')
        plt.show()

        print(year, half, min_odds, tree_size, timeBackOffset, min_pct, minEdge, "winR", right / (right + wrong), "betR", (right + wrong) / len(test_result), "total matches", right + wrong, "pnl", odds, "per match ret", odds / (right + wrong))
        totalPnl += odds
        perMatchPnl.append(odds / (right + wrong))
        winRate.append(right / (right + wrong))
#print("tPnl", totalPnl, "per match average", statistics.mean(perMatchPnl), "variance", statistics.variance(perMatchPnl),
   #"winRate average", statistics.mean(winRate), "variance", statistics.variance(winRate))
