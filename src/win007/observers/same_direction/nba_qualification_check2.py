from datetime import datetime

def find_open_final(data):
    timeList = []
    probOpenTime = 9999999999
    probFinalTime = 0
    for key, value in data.items():
        if key == "final" or key == "open":
            continue
        itemTime = int(key)
        if probOpenTime > itemTime:
            probOpenTime = itemTime
        if probFinalTime < itemTime:
            probFinalTime = itemTime
    timeList.append(str(probOpenTime))
    timeList.append(str(probFinalTime))
    return timeList

class QualificationCheck:

    prediction_home_win = '1'
    prediction_away_win = '2'
    disqualified = 'x'

    def __init__(self):
        pass

    def is_qualified(self, game_data):

        prediction = self.disqualified

        try:

            timeList = find_open_final(game_data['odds']['easybet'])
            game_data['odds']['easybet']['open'] = game_data['odds']['easybet'][timeList[0]]
            game_data['odds']['easybet']['final'] = game_data['odds']['easybet'][timeList[1]]
            game_data['odds']['easybet']['open']['1'] = float(game_data['odds']['easybet']['open']['1'])
            game_data['odds']['easybet']['open']['2'] = float(game_data['odds']['easybet']['open']['2'])
            game_data['odds']['easybet']['final']['1'] = float(game_data['odds']['easybet']['final']['1'])
            game_data['odds']['easybet']['final']['2'] = float(game_data['odds']['easybet']['final']['2'])
            timeList = find_open_final(game_data['probabilities']['easybet'])
            game_data['probabilities']['easybet']['open'] = game_data['probabilities']['easybet'][timeList[0]]
            game_data['probabilities']['easybet']['final'] = game_data['probabilities']['easybet'][timeList[1]]
            game_data['probabilities']['easybet']['open']['1'] = float(game_data['probabilities']['easybet']['open']['1'])
            game_data['probabilities']['easybet']['open']['2'] = float(game_data['probabilities']['easybet']['open']['2'])
            game_data['probabilities']['easybet']['final']['1'] = float(game_data['probabilities']['easybet']['final']['1'])
            game_data['probabilities']['easybet']['final']['2'] = float(game_data['probabilities']['easybet']['final']['2'])

            timeList = find_open_final(game_data['odds']['skybet'])
            game_data['odds']['skybet']['open'] = game_data['odds']['skybet'][timeList[0]]
            game_data['odds']['skybet']['final'] = game_data['odds']['skybet'][timeList[1]]
            game_data['odds']['skybet']['open']['1'] = float(game_data['odds']['skybet']['open']['1'])
            game_data['odds']['skybet']['open']['2'] = float(game_data['odds']['skybet']['open']['2'])
            game_data['odds']['skybet']['final']['1'] = float(game_data['odds']['skybet']['final']['1'])
            game_data['odds']['skybet']['final']['2'] = float(game_data['odds']['skybet']['final']['2'])
            timeList = find_open_final(game_data['probabilities']['skybet'])
            game_data['probabilities']['skybet']['open'] = game_data['probabilities']['skybet'][timeList[0]]
            game_data['probabilities']['skybet']['final'] = game_data['probabilities']['skybet'][timeList[1]]
            game_data['probabilities']['skybet']['open']['1'] = float(game_data['probabilities']['skybet']['open']['1'])
            game_data['probabilities']['skybet']['open']['2'] = float(game_data['probabilities']['skybet']['open']['2'])
            game_data['probabilities']['skybet']['final']['1'] = float(game_data['probabilities']['skybet']['final']['1'])
            game_data['probabilities']['skybet']['final']['2'] = float(game_data['probabilities']['skybet']['final']['2'])

            timeList = find_open_final(game_data['odds']['ladbroke'])
            game_data['odds']['ladbroke']['open'] = game_data['odds']['ladbroke'][timeList[0]]
            game_data['odds']['ladbroke']['final'] = game_data['odds']['ladbroke'][timeList[1]]
            game_data['odds']['ladbroke']['open']['1'] = float(game_data['odds']['ladbroke']['open']['1'])
            game_data['odds']['ladbroke']['open']['2'] = float(game_data['odds']['ladbroke']['open']['2'])
            game_data['odds']['ladbroke']['final']['1'] = float(game_data['odds']['ladbroke']['final']['1'])
            game_data['odds']['ladbroke']['final']['2'] = float(game_data['odds']['ladbroke']['final']['2'])
            timeList = find_open_final(game_data['probabilities']['ladbroke'])
            game_data['probabilities']['ladbroke']['open'] = game_data['probabilities']['ladbroke'][timeList[0]]
            game_data['probabilities']['ladbroke']['final'] = game_data['probabilities']['ladbroke'][timeList[1]]
            game_data['probabilities']['ladbroke']['open']['1'] = float(game_data['probabilities']['ladbroke']['open']['1'])
            game_data['probabilities']['ladbroke']['open']['2'] = float(game_data['probabilities']['ladbroke']['open']['2'])
            game_data['probabilities']['ladbroke']['final']['1'] = float(game_data['probabilities']['ladbroke']['final']['1'])
            game_data['probabilities']['ladbroke']['final']['2'] = float(game_data['probabilities']['ladbroke']['final']['2'])

            timeList = find_open_final(game_data['odds']['will_hill'])
            game_data['odds']['will_hill']['open'] = game_data['odds']['will_hill'][timeList[0]]
            game_data['odds']['will_hill']['final'] = game_data['odds']['will_hill'][timeList[1]]
            game_data['odds']['will_hill']['open']['1'] = float(game_data['odds']['will_hill']['open']['1'])
            game_data['odds']['will_hill']['open']['2'] = float(game_data['odds']['will_hill']['open']['2'])
            game_data['odds']['will_hill']['final']['1'] = float(game_data['odds']['will_hill']['final']['1'])
            game_data['odds']['will_hill']['final']['2'] = float(game_data['odds']['will_hill']['final']['2'])
            timeList = find_open_final(game_data['probabilities']['will_hill'])
            game_data['probabilities']['will_hill']['open'] = game_data['probabilities']['will_hill'][timeList[0]]
            game_data['probabilities']['will_hill']['final'] = game_data['probabilities']['will_hill'][timeList[1]]
            game_data['probabilities']['will_hill']['open']['1'] = float(game_data['probabilities']['will_hill']['open']['1'])
            game_data['probabilities']['will_hill']['open']['2'] = float(game_data['probabilities']['will_hill']['open']['2'])
            game_data['probabilities']['will_hill']['final']['1'] = float(game_data['probabilities']['will_hill']['final']['1'])
            game_data['probabilities']['will_hill']['final']['2'] = float(game_data['probabilities']['will_hill']['final']['2'])

            timeList = find_open_final(game_data['odds']['marathonbet'])
            game_data['odds']['marathonbet']['open'] = game_data['odds']['marathonbet'][timeList[0]]
            game_data['odds']['marathonbet']['final'] = game_data['odds']['marathonbet'][timeList[1]]
            game_data['odds']['marathonbet']['open']['1'] = float(game_data['odds']['marathonbet']['open']['1'])
            game_data['odds']['marathonbet']['open']['2'] = float(game_data['odds']['marathonbet']['open']['2'])
            game_data['odds']['marathonbet']['final']['1'] = float(game_data['odds']['marathonbet']['final']['1'])
            game_data['odds']['marathonbet']['final']['2'] = float(game_data['odds']['marathonbet']['final']['2'])
            timeList = find_open_final(game_data['probabilities']['marathonbet'])
            game_data['probabilities']['marathonbet']['open'] = game_data['probabilities']['marathonbet'][timeList[0]]
            game_data['probabilities']['marathonbet']['final'] = game_data['probabilities']['marathonbet'][timeList[1]]
            game_data['probabilities']['marathonbet']['open']['1'] = float(game_data['probabilities']['marathonbet']['open']['1'])
            game_data['probabilities']['marathonbet']['open']['2'] = float(game_data['probabilities']['marathonbet']['open']['2'])
            game_data['probabilities']['marathonbet']['final']['1'] = float(game_data['probabilities']['marathonbet']['final']['1'])
            game_data['probabilities']['marathonbet']['final']['2'] = float(game_data['probabilities']['marathonbet']['final']['2'])

            timeList = find_open_final(game_data['odds']['pinnacle'])
            game_data['odds']['pinnacle']['open'] = game_data['odds']['pinnacle'][timeList[0]]
            game_data['odds']['pinnacle']['final'] = game_data['odds']['pinnacle'][timeList[1]]
            game_data['odds']['pinnacle']['open']['1'] = float(game_data['odds']['pinnacle']['open']['1'])
            game_data['odds']['pinnacle']['open']['2'] = float(game_data['odds']['pinnacle']['open']['2'])
            game_data['odds']['pinnacle']['final']['1'] = float(game_data['odds']['pinnacle']['final']['1'])
            game_data['odds']['pinnacle']['final']['2'] = float(game_data['odds']['pinnacle']['final']['2'])
            timeList = find_open_final(game_data['probabilities']['pinnacle'])
            game_data['probabilities']['pinnacle']['open'] = game_data['probabilities']['pinnacle'][timeList[0]]
            game_data['probabilities']['pinnacle']['final'] = game_data['probabilities']['pinnacle'][timeList[1]]
            game_data['probabilities']['pinnacle']['open']['1'] = float(game_data['probabilities']['pinnacle']['open']['1'])
            game_data['probabilities']['pinnacle']['open']['2'] = float(game_data['probabilities']['pinnacle']['open']['2'])
            game_data['probabilities']['pinnacle']['final']['1'] = float(game_data['probabilities']['pinnacle']['final']['1'])
            game_data['probabilities']['pinnacle']['final']['2'] = float(game_data['probabilities']['pinnacle']['final']['2'])

            if (game_data['probabilities']['marathonbet']['open']['2'] < game_data['probabilities']['marathonbet']['final']['2'] and \
                game_data['probabilities']['marathonbet']['open']['1'] > game_data['probabilities']['marathonbet']['final']['1']) or \
               (game_data['probabilities']['pinnacle']['open']['2'] < game_data['probabilities']['pinnacle']['final']['2'] and \
                game_data['probabilities']['pinnacle']['open']['1'] > game_data['probabilities']['pinnacle']['final']['1']):

                prediction = self.prediction_away_win

            elif (game_data['probabilities']['marathonbet']['open']['2'] > game_data['probabilities']['marathonbet']['final']['2'] and \
                game_data['probabilities']['marathonbet']['open']['1'] < game_data['probabilities']['marathonbet']['final']['1']) or \
                 (game_data['probabilities']['pinnacle']['open']['2'] > game_data['probabilities']['pinnacle']['final']['2'] and \
                game_data['probabilities']['pinnacle']['open']['1'] < game_data['probabilities']['pinnacle']['final']['1']):

                prediction = self.prediction_home_win
            else:
                prediction = self.disqualified

        except (TypeError, KeyError):
            a = ('exception: missing required odds')

        return prediction
