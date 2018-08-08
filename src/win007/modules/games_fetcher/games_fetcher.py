from bs4 import BeautifulSoup
import re
from src.crawler.browser_requests import BrowserRequests
from pytz import timezone
import sys
from src.win007.modules.games_fetcher.football_odds_fetcher.abstract_odds_fetcher import AbstractOddsFetcher
import datetime


class GamesFetcher:
    url_games_list = 'http://op1.win007.com/index.aspx'
    # url_games_list = 'http://data.nowgoal.com/1x2/index.htm'
    odds_fetcher = None

    def __init__(self, odds_fetcher: AbstractOddsFetcher):
        self.odds_fetcher = odds_fetcher
        pass

    def get_games_by_kickoff(self, minutes):
        return self._get_games_with_conditions(minutes)

    def get_games_by_kickoff_and_league(self, minutes, league_ids):
        return self._get_games_with_conditions(minutes, league_ids)

    def _get_games_with_conditions(self, minutes, league_ids=None):
        try:
            response = BrowserRequests.get(self.url_games_list)
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            print("Can't process url - " + self.url_games_list)
            sys.exit()

        soup = BeautifulSoup(response.content.decode('gb2312', 'ignore'), "html5lib")
        game_rows = soup.findAll("tr", {"id": re.compile('tr_[0-9]{1,2}')})

        games = []
        # Then time range
        time_slot_ends_at = (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).timestamp()

        for row in game_rows:
            tds = row.findAll("td")

            # Grab kickoff time and check if continue.
            kickoff = self._get_kickoff_time(tds)
            if kickoff > time_slot_ends_at:
                break

            # Grab league ID and check if skip
            lid = self._get_league_id(tds)
            if league_ids is not None and lid not in league_ids:
                continue

            gid = self._get_game_id(tds)

            game = dict()
            game["gid"] = gid
            game["league_id"] = lid
            game["kickoff"] = kickoff

            # TODO: for consistency - need to improve prediction code
            game["home_score"] = 0
            game["away_score"] = 0
            game["is_played"] = 0

            try:
                no_use_kickoff_time, \
                game["home_team_name"], \
                game["away_team_name"], \
                game["home_team_id"], \
                game["away_team_id"], \
                game["home_team_rank"], \
                game["away_team_rank"], \
                game["league_name"] \
                            = self.odds_fetcher.get_game_metadata(gid)

                game["odds"], \
                game["probabilities"] \
                    = self.odds_fetcher.get_odds(gid)

            except StopIteration:
                continue
            # Add game details to the games dict
            games.append(game)

        return games

    def _get_league_id(self, tds):
        # Extract league_id
        league_info_a = tds[1].find("a")
        if league_info_a:
            try:
                league_id = int(re.search('.[=|/]([0-9]+)', league_info_a.attrs['href']).group(1))
            except AttributeError:
                print("error while extracting 'league id'")
                sys.exit(1)
        else:
            league_id = None

        return league_id

    # def _get_league_name(self, tds):
    #     # Extract league_name
    #     league_info_a = tds[1].find("a")
    #     if league_info_a:
    #         league_name = league_info_a.text.strip()
    #     else:
    #         league_name = tds[1].text.strip()
    #
    #     return league_name

    def _get_kickoff_time(self, tds):
        try:
            datetime_obj = datetime.datetime.strptime(tds[2].text.strip(), '%y-%m-%d%H:%M')
            kickoff = timezone('Asia/Chongqing').localize(datetime_obj)
            rtn = kickoff.timestamp()
        except AttributeError:
            print("error while extracting 'kickoff'")
            sys.exit(1)

        return rtn

    def _get_game_id(self, tds):
        # Extract game_id
        try:
            game_id = int(re.search('/([0-9]+).', tds[12].find("a").attrs['href']).group(1))
        except AttributeError:
            print("error while extracting 'game id'")
            sys.exit(1)

        return game_id
