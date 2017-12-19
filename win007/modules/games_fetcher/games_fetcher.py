from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
from pytz import timezone
import sys
from win007.modules.games_fetcher.odds_fetcher_interface import OddsFetcherInterface


class GamesFetcher:
    url_games_list = 'http://op1.win007.com/index.aspx'
    odds_fetcher = None

    def __init__(self, odds_fetcher: OddsFetcherInterface):
        self.odds_fetcher = odds_fetcher
        pass

    def get_games(self):
        response = requests.get(self.url_games_list)
        soup = BeautifulSoup(response.text, "lxml")
        game_rows = soup.findAll("tr", {"id": re.compile('tr_[0-9]{1,2}')})
        games = {}
        for row in game_rows:
            tds = row.findAll("td")
            gid = self._get_game_id(tds)
            game = {}
            game["league_id"]= self._get_league_id(tds)
            game["league_name"] = self._get_league_name(tds)
            game["kickoff"] = self._get_kickoff_time(tds),
            game["home_team_name"] = self._get_home_team_name(tds)
            game["away_team_name"] = self._get_away_team_name(tds)
            game["home_team_rank"] = self._get_home_team_rank(tds)
            game["away_team_rank"] = self._get_away_team_rank(tds)
            game["odds"], game["probabilities"], game["kelly_rates"] = self.odds_fetcher.get_odds(gid)
            games[gid] = game
        return games

    def _get_league_id(self, tds):
        # Extract league_id
        league_info_a = tds[1].find("a")
        if league_info_a:
            try:
                league_id = re.search('.=([0-9]+)', league_info_a.attrs['href']).group(1)
            except AttributeError:
                print("error while extracting 'league id'")
                sys.exit(1)
        else:
            league_id = None

        return league_id

    def _get_league_name(self, tds):
        # Extract league_name
        league_info_a = tds[1].find("a")
        if league_info_a:
            league_name = league_info_a.text.strip()
        else:
            league_name = tds[1].text.strip()

        return league_name

    def _get_kickoff_time(self, tds):
        try:
            datetime_obj = datetime.strptime(tds[2].text.strip(), '%y-%m-%d%H:%M')
            kickoff_china = timezone('Asia/Chongqing').localize(datetime_obj)
            kickoff_timestamp = kickoff_china.timestamp()
        except AttributeError:
            print("error while extracting 'kickoff'")
            sys.exit(1)

        return kickoff_timestamp

    def _get_game_id(self, tds):
        # Extract game_id
        try:
            game_id = re.search('/([0-9]+).', tds[12].find("a").attrs['href']).group(1)
        except AttributeError:
            print("error while extracting 'game id'")
            sys.exit(1)

        return game_id

    def _get_home_team_rank(self, tds):
        font = tds[3].find("font")
        if font:
            try:
                home_team_rank = re.search('.*?([0-9]+)', font.text).group(1)
            except AttributeError:
                print("error while extracting 'home_team_rank'")
                sys.exit(1)
        else:
            home_team_rank = None

        return home_team_rank

    def _get_away_team_rank(self, tds):
        font = tds[11].find("font")
        if font:
            try:
                away_team_rank = re.search('.*?([0-9]+)', font.text).group(1)
            except AttributeError:
                print("error while extracting 'away_team_rank'")
                sys.exit(1)
        else:
            away_team_rank = None

        return away_team_rank

    def _get_home_team_name(self, tds):
        a = tds[3].find("a")
        if a:
            try:
                rtn = re.search('(.*?)(?=( |\[.+)|$)', a.text.strip()).group(1)
            except AttributeError:
                print("error while extracting 'home_team_name'")
                sys.exit(1)
        else:
            rtn = None

        return rtn

    def _get_away_team_name(self, tds):
        a = tds[11].find("a")
        if a:
            try:
                rtn = re.search('(.*?)(?=( |\[.+)|$)', a.text.strip()).group(1)
            except AttributeError:
                print("error while extracting 'away_team_name'")
                sys.exit(1)
        else:
            rtn = None

        return rtn
