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

        exceptions = None
        prediction = self.disqualified

        try:
            benchmark = list(collections.OrderedDict(sorted(game_data['odds'][bookie].items())).values())[-1]
            home = float(benchmark['1'])
            draw = float(benchmark['x'])
            away = float(benchmark['2'])
            returnRate = home * draw * away / (home * draw + draw * away + home * away)
            #print(game_data['game_id'], returnRate)
            if returnRate < 0.7 or returnRate > 1:
                return self.disqualified
            #if home > 5 or away> 5:
                #return self.disqualified
            prediction = self.qualified
            #print(game_data['game_id'], len(returnMap), prediction)
        except (TypeError, KeyError):
            #print("missing odds, skip...")
            None

        return prediction

    def _get_readable_kickoff_time(self, kickoff_in_linux_ts):
        return datetime.fromtimestamp(kickoff_in_linux_ts).strftime('%Y-%m-%d %H:%M:%S')