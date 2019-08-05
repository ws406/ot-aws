import collections
from src.ops.game_predictor.interface import GamePredictorInterface
# from src.win007.observers.informed_odds.qualification_check import QualificationCheck
from src.win007.observers.same_direction.qualification_check_lastHourSingleBookie import QualificationCheck

class InformedOdds(GamePredictorInterface):

    benchmark_bookie = 'bet365'
    strategy = 'informed_odds'
    allChoices = {}

    def __init__(self):
        self.gen_map()

    def gen_map(self):
        bookmaker = {}
        data = []
        data.append(0.007)
        data.append(25 * 60)
        bookmaker['macau_slot'] = data
        self.allChoices['English Premier League'] = bookmaker
        data = []
        data.append(0.003)
        data.append(2700)
        self.allChoices['English Premier League']['sb'] = data

        bookmaker = {}
        data = []
        data.append(0.02)
        data.append(3600)
        bookmaker['easybet'] = data
        self.allChoices['England Championship'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.002)
        data.append(1500)
        bookmaker['easybet'] = data
        self.allChoices['Holland Eredivisie'] = bookmaker
        data = []
        data.append(0.005)
        data.append(900)
        self.allChoices['Holland Eredivisie']['ladbroke'] = data
        data = []
        data.append(0.003)
        data.append(1500)
        self.allChoices['Holland Eredivisie']['sbobet'] = data

        bookmaker = {}
        data = []
        data.append(0.008)
        data.append(2700)
        bookmaker['will_hill'] = data
        self.allChoices['Australia A-League'] = bookmaker
        data = []
        data.append(0.007)
        data.append(3600)
        self.allChoices['Australia A-League']['ladbroke'] = data

        bookmaker = {}
        data = []
        data.append(0.007)
        data.append(1200)
        bookmaker['macau_slot'] = data
        self.allChoices['German Bundesliga'] = bookmaker
        data = []
        data.append(0.014)
        data.append(1800)
        self.allChoices['German Bundesliga']['sb'] = data

        bookmaker = {}
        data = []
        data.append(0.003)
        data.append(2700)
        bookmaker['sbobet'] = data
        self.allChoices['German Bundesliga 2'] = bookmaker
        data = []
        data.append(0.016)
        data.append(2700)
        self.allChoices['German Bundesliga 2']['bet365'] = data

        bookmaker = {}
        data = []
        data.append(0.03)
        data.append(3600)
        bookmaker['bet365'] = data
        self.allChoices['Holland Jupiler League'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.004)
        data.append(3600)
        bookmaker['pinnacle'] = data
        self.allChoices['Spanish La Liga'] = bookmaker
        data = []
        data.append(0.005)
        data.append(3600)
        self.allChoices['Spanish La Liga']['hkjc'] = data

        bookmaker = {}
        data = []
        data.append(0.008)
        data.append(900)
        bookmaker['bet365'] = data
        self.allChoices['Italian Serie A'] = bookmaker
        data = []
        data.append(0.006)
        data.append(900)
        self.allChoices['Italian Serie A']['sb'] = data

        bookmaker = {}
        data = []
        data.append(0.018)
        data.append(7200)
        bookmaker['betfred'] = data
        self.allChoices['France Ligue 1'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.018)
        data.append(2700)
        bookmaker['sbobet'] = data
        self.allChoices['France Ligue 2'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.006)
        data.append(9000)
        bookmaker['ladbroke'] = data
        self.allChoices['Scottish Premier League'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.012)
        data.append(600)
        bookmaker['sbobet'] = data
        self.allChoices['Russia Premier League'] = bookmaker
        data = []
        data.append(0.015)
        data.append(3600)
        self.allChoices['Russia Premier League']['betvictor'] = data

        bookmaker = {}
        data = []
        data.append(0.013)
        data.append(3600)
        bookmaker['snai'] = data
        self.allChoices['Belgian Pro League'] = bookmaker
        data = []
        data.append(0.002)
        data.append(1800)
        self.allChoices['Belgian Pro League']['betvictor'] = data

        bookmaker = {}
        data = []
        data.append(0.012)
        data.append(1800)
        bookmaker['sb'] = data
        self.allChoices['Chinese Super League'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.002)
        data.append(1800)
        bookmaker['sbobet'] = data
        self.allChoices['Korea League'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.001)
        data.append(1500)
        bookmaker['sb'] = data
        self.allChoices['Norwegian Tippeligaen'] = bookmaker
        data = []
        data.append(0.02)
        data.append(3600)
        self.allChoices['Norwegian Tippeligaen']['pinnacle'] = data
        data = []
        data.append(0.008)
        data.append(5400)
        self.allChoices['Norwegian Tippeligaen']['betclick'] = data

        bookmaker = {}
        data = []
        data.append(0.002)
        data.append(300)
        bookmaker['sb'] = data
        self.allChoices['Brazil Serie A'] = bookmaker

        bookmaker = {}
        data = []
        data.append(0.025)
        data.append(7200)
        bookmaker['skybet'] = data
        self.allChoices['J-League Division 1'] = bookmaker
        data = []
        data.append(0.004)
        data.append(3600)
        self.allChoices['J-League Division 1']['hkjc'] = data
        #print("Here", self.allChoices)

    def _calc_odds(self, data, directionCode):
        if self.benchmark_bookie in data['odds'].keys():
            odds = list(collections.OrderedDict(sorted(data['odds'][self.benchmark_bookie].items())).values())[-1]
            if self.benchmark_bookie == 'pinnacle':
                 # this is because pinnacle odds also has added OPEN and FINAL in the odds map
                odds = list(collections.OrderedDict(sorted(data['odds'][self.benchmark_bookie].items())).values())[-3]
            home = float(odds['1'])
            draw = float(odds['x'])
            away = float(odds['2'])
            if directionCode == '1':
                return home
            elif directionCode == '2':
                return away
            elif directionCode == '3':
                away_dc_odds = away * draw / (away + draw)
                return 1 + 1 / (away_dc_odds - 1)
            elif directionCode == '4':
                home_dc_odds = home * draw / (home + draw)
                return 1 + 1 / (home_dc_odds - 1)
            else:
                return False
        else:
            return False

    # return_data['bet_direction'] could have values of:
    # '1' predict_home_win
    # '2' predict_away_win 
    # '3' predict_home_not_win, namely lay home
    # '4' predict_away_not_win, namely lay away
    def get_prediction(self, data):
        if data['league_name'] in self.allChoices.keys():
            cached_result = False
            for key, bookmaker in self.allChoices[data['league_name']].items():
                if key in data['probabilities'].keys():
                    probMove = self.allChoices[data['league_name']][key][0]
                    lookbackTime = self.allChoices[data['league_name']][key][1]
                    movements = {}
                    is_qualified = QualificationCheck().is_qualified(data, lookbackTime, probMove, key, movements)
                    if is_qualified != False:
                        if cached_result == False:
                            cached_result = is_qualified
                        elif is_qualified != cached_result:
                            #print(data['game_id'], data['league_name'], is_qualified, cached_result)
                            return False
            if cached_result:
                return_data = dict()
                return_data['gid'] = data ['game_id']
                return_data['league_id'] = data ['league_id']
                return_data['league_name'] = data ['league_name']
                return_data['kickoff'] = data ['kickoff']
                return_data['home_team_name'] = data ['home_team_name']
                return_data['away_team_name'] = data ['away_team_name']
                return_data['home_team_id'] = data ['home_team_id']
                return_data['away_team_id'] = data ['away_team_id']
                return_data['bet_direction'] = cached_result
                return_data['bet_odds'] = self._calc_odds(data, cached_result)
                return_data['strategy'] = self.strategy

                return return_data
            else:
                return False
        else:
            return False
