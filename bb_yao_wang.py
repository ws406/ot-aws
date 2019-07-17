from src.win007.subject.bb_upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.basketball_odds_fetcher.game_info_and_all_odds_sequence \
    import GameInfoAndAllOddsSequence
from src.ops.game_predictor.nba import Nba
from src.ops.game_predictor.nbaVcbet import NbaVcbet
import json


class Main:
    # These data is used for
    bids = {
        26: "will_hill",  # WH
        # 214: "bet365",  # Bet365
        17: "pinnacle",  # Pinnacle
        82: "vcbet",  # VcBet
        506: "betvictor",  # VcBet2
        6: "easybet",
        83: "ladbroke",
        381: "marathon",
        457: "marathonbet",
        446: "skybet",
    }

    league_names = {
        'NBA': 1  # NBA
    }

    def __init__ (self):
        self.minutes = int (input ("Enter the minutes "))
        self.gameDetector = UpcomingGamesProcessor (GameInfoAndAllOddsSequence (self.bids))
        self.qualifiers = [
            Nba (),
            # NbaVcbet ()
        ]

    def execute (self):
        print ("Start...")

        # Get required data from process
        msg = "Getting basketball games that will start in the next " + str (self.minutes) + " mins"
        if self.league_names is not None:
            msg += " and from " + str (len (self.league_names)) + " leagues.."
        print (msg)
        games = self.gameDetector.get_games (self.minutes, self.league_names)  # Get games starting in the next 5 mins.
        # Return False to indicate that it failed to get games from URL
        if games is False:
            return False
        file = open ('./test.json', 'w+')
        file.write (json.dumps (games))
        file.close ()

        # Put your game data here to test
        i = j = 0

        # Pass the file that has current season's data
        file_header = "./data/basketball_all_odds_data/"
        file_name = file_header + "National Basketball Association-2018-2019.json"

        # with open(file_name) as json_file:
        #	games = json.load(json_file)
        for data in games:
            print ("gid: ", data ['game_id'])
            game_qualified = 0
            for qualifier in self.qualifiers:
                result = qualifier.get_prediction (file_name, data, 'top')
                print (type(qualifier).__name__ + ':' + str (result))
                if result:
                    game_qualified += 1

            if game_qualified > 0:
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
        raise e
