import collections
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.fb_qualification_check import QualificationCheck
from src.utils.logger import OtLogger
from src.utils.true_odds_calculator import TrueOddsCalculator
import joblib
import math

# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'true_odds'
    profit_margin = 0.05 # This is to ensure we win something.
    special_leagues_1 = []
    special_leagues_2 = []

    def __init__(self, logger: OtLogger):
        self.logger = logger
        self.rf = joblib.load("./football_model.sav")
        self.special_leagues_1.append(3)
        self.special_leagues_1.append(6)
        self.special_leagues_1.append(8)
        self.special_leagues_1.append(10)
        self.special_leagues_1.append(11)
        self.special_leagues_1.append(13)
        self.special_leagues_1.append(16)
        self.special_leagues_1.append(17)
        self.special_leagues_1.append(29)
        self.special_leagues_1.append(30)
        self.special_leagues_1.append(31)
        self.special_leagues_1.append(33)
        self.special_leagues_1.append(37)

        self.special_leagues_2.append(34)
        self.special_leagues_2.append(25)
        self.special_leagues_2.append(284)
        self.special_leagues_2.append(60)
        self.special_leagues_2.append(133)
        self.special_leagues_2.append(23)
        self.special_leagues_2.append(27)
        self.special_leagues_2.append(26)
        self.special_leagues_2.append(21)
        self.special_leagues_2.append(7)

    def _get_average(self, localList):
        number = 0
        for data in localList:
            number = number + data
        return number / len(localList)

    def _find_odds_with_offset(self, game_data, bookie, lookbackTime, lookbackCheck, backTime = 12.0):
        kickoffTime = int(game_data['kickoff'])
        if lookbackCheck:
            lastUpdateTime = int(list(collections.OrderedDict(sorted(game_data['odds'][bookie].items())).keys())[-1])
            if lastUpdateTime < kickoffTime - backTime * 60 * 60:
                return None
        matchInSeq = collections.OrderedDict(sorted(game_data['odds'][bookie].items()))
        lastRecord = []
        lastRecord.append(0)
        lastRecord.append(0)
        for timeStr, prob in matchInSeq.items():
            time = int(float(timeStr))
            if timeStr == "final" or timeStr == "open" or time > kickoffTime:
                continue
            if time <= kickoffTime - lookbackTime:
                if time > lastRecord[0]:
                    lastRecord[0] = time
            if time <= kickoffTime:
                if time > lastRecord[1]:
                    lastRecord[1] = time
        if lastRecord[1] != 0:
            game_data['odds'][bookie][int(game_data['kickoff'])] = game_data['odds'][bookie][int(lastRecord[1])]
        if lastRecord[0] != 0:
            return game_data['odds'][bookie][int(lastRecord[0])]
        else:
            return None

    def _calc_prob(self, picked_bookie, data, lookbackTime):
        local_list_home = []
        local_list_draw = []
        local_list_away = []
        for bookie in picked_bookie:
            latestOdds = self._find_odds_with_offset(data, bookie, lookbackTime, False)
            home = float(latestOdds['1'])
            draw = float(latestOdds['x'])
            away = float(latestOdds['2'])
            local_list_home.append(home)
            local_list_draw.append(draw)
            local_list_away.append(away)
        home = self._get_average(local_list_home)
        draw = self._get_average(local_list_draw)
        away = self._get_average(local_list_away)

        true_odds_calculator = TrueOddsCalculator()

        raw_true_odds = {}
        raw_true_odds['1'], raw_true_odds['2'], raw_true_odds['x'] = \
            true_odds_calculator.calculate_3_way_margin_prop(home, away, draw)
        self.logger.log(str(local_list_home) + ',' + str(local_list_draw) + ',' + str(local_list_away) + ',' + str(home) + ',' + str(draw) + ',' + str(away) + ',' + str(raw_true_odds) + ',' + str(1 / raw_true_odds['1']))
        return 1 / raw_true_odds['1']

    def _calc_raw_true_odds(self, data, localProfitMargin):
        picked_bookie = list()
        vec = []
        is_qualifed = False

        try:
            picked_bookie.append('pinnacle')
            feature1 = self._calc_prob(picked_bookie, data, 0)
            picked_bookie.append('bet365')
            picked_bookie.append('betvictor')
            picked_bookie.append('ladbroke')
            #feature2 = self._calc_prob(picked_bookie, data, 0)

            localVec = []
            if feature1 > 0:
                localVec.append(feature1)
        except Exception as e:
            self.logger.log('missing odds - ' + str(e))
            return is_qualifed

        vec.append(localVec)
        probability = self.rf.predict_proba(vec)
        home_win_odds = 1 / probability[0,1]
        home_not_win_odds = 1 / probability[0,0]
        if data['league_id'] in self.special_leagues_2:
            localProfitMargin = 0.03
        hw_odds = home_win_odds * (1+localProfitMargin)
        hnw_odds = home_not_win_odds * (1+localProfitMargin)
        self.logger.log('Key data,' + str(probability) + ',' + str(home_win_odds) + ',' + str(home_not_win_odds) + ',' + str(hw_odds) + ',' + str(hnw_odds) + ',' + str(localProfitMargin))
        true_odds = {}
        if data['league_id'] in self.special_leagues_1:
            if hw_odds <= 6 and hw_odds > 3:
                true_odds['1'] = hw_odds
            if hnw_odds <= 4 and hnw_odds > 3:
                true_odds['-1'] = hnw_odds
            if len(true_odds) == 0:
                return is_qualifed
            else:
                return true_odds
        elif data['league_id'] in self.special_leagues_2:
            if hw_odds <= 4:
                true_odds['1'] = hw_odds
            if hnw_odds <= 3:
                true_odds['-1'] = hnw_odds
            if len(true_odds) == 0:
                return is_qualifed
            else:
                return true_odds
        else:
            if hw_odds > 6 or hnw_odds > 4:
                return is_qualifed
            else:
                true_odds['1'] = hw_odds
                true_odds['-1'] = hnw_odds
                return true_odds

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
