from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
from src.ops.game_predictor.fb_blended_true_odds2 import BlendTrueOdds
from src.ops.game_predictor.fb_blended_true_odds_away import BlendTrueAwayOdds
from src.ops.game_predictor.fb_blended_true_odds_home import BlendTrueHomeOdds
from src.ops.game_predictor.fb_blended_true_odds_inplay2 import TrueOddsInplay2
from src.ops.game_predictor.fb_blended_true_odds_inplay3 import TrueOddsInplay3
from src.ops.operator.fb_operator import FbOperator
import time
import datetime
from src.utils.logger import OtLogger


class FbOperatorTrueOdds (FbOperator):

    # get_games_in_minutes = 15
    # amount = 2
    # mins_before_kickoff = 15

    league_ids = [
        36,  # English Premier League
        #37,  # England Championship
        8,  # German Bundesliga
        9,  # German Bundesliga 2
        11,  # France Ligue 1
        12,  # France Ligue 2
        16,  # Holland Eredivisie
        17,  # Holland Jupiler League
        30,  # Turkish Super Liga
        284,  # J-League Division 2
        21,  # USA Major League Soccer
        273,  # Australia A-League
        6, # Poland Super League
        13, # Finland Veikkausliga
        #192, # AFC Champions League
        #350, # AFC Cup
        5,  # Belgian Pro League
        7, # Denmark
        60,  # Chinese Super League
        157,  # Portugal Liga 1
        34,  # Italian Serie A
        40,  # Italian Serie B
        10,  # Russia premier
        303, # Egyptian Premier League
        133, # Croatia Super League
        700, # Thai Premier League
        25,  # J-League Division 1
        23,  # Portugal Primera Liga
        27, # Swiss Super League
        766, # Vietnam
        #4,  # Brazil Serie A
        #358, # Brazil Serie B
        235, # Russia League 1
        35,  # EFL2
        146, # English Nation League
        113, # Europa League
        3, # Austria Leagie 1
        119, # Ukrainian Premier League
        137, # Czech First League
        29,  # Scottish Premier League
        150,  # Scottish Championship
        89, # Copa Libertadores
        263, # Copa Sudamericana
        #32, # Greece
        26,  # Sweden
        #31,  # Spanish La Liga
        33,  # Spanish Segunda Division
        136, # Hungary NB I
        #124, # Romanian Liga I
        203, # France Ligue 3
        #1, # Ireland Premier Division
        #15, # Korea League
        121, # Swiss Challenge League
        122, # Sweden Superettan
        #308, # South Africa Premier League
        #292, # Saudi Professional League
        39,  # EFL1
        #84,  # English League Cup
        #90, # England FA Cup
        #81, # Spanish Copa
        #693,  # GE3
        #51, # German Cup
        #22,  # NOR1
        103, # Champions League
        #193, # Algeria
        #221, # Poland League 1
        #138, # Belgian Second Division
        #140, # Mexico Primera Division
        #165, # Northern Ireland Premier League
        #1413, # Spanish Segunda Division B
        #142, # Italian C1
        #297, # England Conference North
        #298, # England Conference South
        ##54, #French Cup
        ##67, # Euro Cup
        #326, # Tunisia
        ##321, # Morocco Pro 1
        #1385,
        #763,
        #1367,
        #41,
    ]

    def __init__(self, logger: OtLogger):
        self.gamePredictors = [TrueOdds(logger), BlendTrueOdds(logger), BlendTrueAwayOdds(logger), BlendTrueHomeOdds(logger), TrueOddsInplay2(logger)]
        FbOperator.__init__(self, logger)


if __name__ == '__main__':
    normal_interval_in_mins = 1
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
                logger.log("Next kickoff at UTC: " + str (earliest_game_kickoff))
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

        if wait <= 0:
            logger.exception('Something is wrong with setting the wait time!')
            wait = 20 # set wait to 20 seconds in case it needs to run soon
        else:
            logger.log("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (seconds = wait)))
            time.sleep (wait)
