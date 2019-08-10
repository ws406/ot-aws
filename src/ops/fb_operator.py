from src.win007.subject.fb_upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import \
    GameInfoAndAllOddsSequence
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
import time
import datetime
from src.ops.bet_placer.fb_betfair import FBBetfair
import sys
import abc


class FbOperator (abc.ABC):
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

    # Leave this for sub classes to set
    league_ids = {}

    get_games_in_minutes = 15

    amount = 20
    mins_before_kickoff = 2
    commission_rate = 0.05

    gameDetector = None
    gamePredictor = None
    gameBetPlacer = None

    def __init__ (self):
        self.gameDetector = UpcomingGamesProcessor (GameInfoAndAllOddsSequence (self.bids))
        self._set_up_betfair_instance()

    def _set_up_betfair_instance(self):
        args = len (sys.argv)

        if args < 3:
            print ('Please provide Application key and session token')
            app_key = input ('Enter your application key :')
            session_token = input ('Enter your session Token/SSOID :')
            print ('Thanks for the input provided')
        else:
            app_key = sys.argv [1]
            session_token = sys.argv [2]

        self.gameBetPlacer = FBBetfair (app_key, session_token, self.commission_rate)

    def execute (self, debug_mode):
        print ("Start...")

        # Get required data from process
        msg = "Getting games that will start in the next " + str (self.get_games_in_minutes) + " mins"
        if self.league_ids is not None:
            msg += " and from " + str (len (self.league_ids)) + " leagues.."
        print (msg)
        games = self.gameDetector.get_games (self.get_games_in_minutes, self.league_ids)  # Get games starting in the next 5 mins.

        # Return false to indicate that this needs to be return
        if games is False:
            print ('Failed to get data from URL. Retrying....')
            return False

        games_not_bet = []
        for game in games:
            actual_kickoff = datetime.datetime.fromtimestamp (game ['kickoff'])

            # Handle MLS
            # if betting_details['league_id'] == 21:
            #     # Kickoff is always 10 mins after the official kickoff time in game.
            #     actual_kickoff = datetime.datetime.fromtimestamp(betting_details['kickoff']) + datetime.timedelta(minutes = 10)

            # If actual_kickoff is more than mins_before_kickoff mins away, do not place bet
            if actual_kickoff - datetime.datetime.now() > datetime.timedelta(minutes = self.mins_before_kickoff):

                print ("Too early to place bet for game " + ' ' + game['home_team_name'] + ' vs ' +
                       game['away_team_name'])

                # Append this game to the list, so that it can be used to determine next runtime.
                games_not_bet.append(game)
                continue
            else:
                betting_details = self.gamePredictor.get_prediction(game)
                if betting_details is False:
                    print ("--- Game " + str(game['game_id']) + " is not qualified. ---")
                    print(game)
                    continue

                print ("+++ Game " + str(game['game_id']) + " is qualified. +++")
                result = self.gameBetPlacer.place_match_odds_bet(betting_details, self.amount, debug_mode)
                if debug_mode:
                    print('(debug_mode) - bet_placing_request_pay_load:')
                    print(result)
                else:
                    print(result)

        result = self.gameBetPlacer.keep_session_alive()
        if result ['status'] == 'error':
            # producer.send (kafka_topic_error, result)
            print(result)
        else:
            print ("Session renewed at " + str (datetime.datetime.now ()))

        return games_not_bet

    @staticmethod
    def find_next_run_time(games):
        kickoff_times = []
        for game in games:
            print(game)
            kickoff_times.append(game['kickoff'])

        return sorted(kickoff_times)[0]


if __name__ == '__main__':
    normal_interval_in_mins = 2
    operator = FbOperator()
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
            print ('Exception happened.... Try again later.')
            raise e

        print ("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (seconds = wait)))
        time.sleep (wait)
