import json
from collections import defaultdict
import numpy as np

'''
    # This function takes the input data and makes a decision about whether this game is
    # qualified or not based on our strategy.
    #
    # The input data structure is illustrated in data_example.json file
    # The return is one of the three possibilities:
    # 1. None: nothing is qualified
    # 2. "1": home team is preferred
    # 3. "2": awa team is preferred
    def which_is_qualified(self, odds: GameMainBookiesOdds):
        odds['odds']['bookie_name']

        pass
'''


class QualificationCheck:

    prediction_home_win = 'home-win'
    prediction_away_win = 'away-win'
    disqualified = 'disqualified'

    condition_open_odds_ok_home = 'home-team-open-odds-qualify'
    condition_open_odds_ok_away = 'away-team-open-odds-qualify'
    condition_open_odds_disqualify = 'open-odds-disqualify'

    def __init__(self):
        pass

    def is_qualified(self, game_data):

        prediction = None
        open_odds_condition = None

        # 1. Predict by odds trend. If all-final-odds is smaller than all-original-odds, predict that result.
        if game_data['odds']['macau_slot']['open']['1'] < game_data['odds']['macau_slot']['final']['1'] and \
            game_data['odds']['macau_slot']['open']['2'] > game_data['odds']['macau_slot']['final']['2'] and \
            game_data['odds']['will_hill']['open']['1'] < game_data['odds']['will_hill']['final']['1'] and \
            game_data['odds']['will_hill']['open']['2'] > game_data['odds']['will_hill']['final']['2'] and \
            game_data['odds']['bet365']['open']['1'] < game_data['odds']['bet365']['final']['1'] and \
            game_data['odds']['bet365']['open']['2'] > game_data['odds']['bet365']['final']['2'] and \
            game_data['odds']['pinnacle']['open']['1'] < game_data['odds']['pinnacle']['final']['1'] and \
                game_data['odds']['pinnacle']['open']['2'] > game_data['odds']['pinnacle']['final']['2']:

            prediction = self.prediction_away_win

        elif game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
            game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
            game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
            game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2'] and \
            game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
            game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2'] and \
            game_data['odds']['pinnacle']['open']['1'] > game_data['odds']['pinnacle']['final']['1'] and \
                game_data['odds']['pinnacle']['open']['2'] < game_data['odds']['pinnacle']['final']['2']:

            prediction = self.prediction_home_win

        else:
            prediction = self.disqualified

        # 2. Look at the comparison between HKJC and Macau
        if prediction == self.prediction_away_win and np.log(game_data['probability']['HKJC']['open']['2'] / game_data['probability']['macau_slot']['open']['2']) * 10000.0 >= 500.0:
            open_odds_condition = self.prediction_away_win

        elif prediction == self.prediction_home_win and np.log(game_data['probability']['HKJC']['open']['1'] / game_data['probability']['macau_slot']['open']['1']) * 10000.0 >= 500.0:
            open_odds_condition = self.prediction_home_win

        else:
            prediction = self.disqualified
        
        return prediction
