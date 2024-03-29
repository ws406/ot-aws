#from src.ops.game_predictor.fb_blended_true_odds_inplay import TrueOddsInplay
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
from src.ops.game_predictor.fb_blended_true_odds_strong_team import TrueOddsStrongTeam
#from src.ops.game_predictor.fb_blended_true_odds_inplay2 import TrueOddsInplay2
#from src.ops.game_predictor.fb_blended_true_odds_inplay3 import TrueOddsInplay3
from src.ops.operator.fb_operator import FbOperator
import time
import datetime
from src.utils.logger import OtLogger


class FbOperatorTrueOdds (FbOperator):

    # get_games_in_minutes = 15
    # amount = 2
    # mins_before_kickoff = 15

    league_ids = [
        36,  # EPL
        37,  # England Championship
        39,  # EFL1
        35,  # EFL2
        146, # English Nation League
        297, # England Conference North
        298, # England Conference South
        31,  # ES1
        33,  # ES2
        2254, # Spanish Primera Division
        1413, # Spanish Segunda Division B
        ##84,  # English League Cup
        90, # England FA Cup
        ##81, # Spanish Copa
        8,  # GE1
        ##9,  # GE2
        693,  # GE3
        ##51, # German Cup
        11,  # FR1
        12,  # FR2
        203, # France Ligue 3
        ##13, # FIN1
        16,  # HO1
        17,  # HO2
        25,  # JAP1
        284,  # JAP2
        1346,  # JAP3
        60,  # China
        4,  # BRA1
        #358, # BRA2
        #29,  # SCOT1
        #150,  # SCOT2
        5,  # BEL1
        22,  # NOR1
        ##10,  # Russia premier
        21,  # USA1
        26,  # Sweden
        122, # Sweden Superettan
        133, # Croatia Super League
        7, # Denmark Super League
        127, # Denmark League 1
        273,  # AUS
        6, # Poland super league
        221, # Poland League 1
        119, # Ukrainian Premier League
        137, # Czech First League
        3, # Austria Leagie 1
        136, # Hungary NB I
        103, # Champions League
        #113, # Europa League
        2187, # Europa Conference League
        193, # Algeria
        235, # Russia League 1
        ##138, # Belgian Second Division
        27, # Swiss Super League
        121, # Swiss Challenge League
        1, # Ireland Premier Division
        140, # Mexico Primera Division
        ##308, # South Africa Premier League
        ##700, # Thai Premier League
        766, # Vietnam
        89, # Copa Libertadores
        263, # Copa Sudamericana
        192, # AFC Champions League
        350, # AFC Cup
        165, # Northern Ireland Premier League
        135, # Welsh Premier
        34,  # Italy A
        40,  # Italy B
        142, # Italian C1
        #32, # Greece
        #23,  # POTG1
        157,  # POTG2
        30,  # Turkish Super Liga
        130, # Turkey 2
        ###54, #French Cup
        ###67, # Euro Cup
        124, # Romanian Liga I
        118, # Israel Premier League
        #15, # Korea League
        #194, # Singapore
        #326, # Tunisia
        ##321, # Morocco Pro 1
        #1385,
        #763,
        #1367,
        #41,
        #292, # Saudi Professional League
    ]

    def __init__(self, logger: OtLogger):
        self.gamePredictors = [TrueOdds(logger), TrueOddsStrongTeam(logger)]
        #self.gamePredictors = [TrueOddsStrongTeam(logger)]
        FbOperator.__init__(self, logger)


if __name__ == '__main__':
    normal_interval_in_mins = 0.6
    logger = OtLogger('./logs/ops_true_odds.log')
    operator = FbOperatorTrueOdds(logger)
    wait = operator.get_games_in_minutes * 60

    while (True):
        try:
            operator.get_account_info()
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
