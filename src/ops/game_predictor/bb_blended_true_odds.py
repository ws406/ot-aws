import collections
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.bb_qualification_check import QualificationCheck
from src.utils.logger import OtLogger
from src.utils.true_odds_calculator import TrueOddsCalculator


# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'true_odds'
    profit_margin = 0.01 # This is to ensure we win something.

    def __init__(self, logger: OtLogger):
        self.logger = logger

    def _get_average(self, localList):
        number = 0
        for data in localList:
            number = number + data
        return number / len(localList)

    def _calc_raw_true_odds(self, data, localProfitMargin):
        picked_bookie = list()

        picked_bookie.append('pinnacle')

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
            self.logger.log('missing odds - ' + str(e))
            return is_qualifed

        home = self._get_average(local_list_home)
        away = self._get_average(local_list_away)

        true_odds_calculator = TrueOddsCalculator()

        raw_true_odds = {}
        raw_true_odds['1'], raw_true_odds['2'] = \
            true_odds_calculator.calculate_2_way_margin_prop(home, away)

        raw_true_odds['1'] = raw_true_odds['1'] * (1+localProfitMargin)
        raw_true_odds['2'] = raw_true_odds['2'] * (1+localProfitMargin)

        return raw_true_odds

    def _calc_true_odds(self, data, localProfitMargin):
        return self._calc_raw_true_odds(data, localProfitMargin)

    def get_prediction(self, data, profit_margin = None):
        # Check if game is qualified first, if not, return
        is_qualified = QualificationCheck().is_qualified(data, self.benchmark_bookie)
        if not is_qualified:
            return False
        else:
            local_profit_margin = profit_margin if profit_margin is not None else self.profit_margin
            true_odds = self._calc_true_odds(data, local_profit_margin)
            if true_odds is not False:
                return_data = dict()
                return_data['true_odds'] = true_odds
                return_data['gid'] = data ['game_id']
                return_data['league_id'] = data ['league_id']
                return_data['league_name'] = data ['league_name']
                return_data['kickoff'] = data ['kickoff']
                return_data['home_team_name'] = data ['home_team_name']
                return_data['away_team_name'] = data ['away_team_name']
                return_data['home_team_id'] = data ['home_team_id']
                return_data['away_team_id'] = data ['away_team_id']
                return_data['strategy'] = self.strategy
                return return_data
            else:
                return False
