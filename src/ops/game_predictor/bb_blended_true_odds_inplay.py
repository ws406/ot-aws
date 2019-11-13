from src.ops.game_predictor.bb_blended_true_odds import TrueOdds as TrueOddsSuper
import collections
from src.utils.true_odds_calculator import TrueOddsCalculator


# This game predictor provides true odds only
class TrueOddsInplay(TrueOddsSuper):
    strategy = 'to_inplay'
    def _calc_raw_true_odds(self, data, localProfitMargin):
        picked_bookie = list()
        picked_bookie.append('pinnacle')
        picked_bookie.append('Expekt')
        picked_bookie.append('easybet')
        picked_bookie.append('SB')
        picked_bookie.append('vcbet')

        local_list_home = []
        local_list_away = []
        is_qualifed = False

        try:
            for bookie in picked_bookie:
                # {'1533924960': {'1': '1.55', '2': '7.84'}, '1533922980': {'1': '1.58', '2': '7.41'}, ...}
                latestOddsDict = collections.OrderedDict(sorted(data['odds'][bookie].items(), reverse=True))
                latestOdds = latestOddsDict[list(latestOddsDict)[0]]

                home = float(latestOdds['1'])
                away = float(latestOdds['2'])
                local_list_home.append(home)
                local_list_away.append(away)
        except Exception as e:
            self.logger.log('Exception - ' + str(e))
            return is_qualifed

        home = self._get_average(local_list_home)
        away = self._get_average(local_list_away)

        true_odds_calculator = TrueOddsCalculator()

        raw_true_odds = {}
        raw_true_odds['1'], raw_true_odds['2'] = \
            true_odds_calculator.calculate_2_way_margin_prop(home, away)

        raw_true_odds['1'] = raw_true_odds['1'] * (1+localProfitMargin)
        raw_true_odds['2'] = raw_true_odds['2'] * (1+localProfitMargin)

        compareBestOdds = [0, 0]
        true_odds = dict()
        filter_bookies = []
        filter_bookies.append('pinnacle')
        filter_bookies.append('bet365')
        filter_bookies.append('easybet')
        filter_bookies.append('5Dimes')
        for bookie in filter_bookies:
            try:
                compareOdds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
            except Exception as e:
                self.logger.log('Exception - ' + str(e))
                compareOdds = {}
                compareOdds['1'] = 1.0
                compareOdds['2'] = 1.0
            if float(compareOdds['1']) > compareBestOdds[0]:
                compareBestOdds[0] = float(compareOdds['1'])
            if float(compareOdds['2']) > compareBestOdds[1]:
                compareBestOdds[1] = float(compareOdds['2'])
        if compareBestOdds[0] >= raw_true_odds['1']:
            true_odds['1'] = raw_true_odds['1']
            is_qualifed = True
        if compareBestOdds[1] >= raw_true_odds['2']:
            true_odds['2'] = raw_true_odds['2']
            is_qualifed = True

        if is_qualifed:
            return true_odds
        else:
            return False
