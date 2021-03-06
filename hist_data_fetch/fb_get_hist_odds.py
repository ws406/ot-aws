from src.win007.modules.misc.football_hist_games_fetcher import HistGamesFetcher
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import GameInfoAndAllOddsSequence
from src.utils.logger import OtLogger


class Main:
    # These data is used for
    bids = {
        80: "macau_slot",  # Macao Slot
        115: "will_hill",  # WH
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        432: "hkjc",  # HKJC
        255: "bwin",
        88: "coral",
        71: "eurobet",
        110: "snai",
        82: "ladbroke",
        474: "sbobet",
        81: "betvictor",
        545: "sb",
        90: "easybet",
        2: "betfair",
        841: "smarkets",
        352: "matchbook",
        54: "betdaq",
        463: "betclick",
        156: "betfred",
        482: "betway",
        136: "bodog",
        874: "bovada",
        695: "cashpoint",
        961: "championsbet",
        798: "dafabet",
        571: "jetbull",
        936: "setantabet",
        167: "skybet",
        613: "sportsbet",
        706: "sportsbet.au",
        1129: "china",
        908: "topgoal",
        173: "bet-at-home",
        158: "Gamebookers",
        649: "ibcbet",
        60: "sts",
        450: "toto",
        436: "5dimes",
        808: "betcity",
        354: "boylesports",
        527: "tipico",
        315: "victory",
        104: "interwetten"  # Interwetten
    }

    league_ids = {
        # 34,  # IT1
        # 40,  # IT2
        #
        36: "English Premier League",  # EPL
        # 37,  # ENC
        # 39,  # EFL1
        # 35,  # EFL2
        #
        # 31,  # ES1
        # 33,  # ES2
        #
        # 8,  # GE1
        # 9,  # GE2
        #
        # 11,  # FR1
        # 12,  # FR2
        #
        # 13, # FIN1
        # 700, # THAI1
        #
        # 16,  # HO1
        # 17,  # HO2
        #
        # 25: "J-League Division 1",  # JAP1
        # 284: "J-League Division 2",  # JAP2
        #
        # 4,  # BRA1
        # 358,  # BRA2
        #
        # 23,  # POTG1
        # 29,  # SCOT1
        # 30,  # TUR1
        # 5: "Belgian Pro League",  # BEL1
        # 26,  # SWE1
        # 22,  # NOR1
        # 27,  # SWl1
        # 10,  # RUS1
        # 2,  # ARG1
        # 21,  # USA1
        # 415,  # CHILE1
        # 140,  # MEX1
        # 60 : "Chinese Super League",  # CHN1
        # 15: "Korea League",  # KOR1
        # 273,  # AUS
    }

    sub_league_ids = {
        40: 261,
        37: 87,
        39: 135,
        35: 139,
        33: 546,
        9:  132,
        12: 1778,
        16: 98,
        17: 94,
        284:808,
        25: 943,
        23: 1123,
        30: 690,
        5:  114,
        26: 431,
        10: 591,
        2:  1232,
        21: 165,
        415:28,
        140:44,
        15: 313,
        273:462,
        13: 1570,
        700: 442
    }

    def __init__(self, logger: OtLogger):
        self.logger = logger
        pass

    def execute(self):
        # football_odds_fetcher = GameInfoAndOpenFinalOddsFetcher(self.bids)
        odds_fetcher = GameInfoAndAllOddsSequence(self.bids, self.logger)
        hist_game_fetcher = HistGamesFetcher(odds_fetcher, self.logger)

        # Fetch historical games data league by league
        # for lid in self.league_ids:
        num_of_seasons = 1
        start_season_offset = 0

        # True means replace existing data for the games that are in the file already
        replace = False

        for lid, lname in self.league_ids.items():
        # for lid in [273]:
            print("Start extracting historical games from " + str(len(self.league_ids)) + " leagues and "
                + str(num_of_seasons) + " seasons...")
            print("Processing league - " + str(lid))
            if lid in self.sub_league_ids:
                hist_game_fetcher.get_hist_games_by_league(lid, num_of_seasons, start_season_offset, lname, replace,
                    self.sub_league_ids[lid])
            else:
                hist_game_fetcher.get_hist_games_by_league(lid, num_of_seasons, start_season_offset, lname, replace)


if __name__ == '__main__':
    logger = OtLogger('../logs/hist.log')
    Main(logger).execute()
