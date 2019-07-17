from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.true_odds.qualification_check import QualificationCheck


# This game predictor provides true odds only
class TrueOdds(GamePredictorInterface):

    benchmark_bookie = 'pinnacle'
    strategy = 'true_odds'

    def __init__(self):
        pass

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
        if is_qualified == 'x':
            return False
        else:
            # TODO: Yao Wang, this is for you to write.
            #     return {
            # 		"gid": data ['game_id'],
            # 		"league_id": data ['league_id'],
            # 		"league_name": data ['league_name'],
            # 		"kickoff": data ['kickoff'],
            # 		"home_team_name": data ['home_team_name'],
            # 		"away_team_name": data ['away_team_name'],
            # 		"home_team_id": data ['home_team_id'],
            # 		"away_team_id": data ['away_team_id'],
            #       "min_odds": {
            #           "1": 1.3,
            #           "x": 2.5,
            #           "2": 6.8,
            #       }
            # 		"min_odds_to_bet_on": nonFavTeamOdds,
            #       "strategy": self.strategy
            # 	}
            pass
