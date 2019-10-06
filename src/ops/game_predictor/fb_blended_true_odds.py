import collections
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.qualification_check import QualificationCheck
from src.utils.logger import OtLogger


# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'true_odds'
    profit_margin = 0.05 # This is to ensure we win something.
    profitChoice2List = list()
    profitChoice3List = list()
    profitChoice4List = list()
    leagueDivOne = list()
    leagueDivTwo = list()
    leagueDivThree = list()
    leagueDivFour = list()
    leagueDivFive = list()
    leagueDivSix = list()
    leagueDivSeven = list()
    leagueDivEight = list()
    leagueDivNine = list()
    leagueDivTen = list()
    leagueDiv11 = list()
    leagueDiv12 = list()
    leagueDiv13 = list()
    filter_bookies = list()

    def __init__(self, logger: OtLogger):
        self.logger = logger
        # we choose the following liquid bookmakers odds as our filter
        self.filter_bookies.append('pinnacle')
        self.filter_bookies.append('bet365')
        self.filter_bookies.append('sb')
        self.filter_bookies.append('sbobet')
        self.filter_bookies.append('easybet')
        self.filter_bookies.append('betclick')
        # leagues we can use the below three bookmakers to gen true odds
        self.leagueDivOne.append(10) # Russia 1
        self.leagueDivOne.append(31) # Spain 1
        self.leagueDivOne.append(17) # Holland 2
        self.leagueDivOne.append(25) # Japan 1
        self.leagueDivOne.append(11) # France 1
        self.leagueDivOne.append(34) # Italy 1
        #self.leagueDivOne.append(21) # USA

        self.leagueDivTwo.append(37) # English Championship
        self.leagueDivTwo.append(29) # Scottish Premier League
        self.leagueDivTwo.append(7) # Denmark Super League
        self.leagueDivTwo.append(22) # Norway 1
        self.leagueDivTwo.append(27) # Swiss 1
        self.leagueDivTwo.append(8) # Germany 1
        self.leagueDivTwo.append(273) # Australia
        self.leagueDivTwo.append(6) # Poland Super League
        self.leagueDivTwo.append(39) # English League 1

        self.leagueDivThree.append(40) # Italy 2
        self.leagueDivThree.append(60) # China

        self.leagueDivFour.append(124) # Romania
        self.leagueDivFour.append(9) # Germany 2
        self.leagueDivFour.append(26) # Sweden
        self.leagueDivFour.append(5) # Belgium 1

        self.leagueDivFive.append(4) # Brazil A
        self.leagueDivFive.append(358) # Brazil B

        self.leagueDivSix.append(3) # Austria

        self.leagueDivSeven.append(35) # England League 2

        self.leagueDivEight.append(13) # Finland

        self.leagueDivNine.append(284) # Japan 2

        self.leagueDivTen.append(16) # Holland 1

        self.leagueDiv11.append(36) # English Premier league

        self.leagueDiv12.append(33) # Spain 2

        self.leagueDiv13.append(23) # Portugal


    def _get_average(self, localList):
        number = 0
        for data in localList:
            number = number + data
        return number / len(localList)

    def _calc_true_odds(self, data):
        picked_bookie = list()
        if data['league_id'] in self.leagueDivSix:
            picked_bookie.append('will_hill')
        elif data['league_id'] in self.leagueDivTen:
            picked_bookie.append('betvictor')
        elif data['league_id'] in self.leagueDiv11:
            picked_bookie.append('betvictor')
            picked_bookie.append('macau_slot')
        elif data['league_id'] in self.leagueDivSeven:
            picked_bookie.append('bet365')
        elif data['league_id'] in self.leagueDivEight:
            picked_bookie.append('bet365')
            picked_bookie.append('betvictor')
            picked_bookie.append('ladbroke')
        elif data['league_id'] in self.leagueDivNine:
            picked_bookie.append('betway')
            picked_bookie.append('betvictor')
            picked_bookie.append('bwin')
            picked_bookie.append('pinnacle')
        else:
            picked_bookie.append('pinnacle')
            if data['league_id'] in self.leagueDivOne or data['league_id'] in self.leagueDivTwo or data['league_id'] in self.leagueDivThree or data['league_id'] in self.leagueDiv12:
                picked_bookie.append('bet365')
            if data['league_id'] in self.leagueDivOne or data['league_id'] in self.leagueDivThree or data['league_id'] in self.leagueDivFour:
                picked_bookie.append('betvictor')
            if data['league_id'] in self.leagueDivThree or data['league_id'] in self.leagueDivFive:
                picked_bookie.append('will_hill')
            if data['league_id'] in self.leagueDiv12:
                picked_bookie.append('betway')
            if data['league_id'] in self.leagueDiv13:
                picked_bookie.append('skybet')
        local_list_home = []
        local_list_draw = []
        local_list_away = []
        compareBestOdds = [0, 0, 0]
        is_qualifed = False

        try:
            for bookie in picked_bookie:
                benchmark_odds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
                home = float(benchmark_odds['1'])
                draw = float(benchmark_odds['x'])
                away = float(benchmark_odds['2'])
                local_list_home.append(home)
                local_list_draw.append(draw)
                local_list_away.append(away)
        except Exception as e:
            self.logger.log('missing odds - ' + str(e))
            return is_qualifed

        home = self._get_average(local_list_home)
        draw = self._get_average(local_list_draw)
        away = self._get_average(local_list_away)

        localProfitMargin = self.profit_margin
        home = home * (1 + localProfitMargin)
        draw = draw * (1 + localProfitMargin)
        away = away * (1 + localProfitMargin)

        true_odds = dict()

        true_odds['1'] = home
        true_odds['x'] = draw
        true_odds['2'] = away

        return true_odds

    def get_prediction(self, data):
        # Check if game is qualified first, if not, return
        is_qualified = QualificationCheck().is_qualified(data, self.benchmark_bookie)
        if not is_qualified:
            return False
        else:
            true_odds = self._calc_true_odds(data)
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
                return_data['strategy'] = "true_odds"
                return return_data
            else:
                return False
