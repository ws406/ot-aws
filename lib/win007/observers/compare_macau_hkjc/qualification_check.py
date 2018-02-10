import numpy as np
from datetime import datetime

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
        benmark = 500.0

        try:
            #1. Look at the comparison between HKJC and Macau
            if np.log(game_data['probabilities']['hkjc']['open']['2'] / game_data['probabilities']['macau_slot']['open']['2']) * 10000.0 >= benmark\
                and np.log(game_data['probabilities']['macau_slot']['open']['1'] / game_data['probabilities']['hkjc']['open']['1']) * 10000.0 >= benmark:
                odds_comparison_check = self.odds_comparison_check_away_ok

            elif np.log(game_data['probabilities']['hkjc']['open']['1'] / game_data['probabilities']['macau_slot']['open']['1']) * 10000.0 >= benmark\
                and np.log(game_data['probabilities']['macau_slot']['open']['2'] / game_data['probabilities']['hkjc']['open']['2']) * 10000.0 >= benmark:
                odds_comparison_check = self.odds_comparison_check_home_ok

            #odds_comparison2_check = self.odds_comparison_check_disqualified
            #if game_data['probabilities']['interwetten']['open']['1'] > game_data['probabilities']['will_hill']['open']['1'] and \
                #game_data['probabilities']['interwetten']['open']['2'] < game_data['probabilities']['will_hill']['open']['2']:

                #odds_comparison2_check = self.odds_comparison_check_home_ok

            #elif game_data['probabilities']['interwetten']['open']['1'] < game_data['probabilities']['will_hill']['open']['1'] and \
                #game_data['probabilities']['interwetten']['open']['2'] > game_data['probabilities']['will_hill']['open']['2']:

                #odds_comparison2_check = self.odds_comparison_check_away_ok

            ##if odds_comparison_check == self.odds_comparison_check_disqualified and odds_comparison2_check != self.odds_comparison_check_disqualified:
               ##odds_comparison_check = odds_comparison2_check
            ##elif odds_comparison_check == self.odds_comparison_check_away_ok and odds_comparison2_check == self.odds_comparison_check_home_ok:
               ##odds_comparison_check = self.odds_comparison_check_disqualified
            ##elif odds_comparison_check == self.odds_comparison_check_home_ok and odds_comparison2_check == self.odds_comparison_check_away_ok:
               ##odds_comparison_check = self.odds_comparison_check_disqualified

            #if odds_comparison_check != odds_comparison2_check:
               #odds_comparison_check = self.odds_comparison_check_disqualified

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

                prediction = self.prediction_away_win + ' (' + \
                             self._get_readable_kickoff_time(game_data['kickoff']) + ')'

            elif odds_comparison_check == self.odds_comparison_check_home_ok and \
                game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2'] and \
                game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
                game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2'] and \
                game_data['odds']['pinnacle']['open']['1'] > game_data['odds']['pinnacle']['final']['1'] and \
                game_data['odds']['pinnacle']['open']['2'] < game_data['odds']['pinnacle']['final']['2']:

                prediction = self.prediction_home_win + ' (' + \
                             self._get_readable_kickoff_time(game_data['kickoff']) + ')'

        except (TypeError, KeyError):
            exceptions = 'missing required odds'

        if odds_comparison_check != self.odds_comparison_check_disqualified:
            prediction += ' - ' + odds_comparison_check
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
