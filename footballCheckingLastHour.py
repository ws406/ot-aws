import json
import pandas as pd
import numpy as np
import math
import collections
from numpy import matrix
from numpy import array
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoLars

file_header = "/home/wyao/ot-aws/data/football_all_odds_data/"

#from src.win007.observers.same_direction.qualification_check import QualificationCheck
#from src.win007.observers.same_direction.qualification_check_lastHour import QualificationCheck
from src.win007.observers.same_direction.qualification_check_lastHourSingleBookie import QualificationCheck

allQualifiedGames = {}

def IsPredictRight(favTeamProb, favTeamOdds, dnbOdds, dcOdds, predict, result, goalDiff, awayTeamOdds):
    if favTeamOdds <= threshold:
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

def IsPredictRight2(predict, favTeamProb, favTeamOdds, dnbOdds, dcOdds, result, goalDiff, awayTeamOdds):
    if predict == '1':
        if goalDiff > 0:
            return favTeamOdds - 1
        else:
            return -1
    elif predict == '2':
        if goalDiff < 0:
            return favTeamOdds - 1
        else:
            return -1
    elif predict == '3':
        if goalDiff <= 0:
            return dcOdds - 1
        else:
            return -1
    elif predict == '4':
        if goalDiff >= 0:
            return dcOdds - 1
        else:
            return -1

def IsPredictRight3(predict, favTeamProb, favTeamOdds, dnbOdds, dcOdds, result, goalDiff, awayTeamOdds):
    if predict == '1':
        if favTeamOdds > threshold:
            if goalDiff > 0:
                return favTeamOdds - 1
            else:
                return -1
        else:
            if goalDiff > 0:
                return dnbOdds - 1
            elif goalDiff == 0:
                return 0
            else:
                return -1
    elif predict == '2':
        if favTeamOdds > threshold:
            if goalDiff < 0:
                return favTeamOdds - 1
            else:
                return -1
        else:
            if goalDiff < 0:
                return dnbOdds - 1
            elif goalDiff == 0:
                return 0
            else:
                return -1
    elif predict == '3':
        if goalDiff <= 0:
            return dcOdds - 1
        else:
            return -1
    elif predict == '4':
        if goalDiff >= 0:
            return dcOdds - 1
        else:
            return -1

coefficient = 0.95
def CalculateOdds(game_id, prob, roundsPnl):
    match = allQualifiedGames[game_id]
    predict = match['predict']
    if predict == '1' or predict == '4':
        home_dnb_odds = match['odds']['pinnacle']['final']['1'] * (match['odds']['pinnacle']['final']['x'] - 1) / match['odds']['pinnacle']['final']['x']
        home_dc_odds = match['odds']['pinnacle']['final']['1'] * match['odds']['pinnacle']['final']['x'] / (match['odds']['pinnacle']['final']['1'] + match['odds']['pinnacle']['final']['x'])
        #poReturn = Returns(match['probabilities']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient)
        #if poReturn < qualifyBenmark:
            #print("Game", game_id, "home return not qualify", poReturn)
            #return 0
        #if match['odds']['macau_slot']['final']['1'] <= match['odds']['hkjc']['final']['1']:
            #return 0
        returns = IsPredictRight2(predict, match['probabilities']['pinnacle']['final']['1'], match['odds']['pinnacle']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient, match['result'], match['home_score'] - match['away_score'], match['odds']['pinnacle']['final']['2'])
        #print("Game", int(game_id), match['league_name'], "pred home result", match['result'], "return", returns, "calcProb", prob, "score", match['home_score'], ":", match['away_score'], ", prob", prob, ",", match['probabilities']['pinnacle']['final']['1'], ":", match['probabilities']['pinnacle']['final']['x'], ":", match['probabilities']['pinnacle']['final']['2'], ", round", match['rounds'], ", odds", match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['x'],":",match['odds']['pinnacle']['final']['2'])
        curRound = int(match['rounds'])
        roundsPnl[curRound] = roundsPnl[curRound] + returns
        return returns
    elif predict == '2' or predict == '3':
        away_dnb_odds = match['odds']['pinnacle']['final']['2'] * (match['odds']['pinnacle']['final']['x'] - 1) / match['odds']['pinnacle']['final']['x']
        away_dc_odds = match['odds']['pinnacle']['final']['2'] * match['odds']['pinnacle']['final']['x'] / (match['odds']['pinnacle']['final']['2'] + match['odds']['pinnacle']['final']['x'])
        #poReturn = Returns(match['probabilities']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient)
        #if poReturn < qualifyBenmark:
            #print("Game", game_id, "away return not qualify", poReturn)
            #return 0
        #if match['odds']['macau_slot']['final']['2'] <= match['odds']['hkjc']['final']['2']:
            #return 0
        returns = IsPredictRight2(predict, match['probabilities']['pinnacle']['final']['2'], match['odds']['pinnacle']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient, match['result'], match['home_score'] - match['away_score'], match['odds']['pinnacle']['final']['1'])
        #print("Game", int(game_id), match['league_name'], "pred away result", match['result'], "return", returns, "calcProb", prob, "score", match['home_score'], ":", match['away_score'], ", prob is", prob, ",", match['probabilities']['pinnacle']['final']['1'], ":", match['probabilities']['pinnacle']['final']['x'], ":", match['probabilities']['pinnacle']['final']['2'], ", round is", match['rounds'], ", odds", match['odds']['pinnacle']['final']['1'],":",match['odds']['pinnacle']['final']['x'],":",match['odds']['pinnacle']['final']['2'])
        curRound = int(match['rounds'])
        roundsPnl[curRound] = roundsPnl[curRound] + returns
        return returns

number_of_rounds = 48
roundsPnl = [0 for x in range(number_of_rounds)]
allRoundPnl = [0 for x in range(number_of_rounds)]
pnl = 0
right = 0
wrong = 0

def LoadData(file_name):
    with open(file_name) as json_file:
        allMatches = {}
        matches = json.load(json_file)
        for match in matches:
            #time = match['kickoff'] + match['home_team_id']
            #allMatches[float(time)] = match
            allQualifiedGames[int(match['game_id'])] = match

def IsGameQualified(lookbackTime, probMove, bookie, correct_result, wrong_result, movements):
        allMatchesInSeq = collections.OrderedDict(sorted(allQualifiedGames.items()))
        global right
        global wrong
        global pnl
        for time, match in allMatchesInSeq.items():
            predict = QualificationCheck().is_qualified(match, lookbackTime, probMove, bookie, movements)
            if predict == 'x':
                #print("Match", match['game_id'], "unqualified")
                continue
            match['predict'] = predict
            #allQualifiedGames[int(match['game_id'])] = match
            prob = []
            prob.append(0.5)
            perPnl = 0
            if predict == '1':
                perPnl = CalculateOdds(match['game_id'], prob[0], roundsPnl)
                #print("Match", match['game_id'], "qualified with home win with", movements[match['game_id']], match['home_score'], ":", match['away_score'], "return", perPnl, match['odds']['pinnacle']['final']['1'], ":", match['odds']['pinnacle']['final']['x'], ":", match['odds']['pinnacle']['final']['2'])
            if predict == '2':
                perPnl = CalculateOdds(match['game_id'], prob[0], roundsPnl)
                #print("Match", match['game_id'], "qualified with away win with", movements[match['game_id']], match['home_score'], ":", match['away_score'], "return", perPnl, match['odds']['pinnacle']['final']['1'], ":", match['odds']['pinnacle']['final']['x'], ":", match['odds']['pinnacle']['final']['2'])
            if predict == '3':
                #perPnl = 0
                perPnl = CalculateOdds(match['game_id'], prob[0], roundsPnl)
                #print("Match", match['game_id'], "qualified with home not win with", movements[match['game_id']], match['home_score'], ":", match['away_score'], "return", perPnl, match['odds']['pinnacle']['final']['1'], ":", match['odds']['pinnacle']['final']['x'], ":", match['odds']['pinnacle']['final']['2'])
            if predict == '4':
                perPnl = CalculateOdds(match['game_id'], prob[0], roundsPnl)
                #print("Match", match['game_id'], "qualified with away not win with", movements[match['game_id']], match['home_score'], ":", match['away_score'], "return", perPnl, match['odds']['pinnacle']['final']['1'], ":", match['odds']['pinnacle']['final']['x'], ":", match['odds']['pinnacle']['final']['2'])
            if perPnl > 0:
                right = right + 1
            elif perPnl < 0:
                wrong = wrong + 1
            pnl = pnl + perPnl

correct_predict_result = []
wrong_predict_result = []

times = []
times.append(5 * 60)
times.append(10 * 60)
times.append(15 * 60)
times.append(20 * 60)
times.append(25 * 60)
times.append(30 * 60)
times.append(60 * 60)
times.append(90 * 60)
times.append(120 * 60)
times.append(150 * 60)
times.append(180 * 60)
times.append(210 * 60)
times.append(240 * 60)
times.append(270 * 60)
times.append(300 * 60)
times.append(330 * 60)
times.append(360 * 60)
times.append(390 * 60)
times.append(420 * 60)
times.append(450 * 60)
times.append(480 * 60)
times.append(510 * 60)
times.append(540 * 60)
times.append(570 * 60)
times.append(600 * 60)

probMoves = []
probMoves.append(0.001)
probMoves.append(0.002)
probMoves.append(0.003)
probMoves.append(0.004)
probMoves.append(0.005)
probMoves.append(0.006)
probMoves.append(0.007)
probMoves.append(0.008)
probMoves.append(0.009)
probMoves.append(0.01)
probMoves.append(0.015)
probMoves.append(0.02)
probMoves.append(0.025)
probMoves.append(0.03)
probMoves.append(0.035)
probMoves.append(0.04)
probMoves.append(0.045)
probMoves.append(0.05)

bookies = []
bookies.append('macau_slot')
bookies.append('pinnacle')
bookies.append('bet365')
bookies.append('will_hill')
bookies.append('hkjc')
bookies.append('interwetten')

bookies.append('ladbroke')
bookies.append('betvictor')
bookies.append('sb')
bookies.append('betfair')
bookies.append('setantabet')
bookies.append('bwin')
bookies.append('coral')
bookies.append('eurobet')
bookies.append('snai')
bookies.append('sbobet')
bookies.append('easybet')
bookies.append('smarkets')
bookies.append('matchbook')
bookies.append('betdaq')
bookies.append('betclick')
bookies.append('betfred')
bookies.append('betway')
bookies.append('bodog')
bookies.append('bovada')
bookies.append('cashpoint')
bookies.append('championsbet')
bookies.append('dafabet')
bookies.append('jetbull')
bookies.append('skybet')
bookies.append('sportsbet')

leagues = []
#leagues.append('English Premier League-')
#leagues.append('German Bundesliga-')
#leagues.append('German Bundesliga 2-')
#leagues.append('England Championship-')
#leagues.append('Spanish La Liga-')
#leagues.append('Spanish Segunda Division-')
#leagues.append('Holland Eredivisie-')
#leagues.append('Italian Serie A-')
#leagues.append('France Ligue 1-')
#leagues.append('France Ligue 2-')
#leagues.append('England League 1-')
leagues.append('England League 2-')
#leagues.append('Portugal Primera Liga-')
#leagues.append('Turkish Super Liga-')
#leagues.append('Holland Jupiler League-')
#leagues.append('USA Major League Soccer-')

#leagues.append('J-League Division 2-')

seasons = []
seasons.append('2018-2019')
seasons.append('2017-2018')
seasons.append('2016-2017')
seasons.append('2015-2016')
seasons.append('2014-2015')
seasons.append('2013-2014')

#seasons.append('2019')
#seasons.append('2018')
#seasons.append('2017')
#seasons.append('2016')
#seasons.append('2015')
#seasons.append('2014')

for league in leagues:
    for season in seasons:
        file_name = file_header + league + season + ".json"
        LoadData(file_name)

bestPnl = 0
for bookie in bookies:
    print("Bookie", bookie)
    for time in times:
        for probMove in probMoves:
            movements = {}
            pnl = 0
            right = 0
            wrong = 0

            IsGameQualified(time, probMove, bookie, correct_predict_result, wrong_predict_result, movements)

            if pnl > bestPnl:
                bestPnl = pnl
            if (right + wrong) > 0:
                winrate = right / (right + wrong)
                perMatchReturn = pnl / (right + wrong)
                if (right + wrong) > 120 and ((winrate >= 0.55 and perMatchReturn >= 0.08) or winrate < 0.4):
                    print("probMove", probMove, "time", time, "win rate", right / (right + wrong), ", total bet matches", right + wrong, ", pnl", pnl, ", per match return", pnl / (right + wrong))

        #index = 0
        #curPnl = 0
        #for data in roundsPnl:
            #curPnl = curPnl + data
            #allRoundPnl[index] = curPnl
            #index = index + 1

        #plt.figure(1)
        #plt.plot(allRoundPnl, 'r-')
        #plt.show()

print("Best pnl", bestPnl)
