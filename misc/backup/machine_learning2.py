import json
import pandas as pd
import numpy as np
from numpy import matrix
from numpy import array
from sklearn.datasets import load_digits
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

file_header = "/home/wyao/workspace/ot-aws/misc/all_odds_data/"

from lib.win007.observers.same_direction.qualification_check import QualificationCheck

def IsPredictRight(favTeamOdds, dnbOdds, dcOdds, predict, result, goalDiff, awayTeamOdds):
    if favTeamOdds <= 1.83:
        if predict == result:
            return favTeamOdds - 1
        else:
            return -1
    elif dnbOdds < 1.5: # bet 0/0.5
        if goalDiff > 0:
            return (favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2
        elif goalDiff == 0:
            return -0.5
        else:
            return -1
    elif dcOdds < 1.5:
        if predict == result:
            return dnbOdds - 1
        elif result == 'x':
            return 0
        else:
            return -1
    elif dcOdds <= 2:
        if predict == result or result == 'x':
            return dcOdds - 1
        else:
            return -1
    else:
        if goalDiff >= 0:
            return 0.3
        elif goalDiff == -1:
            return 0
        else:
            return -1

def Returns(favTeamOdds, dnbOdds, dcOdds):
    if favTeamOdds <= 1.83:
        return favTeamOdds - 1
    elif dnbOdds < 1.5: # bet 0/0.5
        return (favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2
    elif dcOdds < 1.5:
        return dnbOdds - 1
    elif dcOdds <= 2:
        return dcOdds - 1
    else:
        return 0

coefficient = 0.95
def CalculateOdds(file_names, game_id, prob):
    for file_name in file_names:
        with open(file_name) as json_file:
            matches = json.load(json_file)
            for match in matches:
                if game_id == match['game_id']:
                    predict = QualificationCheck().is_qualified(match)
                    if predict == '1':
                        home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                        home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
                        returns = IsPredictRight(match['odds']['bet365']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient, '1', match['result'], match['home_score'] - match['away_score'], match['odds']['bet365']['final']['2'])
                        print("Game ", int(game_id), ", predict home win, result is ", match['result'], "return is ", returns, " score is ", match['home_score'], ":", match['away_score'], ", prob is ", prob, ", round is", match['rounds'])
                        return returns
                    elif predict == '2':
                        away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                        away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
                        returns = IsPredictRight(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient, '2', match['result'], match['away_score'] - match['home_score'], match['odds']['bet365']['final']['1'])
                        print("Game ", int(game_id), ", predict away win, result is ", match['result'], "return is ", returns, " score is ", match['home_score'], ":", match['away_score'], ", prob is ", prob, ", round is", match['rounds'])
                        return returns

def CalculateLayOdds(file_names, game_id, prob):
    for file_name in file_names:
        with open(file_name) as json_file:
            matches = json.load(json_file)
            for match in matches:
                if game_id == match['game_id']:
                    predict = QualificationCheck().is_qualified(match)
                    if predict == '1':
                        returns = 0
                        if match['result'] != '1':
                            away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
                            if away_dc_odds < 1.5:
                                away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                                if match['result'] == '2':
                                    returns = away_dnb_odds - 1
                            else:
                                returns = away_dc_odds - 1
                        else:
                            returns = -1
                        print("Game ", int(game_id), ", predict home not win, result is ", match['result'], "return is ", returns, " score is ", match['home_score'], ":", match['away_score'], ", prob is ", prob, ", round is", match['rounds'])
                        return returns
                    elif predict == '2':
                        returns = 0
                        if match['result'] != '2':
                            home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
                            if home_dc_odds < 1.5:
                                home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                                if match['result'] == '1':
                                    returns = home_dnb_odds - 1
                            else:
                                returns = home_dc_odds - 1
                        else:
                            returns = -1
                        print("Game ", int(game_id), ", predict away not win, result is ", match['result'], "return is ", returns, " score is ", match['home_score'], ":", match['away_score'], ", prob is ", prob, ", round is", match['rounds'])
                        return returns

def Operation(data1, data2):
    #return np.log(data1 / data2)
    #return (data1 - data2) / 100.0
    return data1 - data2
    #return (data1 / data2)
    #return 0

number_of_features = 60
def GenFeatures(index, side, data, match):
    oppoSide = '1'
    if side == '1':
        oppoSide = '2'
    index = index + 1
    data[index] = match['game_id']

    #result = GenerateInitialProbData(match['probabilities']['bet365'])
    #match['probabilities']['bet365']['open'] = result[0]
    #match['probabilities']['bet365']['final'] = result[1]
    #result = GenerateInitialProbData(match['probabilities']['macau_slot'])
    #match['probabilities']['macau_slot']['open'] = result[0]
    #match['probabilities']['macau_slot']['final'] = result[1]
    #result = GenerateInitialProbData(match['probabilities']['hkjc'])
    #match['probabilities']['hkjc']['open'] = result[0]
    #match['probabilities']['hkjc']['final'] = result[1]
    #result = GenerateInitialProbData(match['probabilities']['will_hill'])
    #match['probabilities']['will_hill']['open'] = result[0]
    #match['probabilities']['will_hill']['final'] = result[1]
    #result = GenerateInitialProbData(match['probabilities']['pinnacle'])
    #match['probabilities']['pinnacle']['open'] = result[0]
    #match['probabilities']['pinnacle']['final'] = result[1]
    #result = GenerateInitialProbData(match['probabilities']['interwetten'])
    #match['probabilities']['interwetten']['open'] = result[0]
    #match['probabilities']['interwetten']['final'] = result[1]

    #index = index + 1
    #data[index] = match['probabilities']['macau_slot']['open'][side]
    #index = index + 1
    #data[index] = match['probabilities']['macau_slot']['final'][side]
    #index = index + 1
    #data[index] = match['probabilities']['hkjc']['open'][side]
    #index = index + 1
    #data[index] = match['probabilities']['interwetten']['open'][side]
    #index = index + 1
    #data[index] = match['probabilities']['will_hill']['open'][side]
    #index = index + 1
    #data[index] = match['probabilities']['will_hill']['final'][side]
    #index = index + 1
    #data[index] = match['probabilities']['pinnacle']['open'][side]
    #index = index + 1
    #data[index] = match['probabilities']['pinnacle']['final'][side]
    #index = index + 1
    #data[index] = match['probabilities']['bet365']['open'][side]
    #index = index + 1
    #data[index] = match['probabilities']['bet365']['final'][side]
    #index = index + 1
    #data[index] = Operation(match['probabilities']['macau_slot']['final'][side], match['probabilities']['macau_slot']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['final'][side], match['probabilities']['will_hill']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final'][side], match['probabilities']['pinnacle']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final'][side], match['probabilities']['bet365']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['hkjc']['open'][side], match['probabilities']['macau_slot']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['open'][side], match['probabilities']['macau_slot']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['open'][side], match['probabilities']['macau_slot']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['open'][side], match['probabilities']['macau_slot']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['interwetten']['open'][side], match['probabilities']['macau_slot']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['final'][side], match['probabilities']['macau_slot']['final'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final'][side], match['probabilities']['macau_slot']['final'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final'][side], match['probabilities']['macau_slot']['final'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['open'][side], match['probabilities']['will_hill']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['open'][side], match['probabilities']['will_hill']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['interwetten']['open'][side], match['probabilities']['will_hill']['open'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final'][side], match['probabilities']['will_hill']['final'][side])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final'][side], match['probabilities']['will_hill']['final'][side])
    #index = index + 1
    #data[index] = match['probabilities']['macau_slot']['open']['x']
    #index = index + 1
    #data[index] = match['probabilities']['macau_slot']['final']['x']
    #index = index + 1
    #data[index] = match['probabilities']['hkjc']['open']['x']
    #index = index + 1
    #data[index] = match['probabilities']['interwetten']['open']['x']
    #index = index + 1
    #data[index] = match['probabilities']['will_hill']['open']['x']
    #index = index + 1
    #data[index] = match['probabilities']['will_hill']['final']['x']
    #index = index + 1
    #data[index] = match['probabilities']['pinnacle']['open']['x']
    #index = index + 1
    #data[index] = match['probabilities']['pinnacle']['final']['x']
    #index = index + 1
    #data[index] = match['probabilities']['bet365']['open']['x']
    #index = index + 1
    #data[index] = match['probabilities']['bet365']['final']['x']
    #index = index + 1
    #data[index] = Operation(match['probabilities']['macau_slot']['final']['x'], match['probabilities']['macau_slot']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['final']['x'], match['probabilities']['will_hill']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final']['x'], match['probabilities']['pinnacle']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final']['x'], match['probabilities']['bet365']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['hkjc']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['interwetten']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['final']['x'], match['probabilities']['macau_slot']['final']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final']['x'], match['probabilities']['macau_slot']['final']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final']['x'], match['probabilities']['macau_slot']['final']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['open']['x'], match['probabilities']['will_hill']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['interwetten']['open']['x'], match['probabilities']['will_hill']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['open']['x'], match['probabilities']['will_hill']['open']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final']['x'], match['probabilities']['will_hill']['final']['x'])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final']['x'], match['probabilities']['will_hill']['final']['x'])
    #index = index + 1
    #data[index] = match['probabilities']['macau_slot']['open'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['macau_slot']['final'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['hkjc']['open'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['interwetten']['open'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['will_hill']['open'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['will_hill']['final'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['pinnacle']['open'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['pinnacle']['final'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['bet365']['open'][oppoSide]
    #index = index + 1
    #data[index] = match['probabilities']['bet365']['final'][oppoSide]
    #index = index + 1
    #data[index] = Operation(match['probabilities']['macau_slot']['final'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['final'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final'][oppoSide], match['probabilities']['pinnacle']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final'][oppoSide], match['probabilities']['bet365']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['hkjc']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['interwetten']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['will_hill']['final'][oppoSide], match['probabilities']['macau_slot']['final'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final'][oppoSide], match['probabilities']['macau_slot']['final'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final'][oppoSide], match['probabilities']['macau_slot']['final'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['open'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['open'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['interwetten']['open'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['pinnacle']['final'][oppoSide], match['probabilities']['will_hill']['final'][oppoSide])
    #index = index + 1
    #data[index] = Operation(match['probabilities']['bet365']['final'][oppoSide], match['probabilities']['will_hill']['final'][oppoSide])

    macau_slot = GenerateProbData(match['probabilities']['macau_slot'], match['kickoff'], side)
    index = index + 1
    data[index] = macau_slot[0]
    i = 1
    while i < len(macau_slot):
        index = index + 1
        if macau_slot[i] == 0:
            data[index] = 0
        else:
            data[index] = Operation(macau_slot[i - 1], macau_slot[i])
        i += 1
    bet365 = GenerateProbData(match['probabilities']['bet365'], match['kickoff'], side)
    index = index + 1
    data[index] = bet365[0]
    i = 1
    while i < len(bet365):
        index = index + 1
        if bet365[i] == 0:
            data[index] = 0
        else:
            data[index] = Operation(bet365[i - 1], bet365[i])
        i += 1
    pinnacle = GenerateProbData(match['probabilities']['pinnacle'], match['kickoff'], side)
    index = index + 1
    data[index] = pinnacle[0]
    i = 1
    while i < len(pinnacle):
        index = index + 1
        if pinnacle[i] == 0:
            data[index] = 0
        else:
            data[index] = Operation(pinnacle[i - 1], pinnacle[i])
        i += 1
    hkjc = GenerateProbData(match['probabilities']['hkjc'], match['kickoff'], side)
    index = index + 1
    data[index] = hkjc[0]
    i = 1
    while i < len(hkjc):
        index = index + 1
        if hkjc[i] == 0:
            data[index] = 0
        else:
            data[index] = Operation(hkjc[i - 1], hkjc[i])
        i += 1
    will_hill = GenerateProbData(match['probabilities']['will_hill'], match['kickoff'], side)
    index = index + 1
    data[index] = will_hill[0]
    i = 1
    while i < len(will_hill):
        index = index + 1
        if will_hill[i] == 0:
            data[index] = 0
        else:
            data[index] = Operation(will_hill[i - 1], will_hill[i])
        i += 1
    interwetten = GenerateProbData(match['probabilities']['interwetten'], match['kickoff'], side)
    index = index + 1
    data[index] = interwetten[0]
    i = 1
    while i < len(interwetten):
        index = index + 1
        if interwetten[i] == 0:
            data[index] = 0
        else:
            data[index] = Operation(interwetten[i - 1], interwetten[i])
        i += 1

    #fullData = []
    #fullData.append(macau_slot)
    #fullData.append(bet365)
    #fullData.append(pinnacle)
    #fullData.append(hkjc)
    #fullData.append(will_hill)
    #fullData.append(interwetten)
    
    #j = 0
    #while j < len(interwetten):
        #i = 1
        #while i < 6:
            #index = index + 1
            #if fullData[0][j] == 0 or fullData[i][j] == 0:
                #data[index] = 0
            #else:
                #data[index] = Operation(fullData[i][j], fullData[0][j])
            #i += 1
        #j += 1

    #x = -1
    #while x < 5:
        #x += 1
        #j = 0
        ##print("x is", x)
        #while j < len(interwetten):
            ##print("j is", j)
            #i = 0
            #while i < 6:
                ##print("x here is", x, ", i here is", i)
                #if x == i:
                    #i += 1
                    #continue
                ##print("i is", i)
                #index = index + 1
                #if fullData[x][j] == 0 or fullData[i][j] == 0:
                    #data[index] = 0
                #else:
                    #data[index] = Operation(fullData[i][j], fullData[x][j])
                ##print("index", index, ", data", data[index], ", x", x, ", i", i, ", j", j)
                #i += 1
            #j += 1
    ##print("interwetten length", len(interwetten))

    index = index + 1
    if side == '1':
        data[index] = 1
    else:
        data[index] = 0

    index = index + 1
    data[index] = float(match['rounds']) / float((match['size'] -1) * 2)
    homeTeamRank = 0
    awayTeamRank = 0
    if match['home_team_rank'] is None or match['home_team_rank'] > 100:
        homeTeamRank = 0
    else:
        homeTeamRank = match['home_team_rank']
    if match['away_team_rank'] is None or match['away_team_rank'] > 100:
        awayTeamRank = 0
    else:
        awayTeamRank = match['away_team_rank']
    index = index + 1
    if side == '1':
        data[index] = homeTeamRank / match['size']
    else:
        data[index] = awayTeamRank / match['size']
    index = index + 1
    if side == '1':
        if homeTeamRank == 0 or match['size'] == 0:
            data[index] = 0
        else:
            data[index] = Operation(awayTeamRank / match['size'], homeTeamRank / match['size'])
    else:
        if awayTeamRank == 0 or match['size'] == 0:
            data[index] = 0
        else:
            data[index] = Operation(homeTeamRank / match['size'], awayTeamRank / match['size'])
    #index = index + 1
    #data[index] = match['odds']['macau_slot']['open']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['macau_slot']['final']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['hkjc']['open']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['interwetten']['open']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['will_hill']['open']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['will_hill']['final']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['pinnacle']['open']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['pinnacle']['final']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['bet365']['open']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['bet365']['final']['x'] / 100.0
    #index = index + 1
    #data[index] = match['odds']['macau_slot']['open'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['macau_slot']['final'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['hkjc']['open'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['interwetten']['open'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['will_hill']['open'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['will_hill']['final'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['pinnacle']['open'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['pinnacle']['final'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['bet365']['open'][oppoSide] / 100.0
    #index = index + 1
    #data[index] = match['odds']['bet365']['final'][oppoSide] / 100.0
    #print("feature is", data)

def GenerateInitialProbData(probList):
    data = []
    probOpenTime = 9999999999
    probFinalTime = 0
    for key, value in probList.items():
        itemTime = int(key)
        if probOpenTime > itemTime:
            probOpenTime = itemTime
        if probFinalTime < itemTime:
            probFinalTime = itemTime
    data.append(probList[str(probOpenTime)])
    data.append(probList[str(probFinalTime)])
    return data

def GenerateProbData(probList, kickoffTime, side):
    kickoffTimeinLong = int(kickoffTime)
    probOpenTime = 9999999999
    probOpen = 0
    probFinalTime = 0
    probFinal = 0
    prob5minTime = 0
    prob5min = 0
    prob15minTime = 0
    prob15min = 0
    prob30minTime = 0
    prob30min = 0
    prob60minTime = 0
    prob60min = 0
    prob6hourTime = 0
    prob6hour = 0
    prob12hourTime = 0
    prob12hour = 0
    prob24hourTime = 0
    prob24hour = 0
    for key, value in probList.items():
        itemTime = int(key)
        if probOpenTime > itemTime:
            probOpenTime = itemTime
            probOpen = value[side]
        if probFinalTime < itemTime:
            probFinalTime = itemTime
            probFinal = value[side]
        #print("item time", itemTime, "kick off time", kickoffTimeinLong)
        if itemTime < kickoffTimeinLong - 24 * 60 * 60:
            #print("item time1", itemTime, "kick off time", kickoffTimeinLong)
            if prob24hourTime < itemTime:
                prob24hourTime = itemTime
                prob24hour = value[side]
        if itemTime >= kickoffTimeinLong - 24 * 60 * 60 and itemTime < kickoffTimeinLong - 12 * 60 * 60:
            #print("item time2", itemTime, "kick off time", kickoffTimeinLong)
            if prob12hourTime < itemTime:
                #print("item time2", itemTime, "kick off time", kickoffTimeinLong)
                prob12hourTime = itemTime
                prob12hour = value[side]
        if itemTime >= kickoffTimeinLong - 12 * 60 * 60 and itemTime < kickoffTimeinLong - 6 * 60 * 60:
            #print("item time3", itemTime, "kick off time", kickoffTimeinLong)
            if prob6hourTime < itemTime:
                #print("item time3", itemTime, "kick off time", kickoffTimeinLong)
                prob6hourTime = itemTime
                prob6hour = value[side]
        if itemTime >= kickoffTimeinLong - 6 * 60 * 60 and itemTime < kickoffTimeinLong - 60 * 60:
            #print("item time4", itemTime, "kick off time", kickoffTimeinLong)
            if prob60minTime < itemTime:
                #print("item time4", itemTime, "kick off time", kickoffTimeinLong)
                prob60minTime = itemTime
                prob60min = value[side]
        if itemTime >= kickoffTimeinLong - 60 * 60 and itemTime < kickoffTimeinLong - 30 * 60:
            #print("item time5", itemTime, "kick off time", kickoffTimeinLong)
            if prob30minTime < itemTime:
                #print("item time5", itemTime, "kick off time", kickoffTimeinLong)
                prob30minTime = itemTime
                prob30min = value[side]
        if itemTime >= kickoffTimeinLong - 30 * 60 and itemTime < kickoffTimeinLong - 15 * 60:
            #print("item time6", itemTime, "kick off time", kickoffTimeinLong)
            if prob15minTime < itemTime:
                #print("item time6", itemTime, "kick off time", kickoffTimeinLong)
                prob15minTime = itemTime
                prob15min = value[side]
        if itemTime >= kickoffTimeinLong - 15 * 60 and itemTime < kickoffTimeinLong - 5 * 60:
            #print("item time7", itemTime, "kick off time", kickoffTimeinLong)
            if prob5minTime < itemTime:
                #print("item time7", itemTime, "kick off time", kickoffTimeinLong)
                prob5minTime = itemTime
                prob5min = value[side]
    data = []
    #print(kickoffTimeinLong, ",", probOpenTime, ",", probFinalTime, ",", prob24hourTime, ",", prob12hourTime, ",", prob6hourTime, ",", prob60minTime, ",", prob30minTime, ",", prob15minTime, ",", prob5minTime)
    data.append(probOpen)
    index = 0
    if prob24hour == 0:
        if probOpenTime > kickoffTimeinLong - 24 * 60 * 60:
            data.append(0)
        else:
            data.append(probOpen)
    else:
        data.append(prob24hour)
    index += 1
    if prob12hour == 0:
        if probOpenTime > kickoffTimeinLong - 12 * 60 * 60:
            data.append(0)
        else:
            data.append(data[index])
    else:
        data.append(prob12hour)
    index += 1
    if prob6hour == 0:
        if probOpenTime > kickoffTimeinLong - 6 * 60 * 60:
            data.append(0)
        else:
            data.append(data[index])
    else:
        data.append(prob6hour)
    index += 1
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
    index += 1
    if prob15min == 0:
        if probOpenTime > kickoffTimeinLong - 15 * 60:
            data.append(0)
        else:
            data.append(data[index])
    else:
        data.append(prob15min)
    index += 1
    if prob5min == 0:
        if probOpenTime > kickoffTimeinLong - 5 * 60:
            data.append(0)
        else:
            data.append(data[index])
    else:
        data.append(prob5min)
    data.append(probFinal)
    #print(probOpen, ",", prob24hour, ",", prob12hour, ",", prob6hour, ",", prob60min, ",", prob30min, ",", prob15min, ",", prob5min, ",", probFinal)
    #print(data[0], ",", data[1], ",", data[2], ",", data[3], ",", data[4], ",", data[5], ",", data[6], ",", data[7], ",", data[8])
    return data

def IsGameQualified(file_name, correct_result, wrong_result):
    with open(file_name) as json_file:
        matches = json.load(json_file)
        for match in matches:
            predict = QualificationCheck().is_qualified(match)
            if predict == 'x':
                continue
            if predict == '1':
                home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
                if Returns(match['odds']['bet365']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient) < 0.5:
                   continue
            if predict == '2':
                away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
                if Returns(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient) < 0.5:
                    continue
            #print("Game ", match['game_id'], " qualified")
            data = [0 for x in range(number_of_features)]
            if predict == '1':
                result = IsPredictRight(match['odds']['bet365']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient, '1', match['result'], match['home_score'] - match['away_score'], match['odds']['bet365']['final']['2'])
                index = 0
                if result > 0:
                    correct_result.append(data)
                    data[index] = 1
                elif result <= 0:
                    wrong_result.append(data)
                    data[index] = 0
                GenFeatures(index, '1', data, match)
            elif predict == '2':
                away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
                result = IsPredictRight(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient, '2', match['result'], match['away_score'] - match['home_score'], match['odds']['bet365']['final']['1'])
                index = 0
                if result > 0:
                    correct_result.append(data)
                    data[index] = 1
                elif result <= 0:
                    wrong_result.append(data)
                    data[index] = 0
                GenFeatures(index, '2', data, match)

correct_predict_result = []
wrong_predict_result = []
#file_name = file_header + "English Premier League-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "England Championship-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "England League 1-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "England League 2-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Scottish Premier League-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Italian Serie A-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "France Ligue 1-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "German Bundesliga 2-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish La Liga-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Spanish Segunda Division-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Holland Eredivisie-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Belgian Pro League-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "France Ligue 2-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Holland Jupiler League-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Italian Serie B-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Norwegian Tippeligaen-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Portugal Primera Liga-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Russia Premier League-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Swedish Allsvenskan-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Swiss Super League-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Turkish Super Liga-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "USA Major League Soccer-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Australia A-League-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Brazil Serie A-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Brazil Serie B-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Chinese Super League-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "J-League Division 2-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Korea League-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Primera Division de Chile-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Primera Division de Mexico-2016-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)

file_name = file_header + "English Premier League-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England Championship-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "England League 1-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "England League 2-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Scottish Premier League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "Italian Serie A-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 1-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "German Bundesliga-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga 2-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "Spanish La Liga-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish Segunda Division-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "Holland Eredivisie-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Belgian Pro League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 2-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Holland Jupiler League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Italian Serie B-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Norwegian Tippeligaen-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Portugal Primera Liga-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Russia Premier League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swedish Allsvenskan-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swiss Super League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Turkish Super Liga-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "USA Major League Soccer-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Australia A-League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Brazil Serie A-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Brazil Serie B-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Chinese Super League-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "J-League Division 2-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Korea League-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Primera Division de Chile-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Primera Division de Mexico-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)

file_name = file_header + "English Premier League-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England Championship-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "England League 1-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "England League 2-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Scottish Premier League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "Italian Serie A-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 1-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "German Bundesliga-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga 2-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "Spanish La Liga-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish Segunda Division-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "Holland Eredivisie-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Belgian Pro League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 2-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Holland Jupiler League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Italian Serie B-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Norwegian Tippeligaen-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Portugal Primera Liga-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Russia Premier League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swedish Allsvenskan-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swiss Super League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Turkish Super Liga-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "USA Major League Soccer-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Australia A-League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Brazil Serie A-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Brazil Serie B-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Chinese Super League-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "J-League Division 2-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Korea League-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Primera Division de Chile-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Primera Division de Mexico-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)

#file_name = file_header + "Brazil Serie A-2014.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Brazil Serie B-2014.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)

allowedSamples = max(len(correct_predict_result), len(wrong_predict_result))
allResult = []
index = 0
for game in correct_predict_result:
    #allResult.append(game)
    if index < allowedSamples:
        allResult.append(game)
    else:
        continue
    index = index + 1

index = 0
for game in wrong_predict_result:
    #allResult.append(game)
    if index < allowedSamples:
        allResult.append(game)
    else:
        continue
    index = index + 1

print("game size is ", len(correct_predict_result), ", and ", len(wrong_predict_result), ", and ", len(allResult))
trainData = matrix(allResult)
trainRes = array(trainData[:,0])
trainArr = trainData[:,2:]
rf = RandomForestClassifier(n_estimators=50000, min_samples_leaf=100, random_state = 0, n_jobs=-1) #, criterion='gini'
#rf = KNeighborsClassifier(n_neighbors=2000, algorithm='brute', n_jobs=-1) #metric='minkowski', 
rf.fit(trainArr, trainRes.ravel())

importances = rf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(trainArr.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f] + 1, importances[indices[f]]))

## Plot the feature importances of the forest
#plt.figure()
#plt.title("Feature importances")
#plt.bar(range(trainArr.shape[1]), importances[indices],
       #color="r", yerr=std[indices], align="center")
#plt.xticks(range(trainArr.shape[1]), indices)
#plt.xlim([-1, trainArr.shape[1]])
#plt.show()

test_result = []
#test_result_1 = []
#test_result_2 = []
file_names = []

file_name = file_header + "English Premier League-2016-2017.json"
IsGameQualified(file_name, test_result, test_result)
file_names.append(file_name)
file_name = file_header + "England Championship-2016-2017.json"
IsGameQualified(file_name, test_result, test_result)
file_names.append(file_name)
file_name = file_header + "Spanish La Liga-2016-2017.json"
IsGameQualified(file_name, test_result, test_result)
file_names.append(file_name)
file_name = file_header + "Holland Eredivisie-2016-2017.json"
IsGameQualified(file_name, test_result, test_result)
file_names.append(file_name)
file_name = file_header + "Italian Serie A-2016-2017.json"
IsGameQualified(file_name, test_result, test_result)
file_names.append(file_name)
file_name = file_header + "German Bundesliga-2016-2017.json"
IsGameQualified(file_name, test_result, test_result)
file_names.append(file_name)

#file_name = file_header + "English Premier League-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)
#file_name = file_header + "England Championship-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)
##file_name = file_header + "England League 1-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "England League 2-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "Scottish Premier League-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)

#file_name = file_header + "Spanish La Liga-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)
##file_name = file_header + "Spanish Segunda Division-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)

#file_name = file_header + "Holland Eredivisie-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)
###file_name = file_header + "Holland Jupiler League-2017-2018.json"
###IsGameQualified(file_name, test_result, test_result)
###file_names.append(file_name)

#file_name = file_header + "German Bundesliga-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)
##file_name = file_header + "German Bundesliga 2-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)

#file_name = file_header + "Italian Serie A-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)
##file_name = file_header + "Italian Serie B-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)

##file_name = file_header + "France Ligue 1-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "France Ligue 2-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)

##file_name = file_header + "Belgian Pro League-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "Portugal Primera Liga-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "Russia Premier League-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "Swiss Super League-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "Turkish Super Liga-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "Australia A-League-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)
##file_name = file_header + "Primera Division de Chile-2017-2018.json"
##IsGameQualified(file_name, test_result, test_result)
##file_names.append(file_name)

#IsGameQualified(file_name, test_result, test_result)

#for game in test_result_1:
    #test_result.append(game)
    
#for game in test_result_2:
    #test_result.append(game)

testData = matrix(test_result)
testRes = array(testData[:,0])
testArr = testData[:,2:]

output = rf.predict(testArr)
a = np.asarray(output)
probability = rf.predict_proba(testArr)
#acc = rf.score(testArr, testRes)
#print("Score1 : %.4f", acc)

#print("game size is ", len(test_result_1), ", and ", len(test_result_2), ", and ", len(test_result))
#print("test result ", testRes.ravel())
#print("predict result ", a)

index = 0
right = 0
wrong = 0
odds = 0
#for predict in a:
    ##odds = odds + CalculateOdds(file_names, testData[index, 1], index)
    ##if testRes[index] == predict:
        ##right = right + 1
    ##else:
        ##wrong = wrong + 1
    #if predict == 1:
        #odds = odds + CalculateOdds(file_names, testData[index, 1], index)
        #if testRes[index] == predict:
            #right = right + 1
        #else:
            #wrong = wrong + 1
    #index = index + 1

benmarkProb1 = 0.56
benmarkProb2 = 0.56
for prob in probability:
    result_odds = 0
    if prob[1] > benmarkProb1:
        result_odds = CalculateOdds(file_names, testData[index, 1], prob)
        if result_odds > 0:
            right = right + 1
        else:
            wrong = wrong + 1
        odds = odds + result_odds
    #elif prob[0] > benmarkProb2:
        #result_odds = CalculateLayOdds(file_names, testData[index, 1], prob)
        #if result_odds > 0:
            #right = right + 1
        #else:
            #wrong = wrong + 1
        #odds = odds + result_odds
    index = index + 1
        

print("win rate is ", right / (right + wrong), ", bet ratio is ", (right + wrong) / len(test_result), ", total bet matches ", right + wrong, ", pnl is ", odds)
