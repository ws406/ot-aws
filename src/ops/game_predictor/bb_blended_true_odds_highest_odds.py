from src.ops.game_predictor.fb_blended_true_odds import TrueOdds as TrueOddsSuper


# This game predictor provides true odds only
class TrueOddsHighest(TrueOddsSuper):

    def _calc_true_odds(self, data, localProfitMargin):

        true_odds = self._calc_raw_true_odds(data, localProfitMargin)
        if true_odds is not False:
            # only return lower two odds
            true_odds.pop(min(true_odds, key=true_odds.get))
        return true_odds
