from src.win007.subject.upcoming_games import Subject as UpcomingGamesProcessor
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import \
        GameInfoAndAllOddsSequence
from src.ops.game_qualifier.nba import Nba
import json

class Main:
    # These data is used for
    bids = {
        26: "will_hill",  # WH
        #214: "bet365",  # Bet365
        17: "pinnacle",  # Pinnacle
        82:  "vcbet", # VcBet
        6: "easybet",
        83: "ladbroke",
        381: "marathon",
        446: "skybet",
    }

    league_ids = [
        1, # NBA
    ]

    def __init__(self):
            self.minutes = int(input("Enter the minutes "))
            self.gameDetector = UpcomingGamesProcessor(GameInfoAndAllOddsSequence(self.bids))
            self.game_qualifier1 = Nba()

    def execute(self):
            print("Start...")
            
            # Get required data from process
            msg = "Getting games that will start in the next " + str(self.minutes) + " mins"
            if self.league_ids is not None:
                    msg += " and from " + str(len(self.league_ids)) + " leagues.."
            print(msg)
            games = self.gameDetector.get_games(self.minutes, self.league_ids)  # Get games starting in the next 5 mins.
            
            # Put your game data here to test
            i = j = 0
            
            # TODO: this is a big lame! Needs to correct it.
            file_header =  = "~/ot-aws/data/basketball_all_odds_data/"
            file_name = file_header + "National Basketball Association-2018-2019.json"
            for data in json.loads(json.dumps(games)):
                    print("gid: ", data['game_id'])
                    result1 = self.game_qualifier1.is_game_qualified(file_name, data)
                    print('qualifier1:' + str(result1))
                    if result1:
                            i += 1
                    else:
                            j += 1
            
            print(str(i) + " games qualified")
            print(str(j) + " games disqualified")


if __name__ == '__main__':
        try:
                Main ().execute ()
        except Exception as e:
                print ('Exception happened.... Try again later.')
