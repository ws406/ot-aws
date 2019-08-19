from src.ops.game_predictor.debug_fb_blended_true_odds import TrueOdds
from src.ops.fb_operator import FbOperator
import time
import datetime
from src.utils.logger import OtLogger


class FbOperatorTrueOdds (FbOperator):

        # These data is used for
    bids = {
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        81:  "betvictor",  # Bet Victor
        80: "macau_slot",  # Macao Slot
        90: "easybet",  # EasyBet
        545: "sb",
        82: "ladbroke",
        474: "sbobet",
        115: "will_hill",  # WH
        432: "hkjc",  # HKJC
        # 104: "interwetten"  # Interwetten
        156: "betfred",
        110: "snai",
        463: "betclick",
        167: "skybet",
    }

    league_ids = [
        34,  # IT1
        # 40,  # IT2
        #
        36,  # EPL
        37,  # ENC
        # 39,  # EFL1
        # 35,  # EFL2
        #
        31,  # ES1
        33,  # ES2
        #
        8,  # GE1
        #9,  # GE2
        #
        11,  # FR1
        #12,  # FR2
        #
        # 13, # FIN1
        # 700, # THAI1
        #
        16,  # HO1
        17,  # HO2
        #
        25,  # JAP1
        284,  # JAP2
        #
        #4,  # BRA1
        #
        #23,  # POTG1
        29,  # SCOT1
        #30,  # TUR1
        5,  # BEL1
        22,  # NOR1
        10,  # RUS1
        # 2,  # ARG1
        21,  # USA1
        # 415,  # CHILE1
        # 140,  # MEX1

        273,  # AUS
        7, # Denmark
        6, # Poland1

        27, # Swiss Super League

        # not entirely sure if we want to bet on these leagues
        #358, # BRA2
        #3, # Austria Leagie 1
        #124, # Romanian Liga I
    ]

    get_games_in_minutes = 2000
    amount = 10
    mins_before_kickoff = 2000

    def __init__(self, logger: OtLogger):
        self.logger = logger
        self.gamePredictor = TrueOdds()
        FbOperator.__init__(self, logger)


if __name__ == '__main__':
    normal_interval_in_mins = 3
    logger = OtLogger('./logs/debug.log')
    operator = FbOperatorTrueOdds(logger)
    wait = operator.get_games_in_minutes * 60

    while (True):
        try:
            games = operator.execute(debug_mode=True)
            # Test data
            # games = [
            #     {'game_id': 1691236, 'league_id': 358, 'kickoff': 1564613390, 'home_team_name': 'Sport Club Recife PE', 'away_team_name': 'Coritiba PR', 'home_team_id': 4176, 'away_team_id': 350, 'home_team_rank': 5, 'away_team_rank': 4, 'league_name': 'Brazil Serie B', 'odds': {}, 'probabilities': {}},
            #     {'game_id': 1691237, 'league_id': 358, 'kickoff': 1564613690, 'home_team_name': 'A Sport Club Recife PE', 'away_team_name': 'A Coritiba PR', 'home_team_id': 4176, 'away_team_id': 350, 'home_team_rank': 5, 'away_team_rank': 4, 'league_name': 'Brazil Serie B', 'odds': {}, 'probabilities': {}}
            # ]

            # Failed to get games from URL, retry
            if games is False:
                continue

            print(len(games))

            if len(games) > 0:
                # Find out the earliest kickoff time of the next matches
                earliest_game_kickoff = operator.find_next_run_time(games)
                now = time.time()
                # Start running the application "normal_interval_in_mins" before the earliest kickoff time
                wait = earliest_game_kickoff - now - (normal_interval_in_mins * 60)
            else:
                wait = (operator.get_games_in_minutes - normal_interval_in_mins) * 60

        except Exception as e:
            print ('Exception happened.... Try again later.')
            raise e

        if wait <= 0:
            wait = 30

        print ("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (seconds = wait)))
        time.sleep (wait)
