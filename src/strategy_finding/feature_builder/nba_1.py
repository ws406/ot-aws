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

        header = [
            'result',
            'init_prob_pinnacle_home',
            'init_prob_pinnacle_away',
            'delta_prob_pin_lad_home',
            'delta_prob_pin_lad_away'
        ]

        featured_data = np.empty((0, 8))

        for data in labelled_data:

            if 'pinnacle' not in data['probabilities'] or 'ladbroke' not in data['probabilities']:
                # self.logger.exception(str(data['game_id']) + ' can not be processed due to lack of prob data')
                continue

            best_probs = list (collections.OrderedDict (sorted (data ['probabilities'] ['pinnacle'].items ())).items ())
            worst_probs = list (collections.OrderedDict (sorted (data ['probabilities']['ladbroke'].items ())).items ())

            benchmark_odds = list (collections.OrderedDict (sorted (data ['odds'] ['ladbroke'].items ())).items ())

            row = [
                data['result'],
                data['game_id'],
                benchmark_odds[-1][1]['1'],
                benchmark_odds[-1][1]['2'],
                best_probs[-1][1]['1'],
                best_probs[-1][1]['2'],
                best_probs[-1][1]['1'] - worst_probs[-1][1]['1'],
                best_probs[-1][1]['2'] - worst_probs[-1][1]['2'],
            ]
            featured_data = np.append(featured_data, [row], axis=0)

        return header, featured_data