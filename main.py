from lib.win007.observers.strategy_prefer_lower_ranked import PreferLowerRankedObserver as StrategyLowerRanked
# from lib.win007.observers.strategy_prefer_much_stronger_team import PreferStrongerTeamObserver as StrategyStrongerTeam
from lib.win007.observers.strategy_compare_macau_hkjc import MacauHKObserver as StrategyMacauHKJCCompare
from lib.win007.subject.upcoming_games import Subject as UpcomingGamesProcessor
# from lib.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_open_final_odds import GameInfoAndOpenFinalOddsFetcher
from lib.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import GameInfoAndAllOddsSequence


class Main:
    # These data is used for
    bids = {
        80: "macau_slot",  # Macao Slot
        115: "will_hill",  # WH
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        432: "hkjc",  # HKJC
    }
    minutes = 720
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

        113, # Euroba league
    ]

    league_ids = [37]


    def __init__(self):
        pass

    def execute(self):
        print("Start...")
        processor = UpcomingGamesProcessor(GameInfoAndAllOddsSequence(self.bids))

        # Register all observers which are strategy executors
        processor.register_observer(StrategyLowerRanked())
        processor.register_observer(StrategyMacauHKJCCompare())
        # processor.register_observer(StrategyStrongerTeam())

        # Get required data from process
        msg = "Getting games that will start in the next " + str(self.minutes) + " mins"
        if self.league_ids is not None:
            msg += " and from "+ str(len(self.league_ids)) + " leagues.."
        print(msg)
        games = processor.get_games(self.minutes, self.league_ids)    # Get games starting in the next 5 mins.
        print(games)
        print(str(len(games)) + " games found")



        # Notify all observers to action using the games data
        # processor.notify(games)  # Notify the strategy to handle these games.


if __name__ == '__main__':
    Main().execute()
