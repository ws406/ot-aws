from bs4 import BeautifulSoup
import re
import requests
from pytz import timezone
import sys
from lib.win007.modules.games_fetcher.odds_fetcher_interface import OddsFetcherInterface
import datetime


class HistGamesFetcher:
    url_season_ids = 'http://info.nowgoal.com/jsData/LeagueSeason/sea%league_id%.js'
    url_league_info = 'http://info.nowgoal.com/jsData/matchResult/%season_id%/s%league_id%_en.js'
    odds_fetcher = None

    def __init__(self, odds_fetcher: OddsFetcherInterface):
        self.odds_fetcher = odds_fetcher
        pass

    def _get_season_page_contents(self, league_id, num_of_seasons):
        league_page_contents = []

        season_ids_url = str.replace(self.url_season_ids, '%league_id%', str(league_id))
        season_ids_soup = BeautifulSoup(requests.get(season_ids_url).text, "lxml")
        league_ids = re.findall('\'([0-9\-]+)\'', season_ids_soup.text)

        league_info_url = str.replace(self.url_league_info, '%league_id%', league_id)
        if num_of_seasons >= 1:
            for season_name_element in league_ids[:num_of_seasons]:
                url = str.replace(league_info_url, '%season_id%', season_name_element)
                print(url)
                league_page_contents.append(
                    BeautifulSoup(
                        requests.get(url).text,
                        "lxml"
                    )
                )
        else:
            print("num_of_seasons is expected to be a positive int instead of " + str(num_of_seasons))
            sys.exit()

        return league_page_contents

    def _get_games_details(self, content_soup):

        games = dict()
        # vars = str.split(content_soup.text, '];')
        # league_info = str.split(vars)

        league_info = re.search('', content_soup.text.strip()).group(1)
        game = dict()
        game["league_id"] = int(league_info[0])
        game["league_name"] = league_info[3]

        # TODO: add these to game_fetcher
        game["season"] = league_info[4]
        game["total_rounds"] = int(league_info[7])
        game["total_teams"] = int(league_info[8])
        # TODO: end of todo!

        # TODO: handle all rounds & all games in each round. TWO rounds splitting.
        individual_game_details = str.split(
            "1424600,31,-1,'2017-08-19 02:15',992,137,'1-0','1-0','17','9',0.25,0.25,'2','0.5/1',1,1,1,1,0,0,'','17','9'",
            ','
        )

        gid = int(individual_game_details[0])
        game['is_played'] = True if individual_game_details[2]=='-1' else False
        game["kickoff"] = kickoff

        game["home_team_name"] = self._get_home_team_name(tds)
        game["away_team_name"] = self._get_away_team_name(tds)
        game["home_team_rank"] = self._get_home_team_rank(tds)
        game["away_team_rank"] = self._get_away_team_rank(tds)
        game["odds"], game["probabilities"], game["kelly_rates"] = self.odds_fetcher.get_odds(gid)

        # Add game details to the games dict
        games[gid] = game


        pass

    def get_hist_games_by_league(self, league_id, num_of_seasons):

        content_soups = self._get_season_page_contents(league_id, num_of_seasons)
        games_details = dict()

        print(content_soups)
        sys.exit()


        for content_soup in content_soups:
            # TODO: replace fake data with request call to actual URL

            pass

        # response = requests.get(self.url_season_page)
        # soup = BeautifulSoup(response.text, "lxml")
        # game_rows = soup.findAll("tr", {"id": re.compile('tr_[0-9]{1,2}')})
        # games = dict()
        # # Then time range
        # time_slot_ends_at = (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).timestamp()
        #
        # for row in game_rows:
        #     tds = row.findAll("td")
        #
        #     # Grab kickoff time and check if continue.
        #     kickoff = self._get_kickoff_time(tds)
        #     if kickoff > time_slot_ends_at:
        #         break
        #
        #     # Grab league ID and check if skip
        #     lid = self._get_league_id(tds)
        #     if lid not in league_ids:
        #         continue
        #
        #     gid = self._get_game_id(tds)
        #     league_name = self._get_league_name(tds)
        #
        #     game = dict()
        #     game["league_id"] = lid
        #     game["league_name"] = league_name
        #     game["kickoff"] = kickoff
        #     game["home_team_name"] = self._get_home_team_name(tds)
        #     game["away_team_name"] = self._get_away_team_name(tds)
        #     game["home_team_rank"] = self._get_home_team_rank(tds)
        #     game["away_team_rank"] = self._get_away_team_rank(tds)
        #     game["odds"], game["probabilities"], game["kelly_rates"] = self.odds_fetcher.get_odds(gid)
        #
        #     # Add game details to the games dict
        #     games[gid] = game
        #
        # return games

    def _get_league_id(self, tds):
        # Extract league_id
        league_info_a = tds[1].find("a")
        if league_info_a:
            try:
                league_id = int(re.search('.=([0-9]+)', league_info_a.attrs['href']).group(1))
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

    def _get_home_team_rank(self, tds):
        font = tds[3].find("font")
        if font:
            try:
                home_team_rank = int(re.search('.*?([0-9]+)', font.text).group(1))
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
                away_team_rank = int(re.search('.*?([0-9]+)', font.text).group(1))
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
