import collections
import math
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.fb_qualification_check import QualificationCheck
from src.utils.logger import OtLogger
from src.utils.true_odds_calculator import TrueOddsCalculator

# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

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
    benchmark_bookie.append('bet365')
    benchmark_bookie.append('tipico')
    benchmark_bookie.append('coral')
    benchmark_bookie.append('bovada')
    benchmark_bookie.append('betfred')
    benchmark_bookie.append('bet-at-home')
    benchmark_bookie.append('skybet')
    benchmark_bookie.append('sportsbet')
    benchmark_bookie.append('betvictor')
    benchmark_bookie.append('betclick')
    benchmark_bookie.append('efbet')
    benchmark_bookie.append('hkjc')
    benchmark_bookie.append('macau_slot')

    league_grp2 = list()
    league_grp2.append(34) # italy A
    league_grp2.append(40) # italy B
    league_grp2.append(31) # spain la liga
    league_grp2.append(33) # spain Segunda Division
    league_grp2.append(1413) #
    league_grp2.append(2254) #
    league_grp2.append(11) # France Ligue 1
    league_grp2.append(12) # France Ligue 2
    league_grp2.append(203) # France Ligue 3
    league_grp2.append(284) # J-League Division 2
    league_grp2.append(23) # Portugal Primera Liga
    league_grp2.append(358) # Brazil Serie B
    league_grp2.append(15) # Korea League
    league_grp2.append(140) # Mexico Primera Division
    league_grp2.append(133) # Croatia Super League
    league_grp2.append(119) # Ukrainian Premier League

    strategy = 'true_odds'
    profit_margin = 0.03
    profit_margin_2 = 0.05

    def __init__(self, logger: OtLogger):
        self.logger = logger

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

    def _calc_raw_true_odds(self, data, localProfitMargin):
        picked_bookie = list()

        picked_bookie.append('pinnacle')
        picked_bookie.append('bet365')
        picked_bookie.append('betvictor')
        picked_bookie.append('ladbroke')
        picked_bookie.append('will_hill')
        picked_bookie.append('sb')
        picked_bookie.append('coral')
        picked_bookie.append('skybet')

        local_list_home = []
        local_list_draw = []
        local_list_away = []
        is_qualifed = False

        try:
            for bookie in picked_bookie:
                # {'1533924960': {'1': '1.55', 'x': '4.01', '2': '7.84'}, '1533922980': {'1': '1.58', 'x': '3.92', '2': '7.41'}, ...}
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
        betHome = 0
        betAway = 0
        self.multiply = 1
        true_odds = self._calc_raw_true_odds(data, localProfitMargin)
        if true_odds:
            pinnacleOddsDict = collections.OrderedDict(sorted(data['odds']['pinnacle'].items(), reverse=True))
            home = float(pinnacleOddsDict[list(pinnacleOddsDict)[0]]['1'])
            draw = float(pinnacleOddsDict[list(pinnacleOddsDict)[0]]['x'])
            away = float(pinnacleOddsDict[list(pinnacleOddsDict)[0]]['2'])
            if home <= 8.5 and draw <= 8.5 and away <= 8.5:
                self.chosen_bet_bookie.clear()
                for bookie in self.benchmark_bookie:
                    latestOdds = {}
                    try:
                        latestOddsDict = collections.OrderedDict(sorted(data['odds'][bookie].items(), reverse=True))
                        latestOdds = latestOddsDict[list(latestOddsDict)[0]]
                        home = float(latestOdds['1'])
                        draw = float(latestOdds['x'])
                        away = float(latestOdds['2'])
                    except Exception as e:
                        self.logger.log('missing bench odds - ' + str(e))
                        latestOdds['1'] = 1.0
                        latestOdds['x'] = 1.0
                        latestOdds['2'] = 1.0
                        home = 0
                        draw = 0
                        away = 0
                    localProfitMargin = self.profit_margin
                    if data['league_id'] in self.league_grp2:
                        localProfitMargin = self.profit_margin_2
                    true_home = float(true_odds['1'])
                    true_draw = float(true_odds['x'])
                    true_away = float(true_odds['2'])
                    true_home = true_home * (1.0 + localProfitMargin)
                    true_draw = true_draw * (1.0 + localProfitMargin)
                    true_away = true_away * (1.0 + localProfitMargin)
                    self.logger.log(str(data['game_id']) + ', ' + bookie + ', ' + str(localProfitMargin) + ', ' + str(true_home) + ', ' + str(true_draw) + ', ' + str(true_away) + ', ' + str(home) + ', ' + str(draw) + ', ' + str(away))
                    if home > true_home:
                        self.logger.log(str(data['game_id']) + ', ' + bookie + ', home, ' + str(true_odds['1']) + ', ' + str(latestOdds['1']))
                        betHome = betHome + 1
                        value1 = self._round_up_odds(true_home / 0.98)
                        value2 = self._round_up_odds(home / 0.98)
                        if '1' in result:
                            if true_home not in result['1']:
                                result['1'].append(true_home)
                            if value1 not in result['1']:
                                result['1'].append(value1)
                            if value2 not in result['1']:
                                result['1'].append(value2)
                        else:
                            result['1'] = []
                            result['1'].append(true_home)
                            if value1 not in result['1']:
                                result['1'].append(value1)
                            if value2 not in result['1']:
                                result['1'].append(value2)
                        if '1' in self.chosen_bet_bookie:
                            self.chosen_bet_bookie['1'].append(bookie)
                        else:
                            self.chosen_bet_bookie['1'] = list()
                            self.chosen_bet_bookie['1'].append(bookie)
                        self.multiply = len(self.chosen_bet_bookie['1'])
                    if away > true_away:
                        self.logger.log(str(data['game_id']) + ', ' + bookie + ', away, ' + str(true_odds['2']) + ', ' + str(latestOdds['2']))
                        betAway = betAway + 1
                        value1 = self._round_up_odds(true_away / 0.98)
                        value2 = self._round_up_odds(away / 0.98)
                        if '2' in result:
                            if true_away not in result['2']:
                                result['2'].append(true_away)
                            if value1 not in result['2']:
                                result['2'].append(value1)
                            if value2 not in result['2']:
                                result['2'].append(value2)
                        else:
                            result['2'] = []
                            result['2'].append(true_away)
                            if value1 not in result['2']:
                                result['2'].append(value1)
                            if value2 not in result['2']:
                                result['2'].append(value2)
                        if '2' in self.chosen_bet_bookie:
                            self.chosen_bet_bookie['2'].append(bookie)
                        else:
                            self.chosen_bet_bookie['2'] = list()
                            self.chosen_bet_bookie['2'].append(bookie)
                        self.multiply = len(self.chosen_bet_bookie['2'])
                if (betHome == 0 and betAway > 1) or (betAway == 0 and betHome > 1):
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
                if '1' in true_odds:
                    bet_odds['1'] = 1.01
                elif '2' in true_odds:
                    bet_odds['2'] = 1.01
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
                return_data['side'] = "BACK"
                return_data['bookie'] = self.chosen_bet_bookie
                return return_data
            else:
                return False
