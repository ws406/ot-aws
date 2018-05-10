from datetime import datetime

def find_open_final(data):
    timeList = []
    probOpenTime = 9999999999
    probFinalTime = 0
    for key, value in data.items():
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

    #prediction_home_win = 'home-win'
    #prediction_away_win = 'away-win'
    #disqualified = 'disqualified'
    prediction_home_win = '1'
    prediction_away_win = '2'
    disqualified = 'disqualified'

    condition_open_odds_ok_home = '*** home-team-open-odds-qualify ***'
    condition_open_odds_ok_away = '*** away-team-open-odds-qualify ***'
    condition_open_odds_disqualify = 'open-odds-disqualify'

    def __init__(self):
        pass

    def is_qualified(self, game_data):

        open_odds_condition = self.condition_open_odds_disqualify
        prediction = self.disqualified
        exceptions = None
        benchmark = 1.92
        benchmark2 = 2

        try:
            test = game_data['odds']['macau_slot']
            test = game_data['odds']['will_hill']
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
            # 1. check ranking condition: to qualify, the team that ranks lower needs to have winning odds that is lower than 1.9
            # Away team ranks lower or only one position higher than home team. E.g. home ranks 3, away ranks 2 or 4 or lower.
            if (game_data['away_team_rank'] - game_data['home_team_rank'] > -1) and \
                            game_data['odds']['macau_slot']['open']['2'] <= benchmark and \
                            game_data['odds']['will_hill']['open']['2'] <= benchmark2:
                open_odds_condition = self.condition_open_odds_ok_away

            # Home team ranks lower or only one position higher than away team. E.g. away ranks 3, home ranks 2 or 4 or lower.
            elif (game_data['home_team_rank'] - game_data['away_team_rank'] > -1 ) and \
                            game_data['odds']['macau_slot']['open']['1'] <= benchmark and \
                            game_data['odds']['will_hill']['open']['1'] <= benchmark2:
                open_odds_condition = self.condition_open_odds_ok_home

            # 2. Predict by odds trend. If all-final-odds is smaller than all-original-odds, predict that result.
            if open_odds_condition == self.condition_open_odds_ok_away and \
                game_data['odds']['macau_slot']['open']['1'] < game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] > game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] < game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] > game_data['odds']['will_hill']['final']['2']:
                #game_data['odds']['bet365']['open']['1'] < game_data['odds']['bet365']['final']['1'] and \
                #game_data['odds']['bet365']['open']['2'] > game_data['odds']['bet365']['final']['2'] and \
                #game_data['odds']['pinnacle']['open']['1'] < game_data['odds']['pinnacle']['final']['1'] and \
                    #game_data['odds']['pinnacle']['open']['2'] > game_data['odds']['pinnacle']['final']['2']:

                #prediction = self.prediction_away_win + ' (' + \
                             #self._get_readable_kickoff_time(game_data['kickoff']) + ')'
                prediction = self.prediction_away_win

            elif open_odds_condition == self.condition_open_odds_ok_home  and \
                game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2']:
                #game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
                #game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2'] and \
                #game_data['odds']['pinnacle']['open']['1'] > game_data['odds']['pinnacle']['final']['1'] and \
                    #game_data['odds']['pinnacle']['open']['2'] < game_data['odds']['pinnacle']['final']['2']:

                #prediction = self.prediction_home_win + ' (' + \
                             #self._get_readable_kickoff_time(game_data['kickoff']) + ')'
                prediction = self.prediction_home_win


        except (TypeError, KeyError):
            exceptions = 'missing required odds'

        #if open_odds_condition != self.condition_open_odds_disqualify:
            #prediction += ' - ' + open_odds_condition

        if exceptions is not None:
            prediction += ' - ' + exceptions

        return prediction

    def _get_readable_kickoff_time(self, kickoff_in_linux_ts):
        return datetime.fromtimestamp(kickoff_in_linux_ts).strftime('%Y-%m-%d %H:%M:%S')
      
#class QualificationCheck:

    #prediction_home_win = 'home-win'
    #prediction_away_win = 'away-win'
    #disqualified = 'disqualified'

    #odds_comparison_check_home_ok = '*** home-odds-comparison-check-ok ***'
    #odds_comparison_check_away_ok = '*** away-odds-comparison-check-ok ***'
    #odds_comparison_check_disqualified = 'odds-comparison-disqualified'

    #def __init__(self):
        #pass

    #def is_qualified(self, game_data):

        #odds_comparison_check = self.odds_comparison_check_disqualified
        #exceptions = None
        #prediction = self.disqualified

        #try:
            #if game_data['odds']['macau_slot']['open']['1'] < game_data['odds']['macau_slot']['final']['1'] and \
                #game_data['odds']['macau_slot']['open']['2'] > game_data['odds']['macau_slot']['final']['2'] and \
                #game_data['odds']['will_hill']['open']['1'] < game_data['odds']['will_hill']['final']['1'] and \
                #game_data['odds']['will_hill']['open']['2'] > game_data['odds']['will_hill']['final']['2'] and \
                #game_data['odds']['bet365']['open']['1'] < game_data['odds']['bet365']['final']['1'] and \
                #game_data['odds']['bet365']['open']['2'] > game_data['odds']['bet365']['final']['2'] and \
                #game_data['odds']['pinnacle']['open']['1'] < game_data['odds']['pinnacle']['final']['1'] and \
                #game_data['odds']['pinnacle']['open']['2'] > game_data['odds']['pinnacle']['final']['2']:

                #prediction = self.prediction_away_win + ' (' + \
                             #self._get_readable_kickoff_time(game_data['kickoff']) + ')'

            #elif game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
                #game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
                #game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
                #game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2'] and \
                #game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
                #game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2'] and \
                #game_data['odds']['pinnacle']['open']['1'] > game_data['odds']['pinnacle']['final']['1'] and \
                #game_data['odds']['pinnacle']['open']['2'] < game_data['odds']['pinnacle']['final']['2']:

                #prediction = self.prediction_home_win + ' (' + \
                             #self._get_readable_kickoff_time(game_data['kickoff']) + ')'

        #except (TypeError, KeyError):
            #exceptions = 'missing required odds'

        #return prediction

    #def _get_readable_kickoff_time(self, kickoff_in_linux_ts):
        #return datetime.fromtimestamp(kickoff_in_linux_ts).strftime('%Y-%m-%d %H:%M:%S')
