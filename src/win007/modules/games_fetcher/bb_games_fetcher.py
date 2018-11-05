from bs4 import BeautifulSoup
import re
from src.crawler.browser_requests import BrowserRequests
from pytz import timezone
import sys
from src.win007.modules.games_fetcher.basketball_odds_fetcher.abstract_odds_fetcher import AbstractOddsFetcher
import datetime


class GamesFetcher:
    url_games_list = 'http://nba.win007.com/1x2/'
    # url_games_list = 'http://nba.win007.com/1x2/cn/next-20181026.html'

    odds_fetcher = None

    league_size = {
        'NBA': 30,  # NBA
    }

    def __init__ (self, odds_fetcher: AbstractOddsFetcher):
        self.odds_fetcher = odds_fetcher
        pass

    def get_games_by_kickoff (self, minutes):
        return self._get_games_with_conditions (minutes)

    def get_games_by_kickoff_and_league (self, minutes, league_names):
        return self._get_games_with_conditions (minutes, league_names)

    def _get_games_with_conditions (self, minutes, league_names = None):
        try:
            response = BrowserRequests.get (self.url_games_list)
        except:
            print ("Can't process url - " + self.url_games_list)
            return

        soup = BeautifulSoup (response.content.decode ('gb2312', 'ignore'), "html5lib")
        game_rows = soup.findAll ("tr", {"id": re.compile ('tr_[0-9]{1,2}')})

        games = []
        # Then time range
        time_slot_ends_at = (datetime.datetime.now () + datetime.timedelta (minutes = minutes)).timestamp ()

        for row in game_rows:
            tds = row.findAll ("td")

            # Grab kickoff time from games list page and check if continue.
            kickoff_from_win007 = self._get_kickoff_time (tds)
            if kickoff_from_win007 > time_slot_ends_at:
                break

            # Grab league ID and check if skip
            lname = self._get_league_name (tds)
            if league_names is not None and lname not in league_names.keys ():
                continue

            gid = self._get_game_id (tds)

            game = dict ()
            game ["game_id"] = gid
            game ["league_id"] = league_names [lname]
            game ["league_name"] = lname
            game ["size"] = self.league_size [str (lname)]

            try:
                # Here we are grabbing the kickoff time again from odds page
                game ["kickoff"], \
                game ["home_team_name"], \
                game ["away_team_name"], \
                game ["home_team_id"], \
                game ["away_team_id"] \
                    = self.odds_fetcher.get_game_metadata (gid)

                game ["odds"], \
                game ["probabilities"] \
                    = self.odds_fetcher.get_odds (gid)

            except StopIteration as si:
                print ('failed to get odds or game metadata')
            # Add game details to the games dict
            games.append (game)
            self.odds_fetcher.clean_cached_game_data (gid)

        return games

    def _get_league_name (self, tds):
        # Extract league_name
        try:
            league_name = tds [1].text.strip ()
        except AttributeError as ae:
            print ("error while extracting 'league id'")
            raise ae
        return league_name

    def _get_kickoff_time (self, tds):
        try:
            datetime_obj = datetime.datetime.strptime (tds [2].text.strip (), '%y-%m-%d%H:%M')
            kickoff = timezone ('Asia/Chongqing').localize (datetime_obj)
            rtn = kickoff.timestamp ()
        except AttributeError as ae:
            print ("error while extracting 'kickoff'")
            raise ae

        return rtn

    def _get_game_id (self, tds):
        # Extract game_id
        try:
            game_id = int (re.search ('([0-9]+)(.htm)', tds [10].find ("a").attrs ['href']).group (1))
        except AttributeError as ae:
            print ("error while extracting 'game id'")
            raise ae

        return game_id
