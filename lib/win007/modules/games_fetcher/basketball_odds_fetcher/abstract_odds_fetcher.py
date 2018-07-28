import abc
import re
from bs4 import BeautifulSoup
from lib.crawler.browser_requests import BrowserRequests
from datetime import datetime
from pytz import timezone
import sys


class AbstractOddsFetcher(abc.ABC):
    bids = []
    odds_url_pattern = 'http://nba.win007.com/1x2/data1x2/%game_id%.js'
    game_page_data = dict()

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
        home_team_name = re.findall('hometeam="(.+?)"', raw_data)[0]
        away_team_name = re.findall('guestteam="(.+?)"', raw_data)[0]

        return kick_off, home_team_name, away_team_name

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
            gid_str = str(gid)
            url = str.replace(self.odds_url_pattern,
                '%game_id%', gid_str[0] + '/' + gid_str[1:3] + '/' + gid_str)
            try:
                data = BrowserRequests.get(url)
            except:
                print("Can't get data from URL - " + url)
                return None

            self.game_page_data[gid] = data

        return BeautifulSoup(data.text, "lxml")

    def _str_to_float(self, str):
        try:
            rtn = float(str)
        except ValueError:
            rtn = None
        return rtn