from lib.win007.modules.games_fetcher.odds_fetcher.abstract_odds_fetcher import AbstractOddsFetcher
import re


class GameInfoAndOpenFinalOddsFetcher(AbstractOddsFetcher):

    def get_odds(self, gid):
        raw_data = self._get_data_soup_by_gid(gid)
        if raw_data is None:
            raise StopIteration

        raw_data = raw_data.text.split('game=Array(')[1].split(');')[0]
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

        return odds, probability
