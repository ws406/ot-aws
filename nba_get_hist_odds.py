from lib.win007.modules.misc.basketball_hist_games_fetcher import HistGamesFetcher
# from lib.win007.modules.games_fetcher.odds_fetcher.game_info_and_open_final_odds import GameInfoAndOpenFinalOddsFetcher
from lib.win007.modules.games_fetcher.odds_fetcher.game_info_and_all_odds_sequence import GameInfoAndAllOddsSequence


class Main:
    # These data is used for
    bids = {
        80: "macau_slot",  # Macao Slot
        115: "will_hill",  # WH
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        # 432: "hkjc",  # HKJC
        82:  "vcbet", # VcBet
        104: "interwetten" # Interwetten
    }

    league_ids = [
        1, # NBA
    ]

    league_id_to_year_month = {
        1: [                          # NBA season is from previous Oct to the following April
            '%year_from%_10',
            '%year_from%_11',
            '%year_from%_12',
            '%year_to%_1',
            '%year_to%_2',
            '%year_to%_3',
            '%year_to%_4',
        ]
    }

    def __init__(self):
        pass

    def execute(self):
        # odds_fetcher = GameInfoAndOpenFinalOddsFetcher(self.bids)
        odds_fetcher = GameInfoAndAllOddsSequence(self.bids)
        hist_game_fetcher = HistGamesFetcher(odds_fetcher)

        # Fetch historical games data league by league
        # for lid in self.league_ids:
        num_of_seasons = 5
        start_season_offset = 0
        for lid in self.league_ids:
        # for lid in [273]:
            print("Start extracting historical games from " + str(len(self.league_ids)) + " leagues and "
                + str(num_of_seasons) + " seasons...")
            print("Processing league - " + str(lid))
            hist_game_fetcher.get_hist_games_by_league(
                lid,
                num_of_seasons,
                start_season_offset,
                self.league_id_to_year_month[lid]
            )


if __name__ == '__main__':
    Main().execute()
