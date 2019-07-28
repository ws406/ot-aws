from src.win007.subject.fb_upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import \
    GameInfoAndAllOddsSequence
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
import time
import datetime
from src.ops.bet_placer.fb_betfair import FBBetfair
import sys


class Main:
    # These data is used for
    bids = {
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        81:  "betvictor",  # Bet Victor
        # 80: "macau_slot",  # Macao Slot
        # 115: "will_hill",  # WH
        # 432: "hkjc",  # HKJC
        # 104: "interwetten"  # Interwetten
    }

    league_ids = [
        34,  # IT1
        # 40,  # IT2
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
        12,  # FR2
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
        4,  # BRA1
        358,  # BRA2
        #
        23,  # POTG1
        29,  # SCOT1
        30,  # TUR1
        5,  # BEL1
        26,  # SWE1
        22,  # NOR1
        # 27,  # SWl1
        10,  # RUS1
        # 2,  # ARG1
        21,  # USA1
        # 415,  # CHILE1
        # 140,  # MEX1

        60,  # CHN1
        15,  # KOR1
        273,  # AUS
    ]

    get_games_in_minutes = 15

    amount = 10
    mins_before_kickoff = 2
    commission_rate = 0.05

    gameDetector = None
    gamePredictor = None
    gameBetPlacer = None

    def __init__ (self):
        self.gameDetector = UpcomingGamesProcessor (GameInfoAndAllOddsSequence (self.bids))
        self.gamePredictor = TrueOdds()
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

        for game_data in games:
            betting_details = self.gamePredictor.get_prediction(game_data)
            if betting_details is False:
                print ("--- Game " + str(game_data['game_id']) + " is not qualified. ---")
                continue
            else:
                actual_kickoff = datetime.datetime.fromtimestamp (game_data ['kickoff'])

                # Handle MLS
                # if betting_details['league_id'] == 21:
                #     # Kickoff is always 10 mins after the official kickoff time in game_data.
                #     actual_kickoff = datetime.datetime.fromtimestamp(betting_details['kickoff']) + datetime.timedelta(minutes = 10)

                # If actual_kickoff is more than mins_before_kickoff mins away, do not place bet
                if actual_kickoff - datetime.datetime.now() > datetime.timedelta(minutes = self.mins_before_kickoff):
                    print ("Too early to place bet for game " + ' ' + betting_details ['home_team_name'] + ' vs ' +
                           betting_details ['away_team_name'])
                    continue

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

        return len(games)


if __name__ == '__main__':
    normal_interval_in_mins = 2
    operator = Main()
    wait = operator.get_games_in_minutes

    while (True):
        try:
            num_games = operator.execute(debug_mode=False)

            # Failed to get games from URL, retry
            if num_games is False:
                continue

            if num_games == 0:
                wait = operator.get_games_in_minutes - normal_interval_in_mins
            else:
                wait = normal_interval_in_mins
        except Exception as e:
            print ('Exception happened.... Try again later.')
            raise e
        print ("Next run at UTC: " + str (datetime.datetime.now () + datetime.timedelta (minutes = wait)))
        time.sleep (60 * wait)
