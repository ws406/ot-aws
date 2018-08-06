from src.strategy_finding.feature_builder.interface import FeatureBuilderInterface
import numpy as np

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

def Operation(data1, data2):
    #return np.log(data1 / data2)
    return (data1 - data2) / 100.0
    #return data1 - data2
    #return (data1 / data2)
    #return 0

# Features are:
#  4: the opening probabilities for the predicted result from 4 bookies: MS, Bet365, WH, PIN
#  4: the delta probabilities for the predicted result from 4 bookies: MS, Bet365, WH, PIN
#  1: home or away
class WDLProbabilitiesFeatureBuilder2(FeatureBuilderInterface):

    def get_features(self, labelled_data: dict):
        print("Running feature builder - 1x2_probabilities with " + str(len(labelled_data)) + " games")

        header = [
            'label',
            'h_or_a',
            'open_prob_ms',
            'open_prob_365',
            'open_prob_wh',
            'open_prob_pin',
            'delta_prob_ms',
            'delta_prob_365',
            'delta_prob_wh',
            'delta_prob_pin'
        ]

        featured_data = np.empty((0, 61))

        for data in labelled_data:

            row = []
            row.append(data['result'])
            row.append(data['game_id'])
            row.append(data['potentialReturn'])
            if data['prediction'] == '1':
                row.append(1)
            else:
                row.append(0)

            h_or_a = str(data['prediction'])

            macau_slot = GenerateProbData(data['probabilities']['macau_slot'], data['kickoff'], h_or_a)
            bet365 = GenerateProbData(data['probabilities']['bet365'], data['kickoff'], h_or_a)
            pinnacle = GenerateProbData(data['probabilities']['pinnacle'], data['kickoff'], h_or_a)
            will_hill = GenerateProbData(data['probabilities']['will_hill'], data['kickoff'], h_or_a)
            hkjc = GenerateProbData(data['probabilities']['hkjc'], data['kickoff'], h_or_a)
            interwetten = GenerateProbData(data['probabilities']['interwetten'], data['kickoff'], h_or_a)

            row.append(macau_slot[0])
            i = 1
            while i < len(macau_slot):
                if macau_slot[i] == 0:
                    row.append(0)
                else:
                    row.append(Operation(macau_slot[i - 1], macau_slot[i]))
                i += 1

            row.append(bet365[0])
            i = 1
            while i < len(bet365):
                if bet365[i] == 0:
                    row.append(0)
                else:
                    row.append(Operation(bet365[i - 1], bet365[i]))
                i += 1

            row.append(pinnacle[0])
            i = 1
            while i < len(pinnacle):
                if pinnacle[i] == 0:
                    row.append(0)
                else:
                    row.append(Operation(pinnacle[i - 1], pinnacle[i]))
                i += 1

            row.append(will_hill[0])
            i = 1
            while i < len(will_hill):
                if will_hill[i] == 0:
                    row.append(0)
                else:
                    row.append(Operation(will_hill[i - 1], will_hill[i]))
                i += 1

            row.append(hkjc[0])
            i = 1
            while i < len(hkjc):
                if hkjc[i] == 0:
                    row.append(0)
                else:
                    row.append(Operation(hkjc[i - 1], hkjc[i]))
                i += 1

            row.append(interwetten[0])
            i = 1
            while i < len(interwetten):
                if interwetten[i] == 0:
                    row.append(0)
                else:
                    row.append(Operation(interwetten[i - 1], interwetten[i]))
                i += 1

            row.append(float(data['rounds']) / float((data['size'] -1) * 2))
            homeTeamRank = 0
            awayTeamRank = 0
            if data['home_team_rank'] is None or data['home_team_rank'] > 100:
                homeTeamRank = 0
            else:
                homeTeamRank = data['home_team_rank']
            if data['away_team_rank'] is None or data['away_team_rank'] > 100:
                awayTeamRank = 0
            else:
                awayTeamRank = data['away_team_rank']
            if h_or_a == '1':
                row.append(homeTeamRank / data['size'])
            else:
                row.append(awayTeamRank / data['size'])
            if h_or_a == '1':
                if homeTeamRank == 0 or data['size'] == 0:
                    row.append(0)
                else:
                    row.append(Operation(awayTeamRank / data['size'], homeTeamRank / data['size']))
            else:
                if awayTeamRank == 0 or data['size'] == 0:
                    row.append(0)
                else:
                    row.append(Operation(homeTeamRank / data['size'], awayTeamRank / data['size']))

            #score = str(data['home_score']) + ":" + str(data['away_score'])
            #row.append(score)

            featured_data = np.append(featured_data, [row], axis=0)

        return header, featured_data