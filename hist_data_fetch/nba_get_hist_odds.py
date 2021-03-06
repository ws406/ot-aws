from src.win007.modules.misc.basketball_hist_games_fetcher import HistGamesFetcher
from src.win007.modules.games_fetcher.basketball_odds_fetcher.game_info_and_all_odds_sequence import GameInfoAndAllOddsSequence
import time
import datetime
from src.utils.logger import OtLogger

class Main:
    # These data is used for
    bids = {
        2: "interwetten", # no data for NBA
        17: "pinnacle",  # Pinnacle
        19: "unibet",
        26: "will_hill",  # WH
        43: "coral",
        77: "Expekt",
        82: "vcbet",  # VcBet
        224: "jetbull",
        317: "SNAI",
        331: "matchbook",
        214: "bet365",  # Bet365
        506: "betvictor", # VcBet2
        265: "Macauslot",
        272: "BWin",
        431: "ChinaSlot",
        458: "SB",
        45: "Betfair",
        11: "5Dimes",
        48: "Centrebet",

        6: "easybet",
        83: "ladbroke",
        381: "marathon",
        457: "marathonbet",
        446: "skybet",
    }

    league_ids = {
        1 : 'National Basketball Association', # NBA
        # 14: 'Australia NBL',
        # 5: 'CBA',
        #22: 'Basketball Bundesliga',
    }

    league_id_to_year_month = {
        1: [                          # NBA season is from previous Oct to the following April
            '%year_from%_10',
            '%year_from%_11',
            '%year_from%_12',
            '%year_to%_1',
            '%year_to%_2',
            '%year_to%_3',
            '%year_to%_4',
        ],
        14: [
            '%year_from%_10',
            '%year_from%_11',
            '%year_from%_12',
            '%year_to%_1',
            '%year_to%_2',
        ],
        22: [
            #'%year_from%_9',
            '%year_from%_10',
            '%year_from%_11',
            '%year_from%_12',
            '%year_to%_1',
            '%year_to%_2',
            '%year_to%_3',
            '%year_to%_4',
            '%year_to%_5',
            ], # notice: Germany league, depends on season, may expand across different months each year
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
        replace = False
        for lid, lname in self.league_ids.items():
        # for lid in [273]:
            print("Start extracting historical games from " + str(len(self.league_ids)) + " leagues and "
                + str(num_of_seasons) + " seasons...")
            print("Processing league - " + str(lid))
            hist_game_fetcher.get_hist_games_by_league(
                lid,
                lname,
                num_of_seasons,
                start_season_offset,
                self.league_id_to_year_month[lid],
                replace # if True, it will re-gather odds for existing games
            )

if __name__ == '__main__':
    logger = OtLogger('../logs/hist.log')

    wait_in_hours = 12

    while (True):
        try:
            num_games = Main(logger).execute()
        except Exception as e:
            raise e
        print ("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (hours = wait_in_hours)))
        time.sleep (60 * 60 * wait_in_hours)
