from lib.win007.modules.games_fetcher.odds_fetcher_interface import OddsFetcherInterface
from bs4 import BeautifulSoup
import re
from lib.crawler.browser_requests import BrowserRequests


class GameInfoAndOpenFinalOddsFetcher(OddsFetcherInterface):

    def __init__(self, bids):
        super().__init__(bids)
        pass

    def get_odds(self, gid):
        response = BrowserRequests.get(str.replace(self.odds_url_pattern, '$GAME_ID$', str(gid)))
        soup = BeautifulSoup(response.text, "lxml")
        raw_data = soup.text.split('game=Array(')[1].split(');')[0]

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
            # TODO: get these details from the page too
            # "kickoff": 1233920412,
            # "home_team_id": 123,
            # "home_team_name": "TeamA",
            # "home_team_rank": 2,
            # "away_team_id": 456,
            # "away_team_name": "TeamB",
            # "away_team_rank": 5,

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