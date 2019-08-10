import collections
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.qualification_check import QualificationCheck


# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'true_odds'
    profit_margin = 0.02 # This is to ensure we win something.
    leagueDivOne = list()
    leagueNoBet = list()
    benchmark_bookie = list()

    def __init__(self):
        # we choose the following liquid bookmakers odds as our filter
        self.benchmark_bookie.append('pinnacle')
        self.benchmark_bookie.append('bet365')
        self.benchmark_bookie.append('sb')
        self.benchmark_bookie.append('easybet')
        self.benchmark_bookie.append('sbobet')
        # leagues we can use the below three bookmakers to gen true odds
        self.leagueDivOne.append('Holland Eredivisie')
        self.leagueDivOne.append('Russia Premier League')
        self.leagueDivOne.append('England Championship')
        self.leagueDivOne.append('Belgian Pro League')
        self.leagueDivOne.append('English Premier League')
        self.leagueDivOne.append('German Bundesliga')
        self.leagueDivOne.append('Spanish La Liga')
        self.leagueDivOne.append('Spanish Segunda Division')
        self.leagueDivOne.append('France Ligue 1')
        self.leagueDivOne.append('Italian Serie A')
        self.leagueDivOne.append('Holland Jupiler League')
        self.leagueDivOne.append('Turkish Super Liga')
        self.leagueDivOne.append('USA Major League Soccer')
        self.leagueDivOne.append('J-League Division 2')
        self.leagueDivOne.append('J-League Division 1')
        self.leagueDivOne.append('Norwegian Tippeligaen')
        # backtest shows no benefit betting on the following leagues
        self.leagueNoBet.append('Chinese Super League')
        self.leagueNoBet.append('Korea League')
        self.leagueNoBet.append('Brazil Serie B')
        self.leagueNoBet.append('Swedish Allsvenskan')
        self.leagueNoBet.append('Finland Veikkausliga')

    def _get_average(self, localList):
        number = 0
        for data in localList:
            number = number + data
        return number / len(localList)

    def _calc_true_odds(self, data, true_odds):
        picked_bookie = list()
        picked_bookie.append('pinnacle')
        picked_bookie.append('bet365')
        if data['league_name'] in self.leagueDivOne:
            picked_bookie.append('betvictor')
        true_odds['1'] = 100.0
        true_odds['x'] = 100.0
        true_odds['2'] = 100.0
        local_list_home = []
        local_list_draw = []
        local_list_away = []
        compareBestOdds = list()
        compareBestOdds.append(0)
        compareBestOdds.append(0)
        compareBestOdds.append(0)

        try:
            for bookie in picked_bookie:
                benchmark_odds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
                home = float(benchmark_odds['1'])
                draw = float(benchmark_odds['x'])
                away = float(benchmark_odds['2'])
                local_list_home.append(home)
                local_list_draw.append(draw)
                local_list_away.append(away)
            for bookie in self.benchmark_bookie:
                compareOdds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
                if float(compareOdds['1']) > compareBestOdds[0]:
                    compareBestOdds[0] = float(compareOdds['1'])
                if float(compareOdds['x']) > compareBestOdds[1]:
                    compareBestOdds[1] = float(compareOdds['x'])
                if float(compareOdds['2']) > compareBestOdds[2]:
                    compareBestOdds[2] = float(compareOdds['2'])
        except (TypeError, KeyError):
            return False

        result = False
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
        true_odds['1'] = home * (1 + self.profit_margin)
        true_odds['x'] = draw * (1 + self.profit_margin)
        true_odds['2'] = away * (1 + self.profit_margin)

        # we only bet at calc true odds, when benchmark bookmaker odds is better than our calc ones
        # the reason we want to do this, is try to avoid adverse selection
        if compareBestOdds[0] < true_odds['1']:
            true_odds['1'] = 100.0
        else:
            result = True
        if compareBestOdds[1] < true_odds['x']:
            true_odds['x'] = 100.0
        else:
            result = True
        if compareBestOdds[2] < true_odds['2']:
            true_odds['2'] = 100.0
        else:
            result = True
        return result

    def get_prediction(self, data):
        # Check if game is qualified first, if not, return
        # Data looks like:
        # {
        #    "home_team_id":7642,
        #    "game_id":1090426,
        #    "league_name":"Chinese Super League",
        #    "home_team_name":"Shanghai East Asia FC",
        #    "home_team_rank":5,
        #    "league_id":60,
        #    "away_team_id":543,
        #    "rounds":"1",
        #    "season":"2015",
        #    "away_team_name":"Jiangsu Sainty",
        #    "away_team_rank":8,
        #    "is_played":1,
        #    "kickoff":1425713700.0,
        #    "odds":{
        #       "bet365":{
        #          "1425590700":{
        #             "1":"1.66",
        #             "x":"3.5",
        #             "2":"5.5"
        #          },
        #          "1425654300":{
        #             "1":"1.57",
        #             "x":"3.7",
        #             "2":"6"
        #          },
        #          "1425685020":{
        #             "1":"1.6",
        #             "x":"3.75",
        #             "2":"5.75"
        #          }
        #       },
        #       "pinnacle":{
        #          "1425624120":{
        #             "1":"1.72",
        #             "x":"3.74",
        #             "2":"5.25"
        #          },
        #          "1425679140":{
        #             "1":"1.63",
        #             "x":"3.86",
        #             "2":"6.09"
        #          },
        #          "1425710460":{
        #             "1":"1.55",
        #             "x":"4.09",
        #             "2":"6.88"
        #          }
        #       },
        #       "vcbet":{
        #          "1425624120":{
        #             "1":"1.72",
        #             "x":"3.74",
        #             "2":"5.25"
        #          },
        #          "1425679140":{
        #             "1":"1.63",
        #             "x":"3.86",
        #             "2":"6.09"
        #          },
        #          "1425710460":{
        #             "1":"1.55",
        #             "x":"4.09",
        #             "2":"6.88"
        #          }
        #       },
        #    },
        #    "probabilities":{
        #       "bet365":{
        #          "1425590700":{
        #             "1":0.5630301257677683,
        #             "x":0.2670371453641415,
        #             "2":0.16993272886809008
        #          },
        #          "1425654300":{
        #             "1":0.5931229795078682,
        #             "x":0.2516765075209062,
        #             "2":0.1552005129712255
        #          },
        #          "1425685020":{
        #             "1":0.5865351921115268,
        #             "x":0.2502550153009181,
        #             "2":0.16320979258755527
        #          }
        #       },
        #       "pinnacle":{
        #          "1425624120":{
        #             "1":0.559436773814883,
        #             "x":0.2572810831448124,
        #             "2":0.1832821430403045
        #          },
        #          "1425679140":{
        #             "1":0.5917398976486372,
        #             "x":0.24987980133867327,
        #             "2":0.15838030101268943
        #          },
        #          "1425710460":{
        #             "1":0.6233388787112867,
        #             "x":0.2362286704162578,
        #             "2":0.1404324508724556
        #          }
        #       },
        #       "vcbet":{
        #          "1425692520":{
        #             "1":0.5478368647819158,
        #             "x":0.2501327982057487,
        #             "2":0.20203033701233547
        #          },
        #          "1425710460":{
        #             "1":0.5798369814312435,
        #             "x":0.24942708139779748,
        #             "2":0.1707359371709589
        #          },
        #          "1425706860":{
        #             "1":0.5883611467693624,
        #             "x":0.2447582370560548,
        #             "2":0.1668806161745828
        #          },
        #          "1425605880":{
        #             "1":0.5477031557605345,
        #             "x":0.2543464797406471,
        #             "2":0.19795036449881848
        #          }
        #       }
        #    }
        # }

        is_qualified = QualificationCheck().is_qualified(data, self.benchmark_bookie)
        if not is_qualified:
            return False
        elif data['league_name'] in self.leagueNoBet:
            return False
        else:
            true_odds = dict()
            result = self._calc_true_odds(data, true_odds)
            if result:
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
