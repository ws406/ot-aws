# This file builds the following features - the idea came from the bookie ranking results from nba_bookie_ranking.py
#  - final_pinnacle_bet_home
#  - delta_pinnacle_bet_away
#  - final_pinnacle_bet_home - final_ladbrokes_home
#  - final_pinnacle_bet_away - final_ladbrokes_away

from src.strategy_finding.feature_builder.interface import FeatureBuilderInterface
import numpy as np
from src.utils.logger import OtLogger
import collections


class NBA1(FeatureBuilderInterface):

    def __init__(self, logger: OtLogger):
        super().__int__(logger)

    def get_features(self, labelled_data: dict):
        self.logger.debug("Running feature builder - NBA1")

        # TODO: this needs to be updated
        header = [
            'result',
            'game_id'
            'final_odds_ladbroke_1',
            'final_odds_ladbroke_2',
            'init_prob_pinnacle_home',
            'init_prob_pinnacle_away',
            'delta_prob_pin_lad_home',
            'delta_prob_pin_lad_away'
        ]
        empty = np.empty((0, 10))
        featured_data = {
            '2015-2016': empty,
            '2016-2017': empty,
            '2017-2018': empty,
            '2018-2019': empty,
        }

        for data in labelled_data:

            if 'Betfair' not in data ['probabilities'] or 'SB' not in data['probabilities'] or\
                'will_hill' not in data ['probabilities'] or 'SNAI' not in data ['probabilities'] or \
                    '5Dimes' not in data ['probabilities'] or 'betvictor' not in data ['probabilities']:
                self.logger.exception(str(data['game_id']) + ' can not be processed due to lack of prob data')
                continue

            best_final_probs_1 = list (collections.OrderedDict (sorted (data ['probabilities'] ['Betfair'].items ())).items ())
            best_final_probs_2 = list (collections.OrderedDict (sorted (data ['probabilities'] ['will_hill'].items ())).items ())
            best_final_probs_3 = list (collections.OrderedDict (sorted (data ['probabilities'] ['5Dimes'].items ())).items ())
            # best_initial_probs = list (collections.OrderedDict (sorted (data ['probabilities'] ['will_hill'].items ())).items ())
            # worst_initial_probs = list (collections.OrderedDict (sorted (data ['probabilities']['ladbroke'].items ())).items ())
            worst_final_probs_1 = list (collections.OrderedDict (sorted (data ['probabilities']['SB'].items ())).items ())
            worst_final_probs_2 = list (collections.OrderedDict (sorted (data ['probabilities']['SNAI'].items ())).items ())
            worst_final_probs_3 = list (collections.OrderedDict (sorted (data ['probabilities']['betvictor'].items ())).items ())
            best_delta_probs = best_final_probs_1
            worst_delta_probs = worst_final_probs_1

            benchmark_odds = list (collections.OrderedDict (sorted (data ['odds'] ['Betfair'].items ())).items ())

            # if float(benchmark_odds[-1][1]['1']) < 1.67 or float(benchmark_odds[-1][1]['2']) < 1.67:
            benchmark_probs_1 = best_final_probs_1 [-1] [1] ['1']
            benchmark_probs_2 = best_final_probs_1 [-1] [1] ['2']
            if float (benchmark_probs_1) > 0.67 or float (benchmark_probs_2) > 0.67\
                    or float (benchmark_probs_1) < 0.33 or float (benchmark_probs_2) < 0.33:
                continue

            best_avg_final_prob_for_1 = (best_final_probs_1[-1][1]['1'] + best_final_probs_2[-1][1]['1']) /2

            best_avg_final_prob_for_2 = (best_final_probs_1 [-1] [1] ['2'] + best_final_probs_2 [-1] [1] ['2']) / 2

            worst_avg_final_prob_for_1 = (worst_final_probs_1[-1][1]['1'] + worst_final_probs_2[-1][1]['1'] )/2

            worst_avg_final_prob_for_2 = (worst_final_probs_1 [-1] [1] ['2'] + worst_final_probs_2 [-1] [1] ['2'] ) / 2

            row = [
                data['result'],
                data['game_id'],
                benchmark_odds[-1][1]['1'],
                benchmark_odds[-1][1]['2'],
                best_avg_final_prob_for_1,
                best_avg_final_prob_for_2,
                # best_initial_probs[0] [1] ['1'],
                # best_initial_probs[0] [1] ['2'],
                best_delta_probs[-1][1]['1']-worst_delta_probs[0][1]['1'],
                best_delta_probs[-1][1]['2']-worst_delta_probs[0][1]['2'],
                # best_initial_probs[-1][1]['1'] - worst_initial_probs[-1][1]['1'],
                # best_initial_probs[-1][1]['2'] - worst_initial_probs[-1][1]['2'],
                best_avg_final_prob_for_1 - worst_avg_final_prob_for_1,
                best_avg_final_prob_for_2 - worst_avg_final_prob_for_2
            ]
            featured_data[data['season']] = np.append(featured_data[data['season']], [row], axis=0)

        return header, featured_data