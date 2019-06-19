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
        empty = np.empty((0, 8))
        featured_data = {
            '2014-2015': empty,
            '2015-2016': empty,
            '2016-2017': empty,
            '2017-2018': empty,
            '2018-2019': empty,
        }

        for data in labelled_data:
            # Home win - odds between 1.3 and 1.7
            if 'betvictor' not in data['probabilities'] or 'matchbook' not in data ['probabilities'] \
                    or 'Betfair' not in data ['probabilities']:
                self.logger.exception(str(data['game_id']) + ' can not be processed due to lack of prob data')
                continue
            best_final_probs_1 = list (collections.OrderedDict (sorted (data ['probabilities'] ['matchbook'].items ())).items ())
            worst_final_probs_1 = list (collections.OrderedDict (sorted (data ['probabilities']['betvictor'].items ())).items ())
            best_delta_probs = list (collections.OrderedDict (sorted (data ['probabilities']['Betfair'].items ())).items ())
            # benchmark_odds = list (collections.OrderedDict (sorted (data ['odds'] ['matchbook'].items ())).items ())
            benchmark_probs_1 = best_final_probs_1 [-1] [1] ['1']
            benchmark_probs_3 = worst_final_probs_1 [-1] [1] ['1']
            if float (benchmark_probs_1 - benchmark_probs_3) < 0.005 or \
                    float (benchmark_probs_3) > 1/1.3 or float (benchmark_probs_3) < 1/1.7 :
                continue

            # Away win - odds between 1.3 and 1.7
            # if 'vcbet' not in data ['probabilities'] or 'bet365' not in data ['probabilities'] :
            #     self.logger.exception(str(data['game_id']) + ' can not be processed due to lack of prob data')
            #     continue
            # best_final_probs_1 = list (
            #     collections.OrderedDict (sorted (data ['probabilities'] ['bet365'].items ())).items ())
            # worst_final_probs_1 = list (
            #     collections.OrderedDict (sorted (data ['probabilities'] ['vcbet'].items ())).items ())
            # benchmark_odds = list (collections.OrderedDict (sorted (data ['odds'] ['bet365'].items ())).items ())
            # benchmark_probs_1 = best_final_probs_1 [-1] [1] ['2']
            # benchmark_probs_3 = worst_final_probs_1 [-1] [1] ['2']
            # if float (benchmark_probs_1 - benchmark_probs_3) < 0.002 or \
            #         float (benchmark_probs_3) > 1 / 1.3 or float (benchmark_probs_1) < 1 / 1.7:
            #     continue

            row = [
                data['result'],
                data['game_id'],
                best_final_probs_1[-1][1]['1'],
                best_final_probs_1[-1][1]['2'],
                # best_avg_final_prob_for_1,
                # best_avg_final_prob_for_2,
                # best_initial_probs[0] [1] ['1'],
                # best_initial_probs[0] [1] ['2'],
                best_final_probs_1 [-1] [1] ['1'],
                best_final_probs_1 [-1] [1] ['2'],
                best_final_probs_1 [-1] [1] ['1'] - worst_final_probs_1 [-1] [1] ['1'],
                best_final_probs_1 [-1] [1] ['2'] - worst_final_probs_1 [-1] [1] ['2'],
                # best_delta_probs[-1][1]['1']-best_delta_probs[0][1]['1'],
                # best_initial_probs[-1][1]['1'] - worst_initial_probs[-1][1]['1'],
                # best_initial_probs[-1][1]['2'] - worst_initial_probs[-1][1]['2'],
                # best_avg_final_prob_for_1 - worst_avg_final_prob_for_1,
                # best_avg_final_prob_for_2 - worst_avg_final_prob_for_2
            ]
            featured_data[data['season']] = np.append(featured_data[data['season']], [row], axis=0)

        return header, featured_data