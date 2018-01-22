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

    odds_comparison_check_home_ok = '*** home-odds-comparison-check-ok ***'
    odds_comparison_check_away_ok = '*** away-odds-comparison-check-ok ***'
    odds_comparison_check_disqualified = 'odds-comparison-disqualified'

    def __init__(self):
        pass

    def is_qualified(self, game_data):

        odds_comparison_check = self.odds_comparison_check_disqualified
        exceptions = None
        prediction = self.disqualified

        try:
            # 1. Look at the comparison between HKJC and Macau
            if np.log(game_data['probabilities']['hkjc']['open']['2'] / game_data['probabilities']['macau_slot']['open'][
                        '2']) * 10000.0 >= 500.0:
                odds_comparison_check = self.odds_comparison_check_away_ok

            elif np.log(game_data['probabilities']['hkjc']['open']['1'] / game_data['probabilities']['macau_slot']['open'][
                        '1']) * 10000.0 >= 500.0:
                odds_comparison_check = self.odds_comparison_check_home_ok

            # 2. Predict by odds trend. If all-final-odds is smaller than all-original-odds, predict that result.
            if odds_comparison_check == self.odds_comparison_check_away_ok and \
                game_data['odds']['macau_slot']['open']['1'] < game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] > game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] < game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] > game_data['odds']['will_hill']['final']['2'] and \
                game_data['odds']['bet365']['open']['1'] < game_data['odds']['bet365']['final']['1'] and \
                game_data['odds']['bet365']['open']['2'] > game_data['odds']['bet365']['final']['2'] and \
                game_data['odds']['pinnacle']['open']['1'] < game_data['odds']['pinnacle']['final']['1'] and \
                game_data['odds']['pinnacle']['open']['2'] > game_data['odds']['pinnacle']['final']['2']:

                prediction = self.prediction_away_win

            elif odds_comparison_check == self.odds_comparison_check_home_ok and \
                game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2'] and \
                game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
                game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2'] and \
                game_data['odds']['pinnacle']['open']['1'] > game_data['odds']['pinnacle']['final']['1'] and \
                game_data['odds']['pinnacle']['open']['2'] < game_data['odds']['pinnacle']['final']['2']:

                prediction = self.prediction_home_win

        except (TypeError, KeyError):
            exceptions = 'missing required odds'

        if odds_comparison_check != self.odds_comparison_check_disqualified:
            prediction += ' - ' + odds_comparison_check
        if exceptions is not None:
            prediction += ' - ' + exceptions

        return prediction
