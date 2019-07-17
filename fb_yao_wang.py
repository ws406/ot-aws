from src.win007.subject.fb_upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import \
    GameInfoAndAllOddsSequence
from src.ops.game_predictor.rf_6_leagues_no_hkjc import RF6LeagusNoHkjc
from src.ops.game_predictor.rf_6_leagues import RF6Leagus
import json


class Main:
    # These data is used for
    bids = {
        80: "macau_slot",  # Macao Slot
        115: "will_hill",  # WH
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        432: "hkjc",  # HKJC
        104: "interwetten"  # Interwetten
    }

    league_ids = [
        34,  # IT1
        36,  # EPL
        37,  # ENC
        31,  # ES1
        8,  # GE1
        16,  # HO1
    ]

    def __init__ (self):
        self.minutes = int (input ("Enter the minutes "))
        self.gameDetector = UpcomingGamesProcessor (GameInfoAndAllOddsSequence (self.bids))
        self.game_qualifier1 = RF6LeagusNoHkjc ()
        self.game_qualifier2 = RF6Leagus ()

    def execute (self):
        print ("Start...")

        # Get required data from process
        msg = "Getting games that will start in the next " + str (self.minutes) + " mins"
        if self.league_ids is not None:
            msg += " and from " + str (len (self.league_ids)) + " leagues.."
        print (msg)
        games = self.gameDetector.get_games (self.minutes, self.league_ids)  # Get games starting in the next 5 mins.

        # Return False to indicate that it failed to get games from URL
        if games is False:
            return False

        # Put your game data here to test
        i = j = 0

        # TODO: this is a big lame! Needs to correct it.
        for data in json.loads (json.dumps (games)):
            print ("gid: ", data ['game_id'])
            result1 = self.game_qualifier1.get_prediction (data)
            result2 = self.game_qualifier2.get_prediction (data)
            print ('qualifier1:' + str (result1))
            print ('qualifier2:' + str (result2))
            if result1 or result2:
                i += 1
            else:
                j += 1

        print (str (i) + " games qualified")
        print (str (j) + " games disqualified")


if __name__ == '__main__':
    try:
        Main ().execute ()
    except Exception as e:
        print ('Exception happened.... Try again later.')
