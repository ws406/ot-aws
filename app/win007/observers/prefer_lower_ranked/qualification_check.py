import json
from collections import defaultdict

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

    def __init__(self):
        pass

    def is_qualified(self, game_data):

        prediction = None

        # 1. check ranking condition: to qualify, the team that ranks lower needs to have winning odds that is lower than 1.9
        # Away team ranks lower or only one position higher than home team. E.g. home ranks 3, away ranks 2 or 4 or lower.
        if (game_data['away_team_rank'] - game_data['home_team_rank'] > -1) and \
                        game_data['odds']['macau_slot']['open']['2'] < 1.9 :
            prediction = self.prediction_away_win

        # Home team ranks lower or only one position higher than away team. E.g. away ranks 3, home ranks 2 or 4 or lower.
        elif (game_data['home_team_rank'] - game_data['away_team_rank'] > -1 ) and \
                        game_data['odds']['macau_slot']['open']['1'] < 1.9 :
            prediction = self.prediction_home_win


        # 2. Predict by odds trend. If all-final-odds is smaller than all-original-odds, predict that result.
        if prediction == self.prediction_away_win and \
            game_data['odds']['macau_slot']['open']['1'] < game_data['odds']['macau_slot']['final']['1'] and \
            game_data['odds']['macau_slot']['open']['2'] > game_data['odds']['macau_slot']['final']['2'] and \
            game_data['odds']['will_hill']['open']['1'] < game_data['odds']['will_hill']['final']['1'] and \
            game_data['odds']['will_hill']['open']['2'] > game_data['odds']['will_hill']['final']['2'] and \
            game_data['odds']['bet365']['open']['1'] < game_data['odds']['bet365']['final']['1'] and \
            game_data['odds']['bet365']['open']['2'] > game_data['odds']['bet365']['final']['2'] and \
            game_data['odds']['pinnacle']['open']['1'] < game_data['odds']['pinnacle']['final']['1'] and \
                game_data['odds']['pinnacle']['open']['2'] > game_data['odds']['pinnacle']['final']['2']:

            prediction = prediction

        elif prediction == 1 and \
            game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
            game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
            game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
            game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2'] and \
            game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
            game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2'] and \
            game_data['odds']['pinnacle']['open']['1'] > game_data['odds']['pinnacle']['final']['1'] and \
                game_data['odds']['pinnacle']['open']['2'] < game_data['odds']['pinnacle']['final']['2']:

            prediction = prediction

        else:
            prediction = self.disqualified

        return prediction
