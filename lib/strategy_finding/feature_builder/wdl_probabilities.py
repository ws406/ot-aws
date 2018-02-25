from lib.strategy_finding.feature_builder.interface import FeatureBuilderInterface
import numpy as np

# Features are:
#  4: the opening probabilities for the predicted result from 4 bookies: MS, Bet365, WH, PIN
#  4: the delta probabilities for the predicted result from 4 bookies: MS, Bet365, WH, PIN
#  1: home or away
class WDLProbabilitiesFeatureBuilder(FeatureBuilderInterface):

    def get_features(self, labelled_data: dict):
        print("Running feature builder - 1x2_probabilities with " + str(len(labelled_data)) + " games")

        header = [
            'label',
            'h_or_a',
            'open_prob_ms',
            'open_prob_365',
            'open_prob_wh',
            'open_prob_pin',
            'delta_prob_ms',
            'delta_prob_365',
            'delta_prob_wh',
            'delta_prob_pin'
        ]

        featured_data = np.empty((0, 10))

        for data in labelled_data:
            h_or_a = str(data['prediction'])

            row = [
                data['result'],
                h_or_a,
                data['probabilities']['macau_slot']['open'][h_or_a],
                data['probabilities']['bet365']['open'][h_or_a],
                data['probabilities']['will_hill']['open'][h_or_a],
                data['probabilities']['pinnacle']['open'][h_or_a],
                data['probabilities']['macau_slot']['final'][h_or_a] - data['probabilities']['macau_slot']['open'][h_or_a],
                data['probabilities']['bet365']['final'][h_or_a] - data['probabilities']['bet365']['open'][h_or_a],
                data['probabilities']['will_hill']['final'][h_or_a] - data['probabilities']['will_hill']['open'][h_or_a],
                data['probabilities']['pinnacle']['final'][h_or_a] - data['probabilities']['pinnacle']['open'][h_or_a]
            ]
            featured_data = np.append(featured_data, [row], axis=0)

        return header, featured_data
