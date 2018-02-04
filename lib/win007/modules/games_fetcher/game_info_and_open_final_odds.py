from lib.win007.modules.games_fetcher.odds_fetcher_interface import OddsFetcherInterface
from bs4 import BeautifulSoup
import re
from lib.crawler.browser_requests import BrowserRequests
from datetime import datetime
from pytz import timezone
import sys

class GameInfoAndOpenFinalOddsFetcher(OddsFetcherInterface):

    game_page_data = dict()
    lower_league_ranking_prefix = 100

    def __init__(self, bids):
        super().__init__(bids)
        pass

    def get_game_metadata(self, gid):
        raw_data = self._get_data_soup_by_gid(gid).text.split('game=Array(')[0].split('var ')

        kick_off = self._get_kickoff(re.findall('MatchTime="(.+?)"', raw_data[6])[0])
        home_team_name = re.findall('hometeam="(.+?)"', raw_data[7])[0]
        away_team_name = re.findall('guestteam="(.+?)"', raw_data[8])[0]
        home_team_id = int(re.findall('hometeamID=(.+?);', raw_data[17])[0])
        away_team_id = int(re.findall('guestteamID=(.+?);', raw_data[18])[0])

        home_ranking_tmp = re.findall('hOrder="([\D]+)?(\d+)"', raw_data[19])[0]
        home_team_rank = int(home_ranking_tmp[1])
        if home_ranking_tmp[0]:
            home_team_rank += self.lower_league_ranking_prefix

        away_ranking_tmp = re.findall('gOrder="([\D]+)?(\d+)"', raw_data[20])[0]
        away_team_rank = int(away_ranking_tmp[1])
        if away_ranking_tmp[0]:
            away_team_rank += self.lower_league_ranking_prefix

        return kick_off, home_team_name, away_team_name, home_team_id, away_team_id, home_team_rank, away_team_rank

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
        if gid in self.game_page_data:
            data = self.game_page_data[gid]
        else:
            data = BrowserRequests.get(str.replace(self.odds_url_pattern, '%game_id%', str(gid)))
        return BeautifulSoup(data.text, "lxml")


    def get_odds(self, gid):
        raw_data = self._get_data_soup_by_gid(gid).text.split('game=Array(')[1].split(');')[0]

        # Build the regex to extract odds from bids: "((?=80\||115\||281\||177\|)(.*?))"
        regex_pattern = '"((?='
        for key, name in self.bids.items():
            regex_pattern += repr(key) + '\|'
            if key != list(self.bids.keys())[-1]:
                regex_pattern += '|'
        regex_pattern += ')(.*?))"'

        # Extract & parse odds data. Return a dictionary
        data_rows = re.finditer(regex_pattern, raw_data)
        odds = {}
        probability = {}
        kelly_rates = {}
        for data_row in data_rows:
            # Remove trailing and prefixing "
            data_list = data_row.group(1).split('|')
            # print(data_list)
            bookie_name = self.bids[int(data_list[0])]
            odds[bookie_name] = {}
            odds[bookie_name]["open"] = {}
            odds[bookie_name]["final"] = {}
            odds[bookie_name]["open"]["1"] = self._str_to_float(data_list[3])
            odds[bookie_name]["open"]["x"] = self._str_to_float(data_list[4])
            odds[bookie_name]["open"]["2"] = self._str_to_float(data_list[5])
            odds[bookie_name]["final"]["1"] = self._str_to_float(data_list[10])
            odds[bookie_name]["final"]["x"] = self._str_to_float(data_list[11])
            odds[bookie_name]["final"]["2"] = self._str_to_float(data_list[12])

            probability[bookie_name] = {}
            probability[bookie_name]["open"] = {}
            probability[bookie_name]["final"] = {}
            probability[bookie_name]["open"]["1"] = self._str_to_float(data_list[6])
            probability[bookie_name]["open"]["x"] = self._str_to_float(data_list[7])
            probability[bookie_name]["open"]["2"] = self._str_to_float(data_list[8])
            probability[bookie_name]["final"]["1"] = self._str_to_float(data_list[13])
            probability[bookie_name]["final"]["x"] = self._str_to_float(data_list[14])
            probability[bookie_name]["final"]["2"] = self._str_to_float(data_list[15])

            kelly_rates[bookie_name] = {}
            kelly_rates[bookie_name]["open"] = self._str_to_float(data_list[9])
            kelly_rates[bookie_name]["final"] = self._str_to_float(data_list[16])

        return odds, probability, kelly_rates

    def _str_to_float(self, str):
        try:
            rtn = float(str)
        except ValueError:
            rtn = None
        return rtn