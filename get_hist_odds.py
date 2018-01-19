import sys
from lib.win007.modules.misc.hist_games_fetcher import HistGamesFetcher
from lib.win007.modules.games_fetcher.open_final_odds_fetcher import OpenFinalOddsFetcher
from lib.win007.modules.dbc.db_connector import DBCOnnector

class Main:
    # These data is used for
    bids = {
        80: "macau_slot",  # Macao Slot
        115: "will_hill",  # WH
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        432: "hkjc",  # HKJC
    }
    # TODO: check with Yaowang to see if it is enough
    num_of_seasons = 5
    league_ids = [
        34,  # IT1
        40,  # IT2

        36,  # EPL
        37,  # ENC
        39,  # EFL1
        35,  # EFL2

        31,  # ES1
        33,  # ES2

        8,  # GE1
        9,  # GE2

        11,  # FR1
        12,  # FR2

        16,  # HO1
        17,  # HO2

        25,  # JAP1
        284,  # JAP2

        4,  # BRA1
        358,  # BRA2

        23,  # POTG1
        29,  # SCOT1
        30,  # TUR1
        5,  # BEL1
        26,  # SWE1
        22,  # NOR1
        27,  # SW1
        10,  # RUS1
        30,  # TUR1
        2,  # ARG1
        21,  # USA1
        415,  # CHILE1
        140,  # MEX1
        50,  # CHN1
        15,  # KOR1
        273,  # AUS
    ]

    jh["R_1"] = [
        [1424600, 31, -1, '2017-08-19 02:15', 992, 137, '1-0', '1-0', '17', '9', 0.25, 0.25, '2', '0.5/1', 1, 1, 1, 1,
         0, 0, '', '17', '9'],
        [1424595, 31, -1, '2017-08-19 04:15', 91, 991, '1-0', '1-0', '12', '14', 0.75, 0.25, '2.5/3', '1', 1, 1, 1, 1,
         0, 1, '', '12', '14'],
        [1424598, 31, -1, '2017-08-20 00:15', 114, 106, '2-3', '1-1', '13', '6', 0.25, 0, '2.5', '1', 1, 1, 1, 1, 0, 0,
         '', '13', '6'],
        [1424606, 31, -1, '2017-08-20 02:15', 982, 109, '2-2', '2-0', '西乙2', '3', -1.25, -0.5, '2.5', '1', 1, 1, 1, 1,
         0, 1, '', 'SPA D2-2', '3'],
        [1424596, 31, -1, '2017-08-20 04:15', 86, 100, '1-1', '1-1', '4', '8', 1, 0.5, '2.5/3', '1', 1, 1, 1, 1, 1, 0,
         '', '4', '8'],
        [1424599, 31, -1, '2017-08-21 00:15', 92, 98, '0-0', '0-0', '7', '西乙3', 1, 0.5, '2.5', '1', 1, 1, 1, 1, 0, 1,
         '', '7', 'SPA D2-3'],
        [1424597, 31, -1, '2017-08-21 02:15', 84, 96, '2-0', '2-0', '2', '15', 2.5, 1, '3.5', '1.5', 1, 1, 1, 1, 0, 0,
         '', '2', '15'],
        [1424594, 31, -1, '2017-08-21 04:15', 93, 82, '0-3', '0-2', '16', '1', -1.75, -0.75, '3/3.5', '1/1.5', 1, 1, 1,
         1, 0, 1, '', '16', '1'],
        [1424593, 31, -1, '2017-08-22 02:15', 103, 107, '1-0', '0-0', '西乙1', '5', -0.25, 0, '2/2.5', '0.5/1', 1, 1, 1,
         1, 0, 0, '', 'SPA D2-1', '5'],
        [1424592, 31, -1, '2017-08-22 04:00', 102, 131, '0-1', '0-0', '11', '10', 0.5, 0.25, '2/2.5', '1', 1, 1, 1, 1,
         0, 0, '', '11', '10']];

    def __init__(self):
        pass

    def execute(self):
        print("Start...")
        odds_fetcher = OpenFinalOddsFetcher(self.bids)
        hist_game_fetcher = HistGamesFetcher(odds_fetcher)

        # Fetch historical games data league by league
        for lid in self.league_ids:
            gameDatas = hist_game_fetcher.get_hist_games_by_league(lid, self.num_of_seasons)
            print(gameDatas)
            # TODO: save data to AWS Dynamo DB

Main().execute()
