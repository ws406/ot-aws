from datetime import datetime
import numpy as np

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
    disqualified = 'x'

    def __init__(self):
        pass

    def is_qualified(self, game_data):

        exceptions = None
        prediction = self.disqualified

        try:
            test = game_data['probabilities']['hkjc']
            test = game_data['probabilities']['interwetten']
            test = game_data['probabilities']['macau_slot']
            test = game_data['probabilities']['will_hill']
            test = game_data['probabilities']['pinnacle']
            test = game_data['probabilities']['bet365']
            test = game_data['odds']['hkjc']
            test = game_data['odds']['interwetten']
            test = game_data['odds']['macau_slot']
            test = game_data['odds']['will_hill']
            test = game_data['odds']['pinnacle']
            test = game_data['odds']['bet365']
            #print("league id", game_data['league_id'], ", game id", game_data['game_id'])

            timeList = find_open_final(game_data['odds']['macau_slot'])
            game_data['odds']['macau_slot']['open'] = game_data['odds']['macau_slot'][timeList[0]]
            game_data['odds']['macau_slot']['final'] = game_data['odds']['macau_slot'][timeList[1]]
            game_data['odds']['macau_slot']['open']['1'] = float(game_data['odds']['macau_slot']['open']['1'])
            game_data['odds']['macau_slot']['open']['x'] = float(game_data['odds']['macau_slot']['open']['x'])
            game_data['odds']['macau_slot']['open']['2'] = float(game_data['odds']['macau_slot']['open']['2'])
            game_data['odds']['macau_slot']['final']['1'] = float(game_data['odds']['macau_slot']['final']['1'])
            game_data['odds']['macau_slot']['final']['x'] = float(game_data['odds']['macau_slot']['final']['x'])
            game_data['odds']['macau_slot']['final']['2'] = float(game_data['odds']['macau_slot']['final']['2'])
            timeList = find_open_final(game_data['odds']['hkjc'])
            game_data['odds']['hkjc']['open'] = game_data['odds']['hkjc'][timeList[0]]
            game_data['odds']['hkjc']['final'] = game_data['odds']['hkjc'][timeList[1]]
            game_data['odds']['hkjc']['open']['1'] = float(game_data['odds']['hkjc']['open']['1'])
            game_data['odds']['hkjc']['open']['x'] = float(game_data['odds']['hkjc']['open']['x'])
            game_data['odds']['hkjc']['open']['2'] = float(game_data['odds']['hkjc']['open']['2'])
            game_data['odds']['hkjc']['final']['1'] = float(game_data['odds']['hkjc']['final']['1'])
            game_data['odds']['hkjc']['final']['x'] = float(game_data['odds']['hkjc']['final']['x'])
            game_data['odds']['hkjc']['final']['2'] = float(game_data['odds']['hkjc']['final']['2'])
            timeList = find_open_final(game_data['odds']['will_hill'])
            game_data['odds']['will_hill']['open'] = game_data['odds']['will_hill'][timeList[0]]
            game_data['odds']['will_hill']['final'] = game_data['odds']['will_hill'][timeList[1]]
            game_data['odds']['will_hill']['open']['1'] = float(game_data['odds']['will_hill']['open']['1'])
            game_data['odds']['will_hill']['open']['x'] = float(game_data['odds']['will_hill']['open']['x'])
            game_data['odds']['will_hill']['open']['2'] = float(game_data['odds']['will_hill']['open']['2'])
            game_data['odds']['will_hill']['final']['1'] = float(game_data['odds']['will_hill']['final']['1'])
            game_data['odds']['will_hill']['final']['x'] = float(game_data['odds']['will_hill']['final']['x'])
            game_data['odds']['will_hill']['final']['2'] = float(game_data['odds']['will_hill']['final']['2'])
            timeList = find_open_final(game_data['odds']['bet365'])
            game_data['odds']['bet365']['open'] = game_data['odds']['bet365'][timeList[0]]
            game_data['odds']['bet365']['final'] = game_data['odds']['bet365'][timeList[1]]
            game_data['odds']['bet365']['open']['1'] = float(game_data['odds']['bet365']['open']['1'])
            game_data['odds']['bet365']['open']['x'] = float(game_data['odds']['bet365']['open']['x'])
            game_data['odds']['bet365']['open']['2'] = float(game_data['odds']['bet365']['open']['2'])
            game_data['odds']['bet365']['final']['1'] = float(game_data['odds']['bet365']['final']['1'])
            game_data['odds']['bet365']['final']['x'] = float(game_data['odds']['bet365']['final']['x'])
            game_data['odds']['bet365']['final']['2'] = float(game_data['odds']['bet365']['final']['2'])
            timeList = find_open_final(game_data['odds']['pinnacle'])
            game_data['odds']['pinnacle']['open'] = game_data['odds']['pinnacle'][timeList[0]]
            game_data['odds']['pinnacle']['final'] = game_data['odds']['pinnacle'][timeList[1]]
            game_data['odds']['pinnacle']['open']['1'] = float(game_data['odds']['pinnacle']['open']['1'])
            game_data['odds']['pinnacle']['open']['x'] = float(game_data['odds']['pinnacle']['open']['x'])
            game_data['odds']['pinnacle']['open']['2'] = float(game_data['odds']['pinnacle']['open']['2'])
            game_data['odds']['pinnacle']['final']['1'] = float(game_data['odds']['pinnacle']['final']['1'])
            game_data['odds']['pinnacle']['final']['x'] = float(game_data['odds']['pinnacle']['final']['x'])
            game_data['odds']['pinnacle']['final']['2'] = float(game_data['odds']['pinnacle']['final']['2'])
            timeList = find_open_final(game_data['odds']['interwetten'])
            game_data['odds']['interwetten']['open'] = game_data['odds']['interwetten'][timeList[0]]
            game_data['odds']['interwetten']['final'] = game_data['odds']['interwetten'][timeList[1]]
            game_data['odds']['interwetten']['open']['1'] = float(game_data['odds']['interwetten']['open']['1'])
            game_data['odds']['interwetten']['open']['x'] = float(game_data['odds']['interwetten']['open']['x'])
            game_data['odds']['interwetten']['open']['2'] = float(game_data['odds']['interwetten']['open']['2'])
            game_data['odds']['interwetten']['final']['1'] = float(game_data['odds']['interwetten']['final']['1'])
            game_data['odds']['interwetten']['final']['x'] = float(game_data['odds']['interwetten']['final']['x'])
            game_data['odds']['interwetten']['final']['2'] = float(game_data['odds']['interwetten']['final']['2'])
            #print("time 1 is", timeList[0], ", time 2 is", timeList[1])
            if game_data['odds']['macau_slot']['open']['1'] < game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] > game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] < game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] > game_data['odds']['will_hill']['final']['2']:
                #game_data['odds']['bet365']['open']['1'] < game_data['odds']['bet365']['final']['1'] and \
                #game_data['odds']['bet365']['open']['2'] > game_data['odds']['bet365']['final']['2']:

                prediction = self.prediction_away_win

            elif game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2']:
                #game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
                #game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2']:

                prediction = self.prediction_home_win

        except (TypeError, KeyError):
            exceptions = 'missing required odds'

        return prediction

    def _get_readable_kickoff_time(self, kickoff_in_linux_ts):
        return datetime.fromtimestamp(kickoff_in_linux_ts).strftime('%Y-%m-%d %H:%M:%S')