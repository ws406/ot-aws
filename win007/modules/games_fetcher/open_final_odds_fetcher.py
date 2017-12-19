from win007.modules.games_fetcher.odds_fetcher_interface import OddsFetcherInterface
from bs4 import BeautifulSoup
import re
import requests


class OpenFinalOddsFetcher(OddsFetcherInterface):

    def __init__(self, bids):
        super().__init__(bids)
        pass

    def get_odds(self, gid):
        response = requests.get(str.replace(self.odds_url_pattern, '$GAME_ID$', gid))
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
        # "macau_slot": {
        #     "open": {
        #         "1": 2.34,
        #         "X": 3.45,
        #         "2": 1.23
        #     },
        #     "final": {
        #         "1": 2.56,
        #         "X": 3.76,
        #         "2": 1.13
        #     }
        # }
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
            kelly_rates[bookie_name]["open"] = {}
            kelly_rates[bookie_name]["final"] = {}
            kelly_rates[bookie_name]["open"]["return_rate"] = self._str_to_float(data_list[9])
            kelly_rates[bookie_name]["final"]["return_rate"] = self._str_to_float(data_list[16])

        return odds, probability, kelly_rates

    def _str_to_float(self, str):
        try:
            rtn = float(str)
        except ValueError:
            rtn = None
        return rtn