from src.win007.subject.fb_upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import \
    GameInfoAndAllOddsSequence
import datetime
from src.ops.bet_placer.fb_betfair import FBBetfair
import sys
import abc
from src.utils.logger import OtLogger
import time
from multiprocessing import Pool
import multiprocessing
from functools import partial


class FbOperator (abc.ABC):
    # These data is used for
    bids = {
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        81:  "betvictor",  # Bet Victor
        82: "ladbroke",

        # 80: "macau_slot",  # Macao Slot
        # 90: "easybet",  # EasyBet
        # 545: "sb",
        # 474: "sbobet",
        # 115: "will_hill",  # WH
        # 432: "hkjc",  # HKJC
        # 104: "interwetten"  # Interwetten
        # 156: "betfred",
        # 110: "snai",
        # 463: "betclick",
        # 167: "skybet",
        # 88: "coral",
        # 936: "setantabet",
        # 961: "championsbet",
        # 527: "tipico",
        # 136: "bodog",
        # 874: "bovada",
        # 695: "cashpoint",
        # 354: "boylesports",
        # 315: "victory",
        # 482: "betway",
        # 808: "betcity",
        # 798: "dafabet",
        # 255: "bwin",
        # 2: "betfair",
    }

    # Leave this for sub classes to set
    league_ids = {}

    get_games_in_minutes = 160

    amount = 10
    mins_before_kickoff = 0.5
    commission_rate = 0.02

    gameDetector = None
    gamePredictors = []
    gameBetPlacer = None

    def __init__ (self, logger: OtLogger):
        self.logger = logger
        self.gameDetector = UpcomingGamesProcessor (GameInfoAndAllOddsSequence (self.bids, self.logger), self.logger)
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

        self.gameBetPlacer = FBBetfair (app_key, session_token, self.commission_rate, self.logger)

    def execute (self, debug_mode):

        # Get required data from process
        msg = "Getting games that will start in the next " + str (self.get_games_in_minutes) + " mins"
        if self.league_ids is not None:
            msg += " and from " + str (len (self.league_ids)) + " leagues.."
        self.logger.log(msg)
        games = self.gameDetector.get_games (self.get_games_in_minutes, self.league_ids)  # Get games starting in the next 5 mins.

        # Return false to indicate that this needs to be return
        if games is False:
            self.logger.log('Failed to get data from URL. Retrying....')
            time.sleep (2)
            return False

        self.logger.log(str(len(games)) + " games to place odds on BF using multi-processing")
        start_time_m = datetime.datetime.now()
        with Pool(multiprocessing.cpu_count()) as p:
            place_bet_func = partial(self._place_bets, debug_mode=debug_mode)
            games_not_bet = p.map(place_bet_func, games)
        end_time_m = datetime.datetime.now()
        time_taken_m = end_time_m - start_time_m
        self.logger.log("Multi - Time taken to place bets for " + str(len(games)) + " games is " + str(time_taken_m))

        # p.map returns None when it is not right time to place bet for a game yet. Thus we end up having a list
        # of None, e.g. [None, None, None]. This causes issue down the line. This is to remove Nones from the list
        games_not_bet = [x for x in games_not_bet if x is not None]

        return games_not_bet

    def _place_bets(self, game, debug_mode):
        actual_kickoff = datetime.datetime.fromtimestamp (game ['kickoff'])

        # Handle MLS
        # if betting_details['league_id'] == 21:
        #     # Kickoff is always 10 mins after the official kickoff time in game.
        #     actual_kickoff = datetime.datetime.fromtimestamp(betting_details['kickoff']) + datetime.timedelta(minutes = 10)

        # If actual_kickoff is more than mins_before_kickoff mins away, do not place bet
        if actual_kickoff - datetime.datetime.now() > datetime.timedelta(minutes = self.mins_before_kickoff):

            self.logger.log("Too early to place bet for game " + ' ' + game['home_team_name'] + ' vs ' +
                   game['away_team_name'])
            return game

        else:

            for game_predictor in self.gamePredictors:
                self.logger.log("Game predictor:" + str(game_predictor))
                betting_details = game_predictor.get_prediction(game)
                if betting_details is False:
                    self.logger.log ("--- Game " + str(game['game_id']) + " is not qualified. ---")
                    continue

                self.logger.log ("+++ Game " + str(game['game_id']) + " is qualified. +++")
                self.logger.log(betting_details)
                result = self.gameBetPlacer.place_match_odds_bet(betting_details, self.amount, debug_mode)
                if debug_mode:
                    self.logger.log('(debug_mode) - bet_placing_request_pay_load:')
                    self.logger.log(result)
                else:
                    self.logger.log(result)

    @staticmethod
    def find_next_run_time(games):
        kickoff_times = []
        for game in games:
            kickoff_times.append(game['kickoff'])

        return sorted(kickoff_times)[0]
