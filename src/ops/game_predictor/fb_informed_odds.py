import collections
from src.ops.game_predictor.interface import GamePredictorInterface
from src.win007.observers.informed_odds.qualification_check import QualificationCheck

class InformedOdds(GamePredictorInterface):

    benchmark_bookie = 'bet365'
    strategy = 'informed_odds'
    allChoices = {}

    def __init__(self):
        self.gen_map()

    def gen_map(self):
        # 'English Premier League' - 36
        bookmaker = {}
        data = []
        data.append(0.007)
        data.append(25 * 60)
        bookmaker['macau_slot'] = data
        self.allChoices[36] = bookmaker
        data = []
        data.append(0.003)
        data.append(2700)
        self.allChoices[36]['sb'] = data

        # 'England Championship' - 37
        bookmaker = {}
        data = []
        data.append(0.02)
        data.append(3600)
        bookmaker['easybet'] = data
        self.allChoices[37] = bookmaker

        # 'Holland Eredivisie' - 16
        bookmaker = {}
        data = []
        data.append(0.002)
        data.append(1500)
        bookmaker['easybet'] = data
        self.allChoices[16] = bookmaker
        data = []
        data.append(0.005)
        data.append(900)
        self.allChoices[16]['ladbroke'] = data
        data = []
        data.append(0.003)
        data.append(1500)
        self.allChoices[16]['sbobet'] = data

        # 'Australia A-League' - 273
        bookmaker = {}
        data = []
        data.append(0.008)
        data.append(2700)
        bookmaker['will_hill'] = data
        self.allChoices[273] = bookmaker
        data = []
        data.append(0.007)
        data.append(3600)
        self.allChoices[273]['ladbroke'] = data

        # 'German Bundesliga' - 8
        bookmaker = {}
        data = []
        data.append(0.007)
        data.append(1200)
        bookmaker['macau_slot'] = data
        self.allChoices[8] = bookmaker
        data = []
        data.append(0.014)
        data.append(1800)
        self.allChoices[8]['sb'] = data

        # 'German Bundesliga 2' - 9
        bookmaker = {}
        data = []
        data.append(0.003)
        data.append(2700)
        bookmaker['sbobet'] = data
        self.allChoices[9] = bookmaker
        data = []
        data.append(0.016)
        data.append(2700)
        self.allChoices[9]['bet365'] = data

        # 'Holland Jupiler League' - 17
        bookmaker = {}
        data = []
        data.append(0.03)
        data.append(3600)
        bookmaker['bet365'] = data
        self.allChoices[17] = bookmaker

        # 'Spanish La Liga' - 31
        bookmaker = {}
        data = []
        data.append(0.004)
        data.append(3600)
        bookmaker['pinnacle'] = data
        self.allChoices[31] = bookmaker
        data = []
        data.append(0.005)
        data.append(3600)
        self.allChoices[31]['hkjc'] = data

        # 'Italian Serie A' - 34
        bookmaker = {}
        data = []
        data.append(0.008)
        data.append(900)
        bookmaker['bet365'] = data
        self.allChoices[34] = bookmaker
        data = []
        data.append(0.006)
        data.append(900)
        self.allChoices[34]['sb'] = data

        # 'France Ligue 1' - 11
        bookmaker = {}
        data = []
        data.append(0.018)
        data.append(7200)
        bookmaker['betfred'] = data
        self.allChoices[11] = bookmaker

        # 'France Ligue 2' - 12
        bookmaker = {}
        data = []
        data.append(0.018)
        data.append(2700)
        bookmaker['sbobet'] = data
        self.allChoices[12] = bookmaker

        # 'Scottish Premier League' - 29
        bookmaker = {}
        data = []
        data.append(0.006)
        data.append(9000)
        bookmaker['ladbroke'] = data
        self.allChoices[29] = bookmaker

        # 'Russia Premier League' - 10
        bookmaker = {}
        data = []
        data.append(0.012)
        data.append(600)
        bookmaker['sbobet'] = data
        self.allChoices[10] = bookmaker
        data = []
        data.append(0.015)
        data.append(3600)
        self.allChoices[10]['betvictor'] = data

        # 'Belgian Pro League' - 5
        bookmaker = {}
        data = []
        data.append(0.013)
        data.append(3600)
        bookmaker['snai'] = data
        self.allChoices[5] = bookmaker
        data = []
        data.append(0.002)
        data.append(1800)
        self.allChoices[5]['betvictor'] = data

        # 'Chinese Super League' - 60
        bookmaker = {}
        data = []
        data.append(0.012)
        data.append(1800)
        bookmaker['sb'] = data
        self.allChoices[60] = bookmaker

        # 'Korea League' - 15
        bookmaker = {}
        data = []
        data.append(0.002)
        data.append(1800)
        bookmaker['sbobet'] = data
        self.allChoices[15] = bookmaker

        # 'Norwegian Tippeligaen' - 22
        bookmaker = {}
        data = []
        data.append(0.001)
        data.append(1500)
        bookmaker['sb'] = data
        self.allChoices[22] = bookmaker
        data = []
        data.append(0.02)
        data.append(3600)
        self.allChoices[22]['pinnacle'] = data
        data = []
        data.append(0.008)
        data.append(5400)
        self.allChoices[22]['betclick'] = data

        # 'Brazil Serie A' - 4
        bookmaker = {}
        data = []
        data.append(0.002)
        data.append(300)
        bookmaker['sb'] = data
        self.allChoices[4] = bookmaker

        # 'J-League Division 1' - 25
        bookmaker = {}
        data = []
        data.append(0.025)
        data.append(7200)
        bookmaker['skybet'] = data
        self.allChoices[25] = bookmaker
        data = []
        data.append(0.004)
        data.append(3600)
        self.allChoices[25]['hkjc'] = data

        # 'Denmark Super League' - 7
        bookmaker = {}
        data = []
        data.append(0.025)
        data.append(2700)
        bookmaker['ladbroke'] = data
        self.allChoices[7] = bookmaker

        # 'Poland Super League' - 6
        bookmaker = {}
        data = []
        data.append(0.025)
        data.append(2700)
        bookmaker['ladbroke'] = data
        self.allChoices[6] = bookmaker
        data = []
        data.append(0.004)
        data.append(120)
        self.allChoices[6]['sb'] = data

        # 'Swiss Super League' - 27
        bookmaker = {}
        data = []
        data.append(0.002)
        data.append(900)
        bookmaker['betvictor'] = data
        self.allChoices[27] = bookmaker

        # 'Austria Leagie 1' - 3
        bookmaker = {}
        data = []
        data.append(0.02)
        data.append(2700)
        bookmaker['will_hill'] = data
        self.allChoices[3] = bookmaker
        data = []
        data.append(0.01)
        data.append(420)
        self.allChoices[3]['easybet'] = data
        data = []
        data.append(0.01)
        data.append(480)
        self.allChoices[3]['sbobet'] = data

        # 'Ukrainian Premier League' - 119
        bookmaker = {}
        data = []
        data.append(0.004)
        data.append(1800)
        bookmaker['snai'] = data
        self.allChoices[119] = bookmaker
        data = []
        data.append(0.01)
        data.append(540)
        self.allChoices[119]['easybet'] = data

        # 'Czech First League' - 137
        bookmaker = {}
        data = []
        data.append(0.012)
        data.append(2700)
        bookmaker['easybet'] = data
        self.allChoices[137] = bookmaker

        # 'Greece Super League' - 32
        bookmaker = {}
        data = []
        data.append(0.035)
        data.append(5400)
        bookmaker['will_hill'] = data
        self.allChoices[32] = bookmaker
        data = []
        data.append(0.018)
        data.append(5400)
        self.allChoices[32]['easybet'] = data

        # 'Hungary NB I' - 136
        bookmaker = {}
        data = []
        data.append(0.03)
        data.append(3600)
        bookmaker['easybet'] = data
        self.allChoices[136] = bookmaker

        # 'Croatia Super League' - 133
        bookmaker = {}
        data = []
        data.append(0.014)
        data.append(1800)
        bookmaker['sb'] = data
        self.allChoices[133] = bookmaker

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
        if data['league_id'] in self.allChoices.keys():
            cached_result = False
            for key, bookmaker in self.allChoices[data['league_id']].items():
                if key in data['probabilities'].keys():
                    probMove = self.allChoices[data['league_id']][key][0]
                    lookbackTime = self.allChoices[data['league_id']][key][1]
                    is_qualified = QualificationCheck().is_qualified(data, lookbackTime, probMove, key)
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
