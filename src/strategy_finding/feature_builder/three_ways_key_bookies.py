from src.strategy_finding.feature_builder.interface import FeatureBuilderInterface
import numpy as np
from src.utils.sort_dict_by_key import SortDictByKey
from src.utils.logger import OtLogger

# Selected bookies: MS, Bet365, WH, PIN
# Features are:
# 4 The opening probabilities for home_win from 4 bookies
# 4 The opening probabilities for draw from 4 bookies
# 4 The opening probabilities for away_win from 4 bookies
# 4 The delta probabilities for home_win from 4 bookies
# 4 The delta probabilities for draw from 4 bookies
# 4 The delta probabilities for away_win from 4 bookies
# 3 The betting odds (for calculating results): PIN final odds


class ThreeWaysKeyBookies(FeatureBuilderInterface):

    bookie_names = [
        'macau_slot',
        'bet365',
        'will_hill',
        'pinnacle'
    ]

    def __init__(self, logger: OtLogger):
        super().__int__(logger)

    def get_header(self):
        # Add headers for each 'labelled' results
        header = [
            'home_win',
            'home_win_or_draw',
            'away_win',
            'away_win_or_draw',
            'draw',
            'no_bet'
        ]

        # add header for each feature
        for bname in self.bookie_names:
            header.append('open_prob_home_win_' + bname)
            header.append('delta_prob_home_win_' + bname)
            header.append('open_prob_draw_' + bname)
            header.append('delta_prob_draw_' + bname)
            header.append('open_prob_away_win_' + bname)
            header.append('delta_prob_away_win_' + bname)

        return header

    def get_num_cols(self):
        return 6 + 6*len(self.bookie_names)

    def get_features(self, raw_data: dict):
        print("Running feature builder - 1x2_probabilities with " + str(len(raw_data)) + " games")

        # Calculate the number of cols and set up feature matrix
        col_num = self.get_num_cols()
        featured_data = np.empty((0, col_num))

        skip = False
        # Go through each data entry and add features
        for data in raw_data:
            # Label results
            if data['home_score'] > data['away_score']:
                row = [1, 1, 0, 0, 0, 0]
            elif data['home_score'] == data['away_score']:
                row = [0, 1, 0, 1, 1, 0]
            else:
                row = [0, 0, 1, 1, 0, 0]

            for bname in self.bookie_names:
                try:
                    probs = data['probabilities'][bname]
                except KeyError:
                    self.logger.debug('XXX game ' + str(data['game_id']) + ' does not have data for bookie ' + bname)
                    skip = True
                    break

                sorted_probs = SortDictByKey.sort(probs)

                home_win_original_prob = sorted_probs[0][1]['1'] * 100
                home_win_final_prob = sorted_probs[-1][1]['1'] * 100
                draw_original_prob = sorted_probs[0][1]['x'] * 100
                draw_final_prob = sorted_probs[-1][1]['x'] * 100
                away_win_original_prob = sorted_probs[0][1]['2'] * 100
                away_win_final_prob = sorted_probs[-1][1]['2'] * 100
                row.append(home_win_original_prob)
                row.append(home_win_final_prob - home_win_original_prob)
                row.append(draw_original_prob)
                row.append(draw_final_prob - draw_original_prob)
                row.append(away_win_original_prob)
                row.append(away_win_final_prob - away_win_original_prob)

            if skip:
                skip = False
                continue

            featured_data = np.append(featured_data, [row], axis=0)

        return featured_data
