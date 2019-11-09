from src.ops.game_predictor.bb_blended_true_odds_highest_odds import TrueOddsHighest
from src.ops.game_predictor.bb_blended_true_odds_inplay import TrueOddsInplay
from src.ops.operator.bb_operator import BbOperator
import time
import datetime
from src.utils.logger import OtLogger


class BbOperatorTrueOdds (BbOperator):

    get_games_in_minutes = 15
    amount = 20
    mins_before_kickoff = 2

    league_names = {
        'NBA': 1,
    }

    def __init__(self, logger: OtLogger):
        self.gamePredictors = [TrueOddsHighest(logger), TrueOddsInplay(logger)]
        BbOperator.__init__(self, logger)


if __name__ == '__main__':
    normal_interval_in_mins = 2
    logger = OtLogger('./logs/ops_bb_true_odds.log')
    operator = BbOperatorTrueOdds(logger)
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
