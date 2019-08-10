import collections
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.qualification_check import QualificationCheck


# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'true_odds'
    profit_margin = 0.02 # This is to ensure we win something.
    leagueDivOne = list()
    filter_bookies = list()

    def __init__(self):
        # we choose the following liquid bookmakers odds as our filter
        self.filter_bookies.append('pinnacle')
        self.filter_bookies.append('bet365')
        self.filter_bookies.append('sb')
        self.filter_bookies.append('easybet')
        self.filter_bookies.append('sbobet')
        # leagues we can use the below three bookmakers to gen true odds
        self.leagueDivOne.append(16) # Holland 1
        self.leagueDivOne.append(10) # Russia 1
        self.leagueDivOne.append(37) # English Championship
        self.leagueDivOne.append(5) # Belgium 1
        self.leagueDivOne.append(36) # English Premier league
        self.leagueDivOne.append(8) # Germany 1
        self.leagueDivOne.append(31) # Spain 1
        self.leagueDivOne.append(33) # Spain 2
        self.leagueDivOne.append(11) # France 1
        self.leagueDivOne.append(34) # Italy 1
        self.leagueDivOne.append(17) # Holland 2
        self.leagueDivOne.append(30) # Turkey 1
        self.leagueDivOne.append(21) # USA
        self.leagueDivOne.append(284) # Japan 1
        self.leagueDivOne.append(25) # Japan 2
        self.leagueDivOne.append(22) # Norway 1

    def _get_average(self, localList):
        number = 0
        for data in localList:
            number = number + data
        return number / len(localList)

    def _calc_true_odds(self, data):
        picked_bookie = list()
        picked_bookie.append('pinnacle')
        picked_bookie.append('bet365')
        if data['league_id'] in self.leagueDivOne:
            picked_bookie.append('betvictor')
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
            for bookie in self.filter_bookies:
                compareOdds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
                if float(compareOdds['1']) > compareBestOdds[0]:
                    compareBestOdds[0] = float(compareOdds['1'])
                if float(compareOdds['x']) > compareBestOdds[1]:
                    compareBestOdds[1] = float(compareOdds['x'])
                if float(compareOdds['2']) > compareBestOdds[2]:
                    compareBestOdds[2] = float(compareOdds['2'])
        except Exception as e:
            print('missing odds - ' + str(e))
            return is_qualifed

        home = self._get_average(local_list_home)
        draw = self._get_average(local_list_draw)
        away = self._get_average(local_list_away)
        return_rate = home * draw * away / (home * draw + draw * away + home * away)
        while return_rate < 0.999999:
            home = (3 * home) / (3 - ((1 - return_rate) * home))
            draw = (3 * draw) / (3 - ((1 - return_rate) * draw))
            away = (3 * away) / (3 - ((1 - return_rate) * away))
            return_rate = home * draw * away / (home * draw + draw * away + home * away)
        true_odds = dict()
        home = home * (1 + self.profit_margin)
        draw = draw * (1 + self.profit_margin)
        away = away * (1 + self.profit_margin)

        # we only bet at calc true odds, when benchmark bookmaker odds is better than our calc ones
        # the reason we want to do this, is try to avoid adverse selection
        print('compareBestOdds: ', compareBestOdds)
        print('home: ', home, 'draw: ', draw, 'away: ', away)
        if compareBestOdds[0] >= home:
            true_odds['1'] = home
            is_qualifed = True
        if compareBestOdds[1] >= draw:
            true_odds['x'] = draw
            is_qualifed = True
        if compareBestOdds[2] >= away:
            true_odds['2'] = away
            is_qualifed = True

        if is_qualifed:
            return true_odds
        else:
            return False

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
