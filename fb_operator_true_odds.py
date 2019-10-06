from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
from src.ops.fb_operator import FbOperator
import time
import datetime
from src.utils.logger import OtLogger


class FbOperatorTrueOdds (FbOperator):

    # get_games_in_minutes = 800
    # amount = 10
    # mins_before_kickoff = 2

    league_ids = [
        34,  # IT1
        40,  # IT2
        #
        36,  # EPL
        37,  # ENC
        39,  # EFL1
        35,  # EFL2
        #
        31,  # ES1
        33,  # ES2
        #
        8,  # GE1
        9,  # GE2
        #
        11,  # FR1
        #12,  # FR2
        #
        13, # FIN1
        # 700, # THAI1
        #
        16,  # HO1
        17,  # HO2
        #
        25,  # JAP1
        284,  # JAP2
        60,  # China
        #
        4,  # BRA1
        358, # BRA2
        #
        23,  # POTG1
        29,  # SCOT1
        #30,  # TUR1
        5,  # BEL1
        22,  # NOR1
        10,  # RUS1
        # 2,  # ARG1
        #21,  # USA1
        26,  # Sweden
        # 415,  # CHILE1
        # 140,  # MEX1

        273,  # AUS
        7, # Denmark
        6, # Poland1

        27, # Swiss Super League

        3, # Austria Leagie 1
        124, # Romanian Liga I
    ]

    def __init__(self, logger: OtLogger):
        self.gamePredictor = TrueOdds(logger)
        FbOperator.__init__(self, logger)


if __name__ == '__main__':
    normal_interval_in_mins = 2
    logger = OtLogger('./logs/ops_true_odds.log')
    operator = FbOperatorTrueOdds(logger)
    wait = operator.get_games_in_minutes * 60

    while (True):
        try:
            games = operator.execute(debug_mode=False)
            # Test data
            # games = [
            #     {'game_id': 1691236, 'league_id': 358, 'kickoff': 1564613390, 'home_team_name': 'Sport Club Recife PE', 'away_team_name': 'Coritiba PR', 'home_team_id': 4176, 'away_team_id': 350, 'home_team_rank': 5, 'away_team_rank': 4, 'league_name': 'Brazil Serie B', 'odds': {}, 'probabilities': {}},
            #     {'game_id': 1691237, 'league_id': 358, 'kickoff': 1564613690, 'home_team_name': 'A Sport Club Recife PE', 'away_team_name': 'A Coritiba PR', 'home_team_id': 4176, 'away_team_id': 350, 'home_team_rank': 5, 'away_team_rank': 4, 'league_name': 'Brazil Serie B', 'odds': {}, 'probabilities': {}}
            # ]

            # Failed to get games from URL, retry
            if games is False:
                continue

            if len(games) > 0:
                # Find out the earliest kickoff time of the next matches
                earliest_game_kickoff = operator.find_next_run_time(games)
                now = time.time()
                # Start running the application "normal_interval_in_mins" before the earliest kickoff time
                if earliest_game_kickoff < now:
                    wait = 0
                else:
                    wait = earliest_game_kickoff - now - (normal_interval_in_mins * 60)
            else:
                wait = (operator.get_games_in_minutes - normal_interval_in_mins) * 60

        except Exception as e:
            logger.exception('Exception happened.... Try again later.')
            raise e

        logger.log("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (seconds = wait)))
        time.sleep (wait)
