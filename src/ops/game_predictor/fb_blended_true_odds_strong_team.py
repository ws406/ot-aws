import collections
import joblib
import math
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.fb_qualification_check import QualificationCheck
from src.utils.logger import OtLogger
from src.utils.true_odds_calculator import TrueOddsCalculator

# This game predictor provides true odds only
class TrueOddsStrongTeam(GamePredictorInterface):
    review_bookie = 'pinnacle'
    multiply = 1
    chosen_bet_bookie = dict()
    benchmark_bookie = list()
    benchmark_bookie.append('eurobet')
    benchmark_bookie.append('betway')
    benchmark_bookie.append('cashpoint')
    benchmark_bookie.append('setantabet')
    benchmark_bookie.append('ibcbet')
    benchmark_bookie.append('toto')
    benchmark_bookie.append('betcity')
    benchmark_bookie.append('bwin')
    benchmark_bookie.append('5dimes')
    benchmark_bookie.append('sts')
    benchmark_bookie.append('Gamebookers')
    benchmark_bookie.append('snai')
    benchmark_bookie.append('boylesports')
    benchmark_bookie.append('betfair')
    benchmark_bookie.append('Sportingbet')
    benchmark_bookie.append('coral')
    benchmark_bookie.append('bovada')
    benchmark_bookie.append('betfred')
    benchmark_bookie.append('bet-at-home')
    benchmark_bookie.append('skybet')
    benchmark_bookie.append('sportsbet')
    benchmark_bookie.append('betvictor')
    benchmark_bookie.append('betclick')
    benchmark_bookie.append('efbet')
    benchmark_bookie.append("interwetten")

    strategy = 'true_odds2'
    profit_margin = 0.05
    side = '0'
    choice = '0'

    def __init__(self, logger: OtLogger):
        self.logger = logger
        self.model = joblib.load("./football_model_16-21.6.v1.sav")

    def _get_average(self, localList):
        number = 0
        for data in localList:
            number = number + data
        return number / len(localList)

    def _round_up_odds(self, odds):
        if odds < 2:
            final_odds = math.floor(odds * 100) / 100 + 0.01
            return round(final_odds, 2)
        elif odds < 3:
            final_odds = math.floor(odds * 50) / 50 + 0.02
            return round(final_odds, 2)
        elif odds < 4:
            final_odds = math.floor(odds * 20) / 20 + 0.05
            return round(final_odds, 2)
        elif odds < 6:
            final_odds = math.floor(odds * 10) / 10 + 0.1
            return round(final_odds, 1)
        elif odds < 10:
            final_odds = math.floor(odds * 5) / 5 + 0.2
            return round(final_odds, 1)
        elif odds < 20:
            final_odds = math.floor(odds * 2) / 2 + 0.5
            return round(final_odds, 1)
        else:
            return math.floor(odds) + 1

    def _calc_raw_true_odds(self, data, localProfitMargin, picked_bookie):
        local_list_home = []
        local_list_draw = []
        local_list_away = []
        is_qualifed = False

        try:
            for bookie in picked_bookie:
                latestOddsDict = collections.OrderedDict(sorted(data['odds'][bookie].items(), reverse=True))
                latestOdds = latestOddsDict[list(latestOddsDict)[0]]

                home = float(latestOdds['1'])
                draw = float(latestOdds['x'])
                away = float(latestOdds['2'])
                local_list_home.append(home)
                local_list_draw.append(draw)
                local_list_away.append(away)
        except Exception as e:
            self.logger.log('missing odds for calculation - ' + str(e))
            return is_qualifed

        home = self._get_average(local_list_home)
        draw = self._get_average(local_list_draw)
        away = self._get_average(local_list_away)

        true_odds_calculator = TrueOddsCalculator()

        raw_true_odds = {}
        raw_true_odds['1'], raw_true_odds['2'], raw_true_odds['x'] = \
            true_odds_calculator.calculate_3_way_margin_prop(home, away, draw)

        raw_true_odds['1'] = raw_true_odds['1']
        raw_true_odds['2'] = raw_true_odds['2']
        raw_true_odds['x'] = raw_true_odds['x']

        return raw_true_odds

    def _calc_true_odds(self, data, localProfitMargin):
        result = {}
        picked_bookie = list()
        picked_bookie.append('pinnacle')
        picked_bookie.append('bet365')
        picked_bookie.append('betvictor')
        picked_bookie.append('ladbroke')
        picked_bookie.append('will_hill')
        picked_bookie.append('sb')
        picked_bookie.append('coral')
        picked_bookie.append('skybet')
        true_odds = self._calc_raw_true_odds(data, localProfitMargin, picked_bookie)
        self.side = '0'
        self.choice = '0'
        if true_odds:
            self.side = '1' if latestPinnacleOdds['1'] < latestPinnacleOdds['2'] else '2'
            localVec = []
            localVec.append(0 if self.side == '1' else 1)
            localVec.append(1 / float(true_odds[self.side]))
            picked_bookie = list()
            picked_bookie.append('pinnacle')
            true_odds_pinnacle = self._calc_raw_true_odds(data, localProfitMargin, picked_bookie)
            localVec.append(1 / float(true_odds_pinnacle[self.side]) - 1 / float(true_odds[self.side]))
            picked_bookie = list()
            picked_bookie.append('bet365')
            true_odds_bet365 = self._calc_raw_true_odds(data, localProfitMargin, picked_bookie)
            localVec.append(1 / float(true_odds_bet365[self.side]) - 1 / float(true_odds[self.side]))
            picked_bookie = list()
            picked_bookie.append('betvictor')
            true_odds_betvictor = self._calc_raw_true_odds(data, localProfitMargin, picked_bookie)
            localVec.append(1 / float(true_odds_betvictor[self.side]) - 1 / float(true_odds[self.side]))
            latestPinnacleOddsDict = collections.OrderedDict(sorted(data['odds']['pinnacle'].items(), reverse=True))
            latestPinnacleOdds = latestPinnacleOddsDict[list(latestPinnacleOddsDict)[0]]
            localVec.append(float(latestPinnacleOdds[self.side]))
            vec = []
            vec.append(localVec)
            probability = self.model.predict_proba(vec)
            true_strong_team_win_odds = float(1 / probability[0,1])
            true_strong_team_not_win_odds = float(1 / probability[0,0])
            self.chosen_bet_bookie.clear()
            for bookie in self.benchmark_bookie:
                latestOdds = {}
                try:
                    latestOddsDict = collections.OrderedDict(sorted(data['odds'][bookie].items(), reverse=True))
                    latestOdds = latestOddsDict[list(latestOddsDict)[0]]
                except Exception as e:
                    self.logger.log('missing bench odds - ' + str(e))
                    latestOdds['1'] = -1.0
                    latestOdds['x'] = -1.0
                    latestOdds['2'] = -1.0
                localProfitMargin = self.profit_margin
                strong_team_win_odds = true_strong_team_win_odds * (1.0 + localProfitMargin)
                strong_team_not_win_odds = true_strong_team_not_win_odds * (1.0 + localProfitMargin)
                bookie_strong_team_win_odds = float(latestOdds[self.side]) if float(latestOdds['x']) > 0 else 1.0
                nonFavSide = '2' if self.side == '1' else '1'
                bookie_strong_team_not_win_odds = float(latestOdds[nonFavSide]) * float(latestOdds['x']) / (float(latestOdds[nonFavSide]) + float(latestOdds['x'])) if float(latestOdds['x']) > 0 else 1.0
                self.logger.log(str(data['game_id']) + ', ' + bookie + ', ' + str(localProfitMargin) + ', ' + str(true_strong_team_win_odds) + ', ' + str(true_strong_team_not_win_odds) + ', ' + str(bookie_strong_team_win_odds) + ', ' + str(bookie_strong_team_not_win_odds))
                if bookie_strong_team_win_odds > strong_team_win_odds:
                    self.logger.log(str(data['game_id']) + ', ' + bookie + ', strong, ' + str(strong_team_win_odds) + ', ' + str(bookie_strong_team_win_odds))
                    self.choice = 'back'
                    if 'strong' in self.chosen_bet_bookie:
                        self.chosen_bet_bookie['strong'].append(bookie)
                    else:
                        self.chosen_bet_bookie['strong'] = list()
                        self.chosen_bet_bookie['strong'].append(bookie)
                    self.multiply = len(self.chosen_bet_bookie['strong'])
                if bookie_strong_team_not_win_odds > strong_team_not_win_odds:
                    self.logger.log(str(data['game_id']) + ', ' + bookie + ', weak, ' + str(strong_team_not_win_odds) + ', ' + str(bookie_strong_team_not_win_odds))
                    self.choice = 'lay'
                    if 'weak' in self.chosen_bet_bookie:
                        self.chosen_bet_bookie['weak'].append(bookie)
                    else:
                        self.chosen_bet_bookie['weak'] = list()
                        self.chosen_bet_bookie['weak'].append(bookie)
                    self.multiply = len(self.chosen_bet_bookie['weak'])
            if len(self.chosen_bet_bookie):
                result[self.side] = strong_team_win_odds
                return result
        return False

    def get_prediction(self, data, profit_margin = None):
        # Check if game is qualified first, if not, return
        is_qualified = QualificationCheck().is_qualified(data, self.review_bookie)
        if not is_qualified:
            return False
        else:
            local_profit_margin = profit_margin if profit_margin is not None else self.profit_margin
            true_odds = self._calc_true_odds(data, local_profit_margin)
            if true_odds is not False:
                return_data = dict()
                return_data['odds'] = true_odds
                bet_odds = {}
                if self.choice == 'back':
                    bet_odds[self.side] = 1.01
                else:
                    bet_odds[self.side] = 10.0
                return_data['true_odds'] = bet_odds
                return_data['multiply'] = self.multiply
                return_data['gid'] = data ['game_id']
                return_data['league_id'] = data ['league_id']
                return_data['league_name'] = data ['league_name']
                return_data['kickoff'] = data ['kickoff']
                return_data['home_team_name'] = data ['home_team_name']
                return_data['away_team_name'] = data ['away_team_name']
                return_data['home_team_id'] = data ['home_team_id']
                return_data['away_team_id'] = data ['away_team_id']
                return_data['strategy'] = self.strategy
                return_data['side'] = "BACK" if self.choice == 'back' else "LAY"
                return_data['bookie'] = self.chosen_bet_bookie
                return return_data
            else:
                return False

