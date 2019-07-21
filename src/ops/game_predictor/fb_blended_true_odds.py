from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.qualification_check import QualificationCheck
import collections


# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'true_odds'

    def __init__(self):
        pass

    @staticmethod
    def _get_average(local_list):
        number = 0
        for data in local_list:
            number = number + data
        return number / len(local_list)

    def _calc_true_odds(self, data):
        picked_bookie = list()
        picked_bookie.append('pinnacle')
        picked_bookie.append('bet365')
        picked_bookie.append('betvictor')

        odds_1 = []
        odds_x = []
        odds_2 = []
        try:
            for bookie in picked_bookie:
                benchmark_odds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
                odds_1.append(float(benchmark_odds['1']))
                odds_x.append(float(benchmark_odds['x']))
                odds_2.append(float(benchmark_odds['2']))
        except KeyError as ke:
            print(ke)
            return False

        home = self._get_average(odds_1)
        draw = self._get_average(odds_x)
        away = self._get_average(odds_2)
        return_rate = home * draw * away / (home * draw + draw * away + home * away)
        while return_rate < 0.999999:
            home = (3 * home) / (3 - ((1 - return_rate) * home))
            draw = (3 * draw) / (3 - ((1 - return_rate) * draw))
            away = (3 * away) / (3 - ((1 - return_rate) * away))
            return_rate = home * draw * away / (home * draw + draw * away + home * away)

        true_odds = dict()
        true_odds['1'] = home
        true_odds['x'] = draw
        true_odds['2'] = away
        return true_odds

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
        else:
            return_data = dict()
            return_data['gid'] = data ['game_id']
            return_data['league_id'] = data ['league_id']
            return_data['league_name'] = data ['league_name']
            return_data['kickoff'] = data ['kickoff']
            return_data['home_team_name'] = data ['home_team_name']
            return_data['away_team_name'] = data ['away_team_name']
            return_data['home_team_id'] = data ['home_team_id']
            return_data['away_team_id'] = data ['away_team_id']
            return_data['min_odds'] = self._calc_true_odds(data)
            return_data['strategy'] = self.strategy

            return return_data
