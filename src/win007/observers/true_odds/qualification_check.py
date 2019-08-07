from datetime import datetime
import numpy as np
import math
import collections

class QualificationCheck:

    def __init__(self):
        pass

    def is_qualified(self, game_data, bookie):

        is_qualified = False

        try:
            benchmark = list(collections.OrderedDict(sorted(game_data['odds'][bookie].items())).values())[-1]
            home = float(benchmark['1'])
            draw = float(benchmark['x'])
            away = float(benchmark['2'])
            returnRate = home * draw * away / (home * draw + draw * away + home * away)

            #print(returnRate)

            # Disqualify the game if return_rate is too low or too high
            if returnRate >= 0.9 and returnRate <= 1:
                is_qualified = True
        except (TypeError, KeyError):
            #print("missing odds, skip...")
            None

        return is_qualified
