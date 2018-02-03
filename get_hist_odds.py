import sys
from lib.win007.modules.misc.hist_games_fetcher import HistGamesFetcher
from lib.win007.modules.games_fetcher.game_info_and_open_final_odds import GameInfoAndOpenFinalOddsFetcher
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

    def __init__(self):
        pass

    def execute(self):
        print("Start...")
        odds_fetcher = GameInfoAndOpenFinalOddsFetcher(self.bids)
        hist_game_fetcher = HistGamesFetcher(odds_fetcher)

        # Fetch historical games data league by league
        # for lid in self.league_ids:
        # TODO: check with Yaowang to see if it is enough
        num_of_seasons = 1
        for lid in [29]:
            game_datas = hist_game_fetcher.get_hist_games_by_league(lid, num_of_seasons)
            print(game_datas)
            # TODO: save data to AWS Dynamo DB

Main().execute()
