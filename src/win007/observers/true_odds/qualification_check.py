from datetime import datetime
import numpy as np
import math
import collections

class QualificationCheck:

    qualified = '1'
    disqualified = 'x'

    def __init__(self):
        pass

    def is_qualified(self, game_data, bookie):

        is_qualified = self.disqualified

        try:
            benchmark = list(collections.OrderedDict(sorted(game_data['odds'][bookie].items())).values())[-1]
            home = float(benchmark['1'])
            draw = float(benchmark['x'])
            away = float(benchmark['2'])
            returnRate = home * draw * away / (home * draw + draw * away + home * away)

            # Disqualify the game if return_rate is too low or too high
            if returnRate < 0.7 or returnRate > 1:
                return self.disqualified

            is_qualified = self.qualified
        except (TypeError, KeyError):
            print("missing odds, skip...")

        return is_qualified
