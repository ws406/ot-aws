import collections
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.fb_qualification_check import QualificationCheck
from src.utils.logger import OtLogger
from src.utils.true_odds_calculator import TrueOddsCalculator
import joblib
import math

# This game predictor provides true odds only
class BlendTrueAwayOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'blend_true_away_odds'
    profit_margin = 0.03 # This is to ensure we win something.
    profit_margin2 = 0.05
    special_leagues_1 = []
    special_leagues_2 = []

    def __init__(self, logger: OtLogger):
        self.logger = logger
        self.rf = joblib.load("./football_model_blend_bookie_away.sav")
        self.special_leagues_1.append(8) # German Bundesliga
        self.special_leagues_1.append(40) # Italian Serie B
        self.special_leagues_1.append(12) # France Ligue 2
        self.special_leagues_1.append(27) # Swiss Super League
        self.special_leagues_1.append(34) # Italian Serie A
        self.special_leagues_1.append(10) # Russia Premier League
        self.special_leagues_1.append(30) # Turkish Super Liga
        self.special_leagues_1.append(119) # Ukrainian Premier League
        self.special_leagues_1.append(103) # Champions League
        self.special_leagues_1.append(124) # Romanian Liga I
        self.special_leagues_1.append(89) # Copa Libertadores
        self.special_leagues_1.append(263) # Copa Sudamericana
        self.special_leagues_2.append(39) # England League 1
        self.special_leagues_2.append(35) # England League 2
        self.special_leagues_2.append(146) # England National League
        self.special_leagues_2.append(6) # Poland Super League
        self.special_leagues_2.append(136) # Hungary NB I
        self.special_leagues_2.append(22) # Norwegian Tippeligaen

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
        self.logger.log(str(local_list_home) + ',' + str(local_list_draw) + ',' + str(local_list_away) + ',' + str(home) + ',' + str(draw) + ',' + str(away) + ',' + str(raw_true_odds) + ',' + str(1 / raw_true_odds['2']))
        return 1 / raw_true_odds['2']

    def _calc_raw_true_odds(self, data, localProfitMargin):
        picked_bookie = list()
        vec = []
        is_qualifed = False

        try:
            picked_bookie.append('pinnacle')
            picked_bookie.append('betvictor')
            picked_bookie.append('ladbroke')
            feature1 = self._calc_prob(picked_bookie, data, 0)
            picked_bookie.append('bet365')
            #feature2 = self._calc_prob(picked_bookie, data, 0)

            localVec = []
            if feature1 > 0:
                localVec.append(feature1)
        except Exception as e:
            self.logger.log('missing odds - ' + str(e))
            return is_qualifed

        vec.append(localVec)
        probability = self.rf.predict_proba(vec)
        away_win_odds = 1 / probability[0,1]
        away_not_win_odds = 1 / probability[0,0]
        if data['league_id'] in self.special_leagues_2:
            localProfitMargin = profit_margin2
        aw_odds = away_win_odds * (1+localProfitMargin)
        anw_odds = away_not_win_odds * (1+localProfitMargin)
        self.logger.log('Key data,' + str(probability) + ',' + str(away_win_odds) + ',' + str(away_not_win_odds) + ',' + str(aw_odds) + ',' + str(anw_odds) + ',' + str(localProfitMargin))
        true_odds = {}
        if data['league_id'] in self.special_leagues_1 or data['league_id'] in self.special_leagues_2:
            if aw_odds <= 3:
                true_odds['1'] = aw_odds
            if anw_odds <= 3:
                true_odds['-1'] = anw_odds
            if len(true_odds) == 0:
                return is_qualifed
            else:
                return true_odds
        else:
            return is_qualifed

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
