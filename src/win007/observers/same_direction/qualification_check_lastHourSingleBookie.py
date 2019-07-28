from datetime import datetime
import numpy as np
import math
import collections

def find_open_final(data):
    timeList = []
    probOpenTime = 9999999999
    probFinalTime = 0
    for key, value in data.items():
        if key == "final" or key == "open":
            continue
        itemTime = int(key)
        #print("Time is", itemTime, "value is", value)
        if probOpenTime > itemTime:
            probOpenTime = itemTime
        if probFinalTime < itemTime:
            probFinalTime = itemTime
    timeList.append(str(probOpenTime))
    timeList.append(str(probFinalTime))
    #print("Time 1 is ", timeList[0], ", time 2 is ", timeList[1])
    return timeList

class QualificationCheck:

    prediction_home_win = '1'
    prediction_away_win = '2'
    prediction_home_not_win = '3'
    prediction_away_not_win = '4'
    disqualified = 'x'
    notset = '0'

    def __init__(self):
        pass

    def is_qualified(self, game_data, lookbackTime, percent, bookie, movements):

        exceptions = None
        prediction = self.disqualified

        try:
            timeList = find_open_final(game_data['odds']['pinnacle'])
            game_data['odds']['pinnacle']['open'] = game_data['odds']['pinnacle'][timeList[0]]
            game_data['odds']['pinnacle']['final'] = game_data['odds']['pinnacle'][timeList[1]]
            game_data['odds']['pinnacle']['open']['1'] = float(game_data['odds']['pinnacle']['open']['1'])
            game_data['odds']['pinnacle']['open']['x'] = float(game_data['odds']['pinnacle']['open']['x'])
            game_data['odds']['pinnacle']['open']['2'] = float(game_data['odds']['pinnacle']['open']['2'])
            game_data['odds']['pinnacle']['final']['1'] = float(game_data['odds']['pinnacle']['final']['1'])
            game_data['odds']['pinnacle']['final']['x'] = float(game_data['odds']['pinnacle']['final']['x'])
            game_data['odds']['pinnacle']['final']['2'] = float(game_data['odds']['pinnacle']['final']['2'])
            timeList = find_open_final(game_data['probabilities']['pinnacle'])
            game_data['probabilities']['pinnacle']['open'] = game_data['probabilities']['pinnacle'][timeList[0]]
            game_data['probabilities']['pinnacle']['final'] = game_data['probabilities']['pinnacle'][timeList[1]]
            game_data['probabilities']['pinnacle']['open']['1'] = float(game_data['probabilities']['pinnacle']['open']['1'])
            game_data['probabilities']['pinnacle']['open']['x'] = float(game_data['probabilities']['pinnacle']['open']['x'])
            game_data['probabilities']['pinnacle']['open']['2'] = float(game_data['probabilities']['pinnacle']['open']['2'])
            game_data['probabilities']['pinnacle']['final']['1'] = float(game_data['probabilities']['pinnacle']['final']['1'])
            game_data['probabilities']['pinnacle']['final']['x'] = float(game_data['probabilities']['pinnacle']['final']['x'])
            game_data['probabilities']['pinnacle']['final']['2'] = float(game_data['probabilities']['pinnacle']['final']['2'])

            test = game_data['probabilities'][bookie]

            matchInSeq = collections.OrderedDict(sorted(game_data['probabilities'][bookie].items()))
            kickoffTime = int(game_data['kickoff'])
            qualifiedData = {}
            lastRecord = []
            lastRecord.append(0)
            for timeStr, prob in matchInSeq.items():
                if timeStr == "final" or timeStr == "open":
                    continue
                time = int(timeStr)
                if time >= kickoffTime - lookbackTime:
                    qualifiedData[time] = prob
                else:
                    if time > lastRecord[0]:
                        lastRecord[0] = time
            curTime = int(lastRecord[0])
            if curTime > 0:
                qualifiedData[curTime] = game_data['probabilities'][bookie][str(curTime)]

            qualifiedDataInSeq = collections.OrderedDict(sorted(qualifiedData.items()))
            #if game_data['game_id'] == 1395221:
                #print(lookbackTime, kickoffTime, lastRecord[0], qualifiedDataInSeq)
            allProb = []
            allProbAway = []
            for time, prob in qualifiedDataInSeq.items():
                if time != 0:
                    allProb.append(prob['1'])
                    allProbAway.append(prob['2'])
                
            index = 0
            finalIndex = len(allProb) - 1
            
            isSameOrder = False
            direction = 0
            while index < finalIndex:
                diffHome = float(allProb[index + 1] - allProb[index])
                diffAway = float(allProbAway[index + 1] - allProbAway[index])
                if abs(diffHome) > abs(diffAway) and abs(diffHome) >= percent:
                    movements[game_data['game_id']] = diffHome*100
                    if diffHome > 0: # home win
                        if direction == 0 or direction == 1:
                            isSameOrder = True
                            direction = 1
                        else: 
                            isSameOrder = False
                            break
                    elif diffHome < 0: # home not win
                        if direction == 0 or direction == 3:
                            isSameOrder = True
                            direction = 3
                        else: 
                            isSameOrder = False
                            break
                elif abs(diffHome) < abs(diffAway) and abs(diffAway) >= percent:
                    movements[game_data['game_id']] = diffAway*100
                    if diffAway > 0:
                        if direction == 0 or direction == 2:
                            isSameOrder = True
                            direction = 2
                        else: 
                            isSameOrder = False
                            break
                    elif diffAway < 0:
                        if direction == 0 or direction == 4:
                            isSameOrder = True
                            direction = 4
                        else: 
                            isSameOrder = False
                            break
                index = index + 1

            #largestDelta = 0
            #while index < finalIndex:
                #diffHome = float(allProb[index + 1] - allProb[index])
                #diffAway = float(allProbAway[index + 1] - allProbAway[index])
                #if abs(diffHome) > abs(diffAway) and abs(diffHome) >= percent:
                    #if diffHome > 0: # home win
                        #if abs(diffHome) > largestDelta:
                            #largestDelta = abs(diffHome)
                            #direction = 1
                            #isSameOrder = True
                    #elif diffHome < 0: # home not win
                        #if abs(diffHome) > largestDelta:
                            #largestDelta = abs(diffHome)
                            #direction = 3
                            #isSameOrder = True
                #elif abs(diffHome) < abs(diffAway) and abs(diffAway) >= percent:
                    #if diffAway > 0:
                        #if abs(diffAway) > largestDelta:
                            #largestDelta = abs(diffAway)
                            #isSameOrder = True
                            #direction = 2
                    #elif diffAway < 0:
                        #if abs(diffAway) > largestDelta:
                            #largestDelta = abs(diffAway)
                            #isSameOrder = True
                            #direction = 4
                #index = index + 1

            if isSameOrder:
                if direction == 1:
                    prediction = self.prediction_home_win
                    #prediction = self.prediction_home_not_win
                elif direction == 2:
                    prediction = self.prediction_away_win
                    #prediction = self.prediction_away_not_win
                elif direction == 3:
                    prediction = self.prediction_home_not_win
                    #prediction = self.prediction_home_win
                elif direction == 4:
                    prediction = self.prediction_away_not_win
                    #prediction = self.prediction_away_win

            coefficient = 0.98
            benchmarkOdds = 1.5
            benchmarkOdds2 = 3.0
            home_dc_odds = coefficient * (game_data['odds']['pinnacle']['final']['1'] * game_data['odds']['pinnacle']['final']['x'] / (game_data['odds']['pinnacle']['final']['1'] + game_data['odds']['pinnacle']['final']['x']))
            away_dc_odds = coefficient * (game_data['odds']['pinnacle']['final']['2'] * game_data['odds']['pinnacle']['final']['x'] / (game_data['odds']['pinnacle']['final']['2'] + game_data['odds']['pinnacle']['final']['x']))
            if prediction == self.prediction_home_win and (game_data['odds']['pinnacle']['final']['1'] < benchmarkOdds or game_data['odds']['pinnacle']['final']['1'] >= benchmarkOdds2):
                return self.disqualified
            elif prediction == self.prediction_away_win and (game_data['odds']['pinnacle']['final']['2'] < benchmarkOdds or game_data['odds']['pinnacle']['final']['2'] >= benchmarkOdds2):
                return self.disqualified
            elif prediction == self.prediction_home_not_win and (away_dc_odds < benchmarkOdds or away_dc_odds >= benchmarkOdds2):
                return self.disqualified
            elif prediction == self.prediction_away_not_win and (home_dc_odds < benchmarkOdds or home_dc_odds >= benchmarkOdds2):
                return self.disqualified

        except (TypeError, KeyError):
            #print("missing odds, skip...")
            None

        return prediction

    def _get_readable_kickoff_time(self, kickoff_in_linux_ts):
        return datetime.fromtimestamp(kickoff_in_linux_ts).strftime('%Y-%m-%d %H:%M:%S')
