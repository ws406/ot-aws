import json
import pandas as pd
import numpy as np
from numpy import matrix
from numpy import array
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

file_header = "/home/wyao/Downloads/Odds/"

from lib.win007.observers.same_direction.qualification_check import QualificationCheck

def IsPredictRight(favTeamOdds, dnbOdds, dcOdds, predict, result, goalDiff):
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

coefficient = 0.95
def CalculateOdds(file_names, game_id):
    for file_name in file_names:
        with open(file_name) as json_file:
            matches = json.load(json_file)
            for match in matches:
                if game_id == match['game_id']:
                    predict = QualificationCheck().is_qualified(match)
                    if predict == '1':
                        home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                        home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
                        returns = IsPredictRight(match['odds']['bet365']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient, '1', match['result'], match['home_score'] - match['away_score'])
                        print("Game ", int(game_id), ", predict home win, result is ", match['result'], "return is ", returns, " score is ", match['home_score'], ":", match['away_score'])
                        return returns
                    elif predict == '2':
                        away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                        away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
                        returns = IsPredictRight(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient, '2', match['result'], match['away_score'] - match['home_score'])
                        print("Game ", int(game_id), ", predict away win, result is ", match['result'], "return is ", returns, " score is ", match['home_score'], ":", match['away_score'])
                        return returns

def Operation(data1, data2):
    return np.log(data1 / data2)
    #return (data1 - data2) / 100.0
    #return (data1 / data2)
    #return 0

number_of_features = 127
def GenFeatures(index, side, data, match):
    oppoSide = '1'
    if side == '1':
        oppoSide = '2'
    index = index + 1
    data[index] = match['game_id']
    index = index + 1
    if side == '1':
        data[index] = 1
    else:
        data[index] = 0
    index = index + 1
    data[index] = match['probabilities']['macau_slot']['open'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['macau_slot']['final'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['hkjc']['open'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['interwetten']['open'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['will_hill']['open'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['will_hill']['final'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['pinnacle']['open'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['pinnacle']['final'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['bet365']['open'][side] / 100.0
    index = index + 1
    data[index] = match['probabilities']['bet365']['final'][side] / 100.0
    index = index + 1
    data[index] = Operation(match['probabilities']['macau_slot']['final'][side], match['probabilities']['macau_slot']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['final'][side], match['probabilities']['will_hill']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final'][side], match['probabilities']['pinnacle']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final'][side], match['probabilities']['bet365']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['hkjc']['open'][side], match['probabilities']['macau_slot']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['open'][side], match['probabilities']['macau_slot']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['open'][side], match['probabilities']['macau_slot']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['open'][side], match['probabilities']['macau_slot']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['interwetten']['open'][side], match['probabilities']['macau_slot']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['final'][side], match['probabilities']['macau_slot']['final'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final'][side], match['probabilities']['macau_slot']['final'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final'][side], match['probabilities']['macau_slot']['final'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['open'][side], match['probabilities']['will_hill']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['open'][side], match['probabilities']['will_hill']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['interwetten']['open'][side], match['probabilities']['will_hill']['open'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final'][side], match['probabilities']['will_hill']['final'][side])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final'][side], match['probabilities']['will_hill']['final'][side])
    index = index + 1
    data[index] = match['probabilities']['macau_slot']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['macau_slot']['final']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['hkjc']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['interwetten']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['will_hill']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['will_hill']['final']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['pinnacle']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['pinnacle']['final']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['bet365']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['probabilities']['bet365']['final']['x'] / 100.0
    index = index + 1
    data[index] = Operation(match['probabilities']['macau_slot']['final']['x'], match['probabilities']['macau_slot']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['final']['x'], match['probabilities']['will_hill']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final']['x'], match['probabilities']['pinnacle']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final']['x'], match['probabilities']['bet365']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['hkjc']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['interwetten']['open']['x'], match['probabilities']['macau_slot']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['final']['x'], match['probabilities']['macau_slot']['final']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final']['x'], match['probabilities']['macau_slot']['final']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final']['x'], match['probabilities']['macau_slot']['final']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['open']['x'], match['probabilities']['will_hill']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['interwetten']['open']['x'], match['probabilities']['will_hill']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['open']['x'], match['probabilities']['will_hill']['open']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final']['x'], match['probabilities']['will_hill']['final']['x'])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final']['x'], match['probabilities']['will_hill']['final']['x'])
    index = index + 1
    data[index] = match['probabilities']['macau_slot']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['macau_slot']['final'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['hkjc']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['interwetten']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['will_hill']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['will_hill']['final'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['pinnacle']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['pinnacle']['final'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['bet365']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['probabilities']['bet365']['final'][oppoSide] / 100.0
    index = index + 1
    data[index] = Operation(match['probabilities']['macau_slot']['final'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['final'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final'][oppoSide], match['probabilities']['pinnacle']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final'][oppoSide], match['probabilities']['bet365']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['hkjc']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['interwetten']['open'][oppoSide], match['probabilities']['macau_slot']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['will_hill']['final'][oppoSide], match['probabilities']['macau_slot']['final'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final'][oppoSide], match['probabilities']['macau_slot']['final'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final'][oppoSide], match['probabilities']['macau_slot']['final'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['open'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['open'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['interwetten']['open'][oppoSide], match['probabilities']['will_hill']['open'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['pinnacle']['final'][oppoSide], match['probabilities']['will_hill']['final'][oppoSide])
    index = index + 1
    data[index] = Operation(match['probabilities']['bet365']['final'][oppoSide], match['probabilities']['will_hill']['final'][oppoSide])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['macau_slot']['final'], match['kelly_rates']['macau_slot']['open'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['will_hill']['final'], match['kelly_rates']['will_hill']['open'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['pinnacle']['final'], match['kelly_rates']['pinnacle']['open'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['bet365']['final'], match['kelly_rates']['bet365']['open'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['will_hill']['open'], match['kelly_rates']['macau_slot']['open'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['pinnacle']['open'], match['kelly_rates']['macau_slot']['open'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['bet365']['open'], match['kelly_rates']['macau_slot']['open'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['will_hill']['final'], match['kelly_rates']['macau_slot']['final'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['pinnacle']['final'], match['kelly_rates']['macau_slot']['final'])
    index = index + 1
    data[index] = Operation(match['kelly_rates']['bet365']['final'], match['kelly_rates']['macau_slot']['final'])
    index = index + 1
    data[index] = float(match['rounds']) / float((match['size'] -1) * 2)
    index = index + 1
    if match['home_team_rank'] is None or match['home_team_rank'] > 100:
        data[index] = 0
    else:
        data[index] = match['home_team_rank'] / match['size']
    index = index + 1
    if match['away_team_rank'] is None or match['away_team_rank'] > 100:
        data[index] = 0
    else:
        data[index] = match['away_team_rank'] / match['size']
    index = index + 1
    data[index] = match['odds']['macau_slot']['open'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['macau_slot']['final'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['hkjc']['open'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['interwetten']['open'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['will_hill']['open'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['will_hill']['final'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['pinnacle']['open'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['pinnacle']['final'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['bet365']['open'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['bet365']['final'][side] / 100.0
    index = index + 1
    data[index] = match['odds']['macau_slot']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['macau_slot']['final']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['hkjc']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['interwetten']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['will_hill']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['will_hill']['final']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['pinnacle']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['pinnacle']['final']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['bet365']['open']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['bet365']['final']['x'] / 100.0
    index = index + 1
    data[index] = match['odds']['macau_slot']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['macau_slot']['final'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['hkjc']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['interwetten']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['will_hill']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['will_hill']['final'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['pinnacle']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['pinnacle']['final'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['bet365']['open'][oppoSide] / 100.0
    index = index + 1
    data[index] = match['odds']['bet365']['final'][oppoSide] / 100.0

def IsGameQualified(file_name, correct_result, wrong_result):
    with open(file_name) as json_file:
        matches = json.load(json_file)
        for match in matches:
            predict = QualificationCheck().is_qualified(match)
            if(predict == 'x' or match['odds']['bet365']['final']['1'] < 1.5 or match['odds']['bet365']['final']['2'] < 1.5):
                continue
            data = [0 for x in range(number_of_features)]
            if predict == '1':
                home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
                result = IsPredictRight(match['odds']['bet365']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient, '1', match['result'], match['home_score'] - match['away_score'])
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
                result = IsPredictRight(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient, '2', match['result'], match['away_score'] - match['home_score'])
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
file_name = file_header + "English Premier League-2016-2017.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England Championship-2016-2017.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England League 1-2016-2017.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England League 2-2016-2017.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Italian Serie A-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 1-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga 2-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish La Liga-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Holland Eredivisie-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Belgian Pro League-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 2-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Holland Jupiler League-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Italian Serie B-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Norwegian Tippeligaen-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Portugal Primera Liga-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Russia Premier League-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Scottish Premier League-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish Segunda Division-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swedish Allsvenskan-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swiss Super League-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Turkish Super Liga-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "USA Major League Soccer-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
##file_name = file_header + "Argentine Division 1-2017.json"
##IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Australia A-League-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Brazil Serie A-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Brazil Serie B-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Chinese Super League-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "J-League Division 2-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Korea League-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Primera Division de Chile-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Primera Division de Mexico-2016-2017.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)

file_name = file_header + "English Premier League-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England Championship-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England League 1-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England League 2-2015-2016.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Italian Serie A-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 1-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga 2-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish La Liga-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Holland Eredivisie-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
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
#file_name = file_header + "Scottish Premier League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish Segunda Division-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swedish Allsvenskan-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swiss Super League-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Turkish Super Liga-2015-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "USA Major League Soccer-2016.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Argentine Division 1-2016.json"
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
file_name = file_header + "England League 1-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
file_name = file_header + "England League 2-2014-2015.json"
IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Italian Serie A-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "France Ligue 1-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "German Bundesliga 2-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish La Liga-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Holland Eredivisie-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
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
#file_name = file_header + "Scottish Premier League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Spanish Segunda Division-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swedish Allsvenskan-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Swiss Super League-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Turkish Super Liga-2014-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "USA Major League Soccer-2015.json"
#IsGameQualified(file_name, correct_predict_result, wrong_predict_result)
#file_name = file_header + "Argentine Division 1-2015.json"
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

allowedSamples = min(len(correct_predict_result), len(wrong_predict_result))
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
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

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

file_name = file_header + "English Premier League-2017-2018.json"
IsGameQualified(file_name, test_result, test_result)
file_names.append(file_name)

#file_name = file_header + "England Championship-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)

#file_name = file_header + "Spanish La Liga-2017-2018.json"
#IsGameQualified(file_name, test_result_1, test_result_2)
#file_names.append(file_name)

#file_name = file_header + "German Bundesliga-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)

#file_name = file_header + "Italian Serie A-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)

#file_name = file_header + "France Ligue 1-2017-2018.json"
#IsGameQualified(file_name, test_result, test_result)
#file_names.append(file_name)

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
#acc = rf.score(testArr, testRes)
#print("Score1 : %.4f", acc)

#print("game size is ", len(test_result_1), ", and ", len(test_result_2), ", and ", len(test_result))
#print("test result ", testRes.ravel())
#print("predict result ", a)

index = 0
right = 0
wrong = 0
odds = 0
for predict in a:
    if predict == 1:
        odds = odds + CalculateOdds(file_names, testData[index, 1])
        if testRes[index] == predict:
            right = right + 1
        else:
            wrong = wrong + 1
    index = index + 1

print("win rate is ", right / (right + wrong), ", bet ratio is ", (right + wrong) / len(test_result), ", total bet matches ", right + wrong, ", pnl is ", odds)
