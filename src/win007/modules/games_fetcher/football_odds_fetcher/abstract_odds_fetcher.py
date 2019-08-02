import abc
import re
from bs4 import BeautifulSoup
from src.utils.browser_requests import BrowserRequests
from datetime import datetime
from pytz import timezone
import sys


class AbstractOddsFetcher(abc.ABC):
    bids = []
    # odds_url_pattern = 'http://1x2.nowscore.com/%game_id%.js'
    odds_url_pattern = 'http://1x2d.win007.com/%game_id%.js'
    game_page_data = dict()
    lower_league_ranking_prefix = 100

    def __init__(self, bids):
        self.bids = bids

    @abc.abstractmethod
    def get_odds(self, gid):
        pass

    def get_game_metadata(self, gid):
        # raw_data = self._get_data_soup_by_gid(gid).text.split('game=Array(')[0].split('var ')
        raw_data = self._get_data_soup_by_gid(gid)

        if raw_data is None:
            raise StopIteration

        raw_data = raw_data.text

        kick_off = self._get_kickoff(re.findall('MatchTime="(.+?)"', raw_data)[0])
        league_name = re.findall('matchname="(.+?)"', raw_data)[0]
        home_team_name = re.findall('hometeam="(.+?)"', raw_data)[0]
        away_team_name = re.findall('guestteam="(.+?)"', raw_data)[0]
        home_team_id = int(re.findall('hometeamID=(.+?);', raw_data)[0])
        away_team_id = int(re.findall('guestteamID=(.+?);', raw_data)[0])

        home_team_rank = self._get_team_ranking(re.findall('hOrder="(.+?)"', raw_data))
        away_team_rank = self._get_team_ranking(re.findall('gOrder="(.+?)"', raw_data))

        return kick_off, home_team_name, away_team_name, home_team_id, away_team_id, home_team_rank, away_team_rank, league_name

    def _get_team_ranking(self, ranking_string):
        # If no match, return None.
        if not ranking_string:
            return None

        tmp = re.findall('^([0-9]+)$', ranking_string[0])
        if len(tmp) == 1:
            return int(tmp[0])
        # When there is prefix and a number in the ranking_string
        else:
            tmp = re.findall('^(.+?)([0-9]+)$', ranking_string[0])
            return int(tmp[0][1]) + self.lower_league_ranking_prefix

    def _get_kickoff(self, kickoff_in_string):
        try:
            simplified_kickoff_in_string = str.replace(kickoff_in_string, '-1', '')
            datetime_obj = datetime.strptime(simplified_kickoff_in_string, '%Y,%m,%d,%H,%M,%S')
            kickoff = timezone('utc').localize(datetime_obj)
            rtn = kickoff.timestamp()
        except AttributeError:
            print("error while extracting 'kickoff'")
            sys.exit(1)

        return rtn

    def _get_data_soup_by_gid(self, gid):
        if gid in self.game_page_data.keys():
            data = self.game_page_data[gid]
        else:
            url = str.replace(self.odds_url_pattern, '%game_id%', str(gid))
            retry = 1
            data = None
            while retry <= 3:
                try:
                    data = BrowserRequests.get(url)
                except:
                    print("Can't get data from URL - " + url + ", retry = " + str(retry))
                    retry += 1
                    continue
                break
            if data is None:
                return None

            self.game_page_data[gid] = data

        return BeautifulSoup(data.text, "lxml")

    def clean_cached_game_data(self, gid):
        if gid in self.game_page_data.keys():
            del self.game_page_data[gid]

    def _str_to_float(self, str):
        try:
            rtn = float(str)
        except ValueError:
            rtn = None
        return rtn
