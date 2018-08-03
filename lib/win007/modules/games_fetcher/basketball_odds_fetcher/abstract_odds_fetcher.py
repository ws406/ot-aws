import abc
import re
from bs4 import BeautifulSoup
from lib.crawler.browser_requests import BrowserRequests
import datetime
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
            # Add 10 more mins to the kickoff time.
            # Because NBA always starts 10 mins after planned kickoff and odds could change after planned kickoff.
            # If the 10 mins isn't added, it could cause issues.
            datetime_obj = datetime.datetime.strptime(simplified_kickoff_in_string, '%Y,%m,%d,%H,%M,%S') + \
                           datetime.timedelta(minutes = 10)
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

            # TODO: fix this! This is to make it work for NBA only when the url for 2013-2014 season is like:
            # http://nba.win007.com/1x2/data1x2/160570.js
            game_id_replacement = gid_str if gid < 188584 \
                else gid_str[0] + '/' + gid_str[1:3] + '/' + gid_str

            url = str.replace(self.odds_url_pattern, '%game_id%', game_id_replacement)
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