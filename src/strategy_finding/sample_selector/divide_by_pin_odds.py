from src.strategy_finding.sample_selector.interface import SampleSelectorInterface
from src.utils.logger import OtLogger
import collections
import pprint


class DivideByPinOdds(SampleSelectorInterface):

    def __init__(self, logger: OtLogger):
        super().__int__(logger)

    def get_selected_games_data(self, raw_data: dict, dividing_threshold_sets=None):
        self.logger.debug("Running game selector - SelectAll")
        return raw_data

    def get_sorted_game_data_sets(self, raw_data: list, dividing_threshold_sets, bookie_list):
        self.logger.debug("Running game selector - SelectAll")

        data_sets = {}

        # set up all sets first
        for set in dividing_threshold_sets:
            data_sets[str(set['min']) + '_to_' + str(set['max']) + '_home'] = []
            data_sets [str(set ['min']) + '_to_' + str(set ['max']) + '_away'] = []

        # Loop through data & add them to each set
        for data in raw_data:

            try:
                sorted_data = self._sort_game_data_timestamp (bookie_list, data)
            except KeyError as ke:
                # print (ke)
                continue
            home_pin_final_odds = list (sorted_data ['odds'] ['pinnacle'].items ()) [-1] [1] ["1"]
            away_pin_final_odds = list (sorted_data ['odds'] ['pinnacle'].items ()) [-1] [1] ["2"]

            for set in dividing_threshold_sets:
                set_name_home = str(set['min']) + '_to_' + str(set['max']) + '_home'
                set_name_away = str(set ['min']) + '_to_' + str(set ['max']) + '_away'
                if set['min'] < float(home_pin_final_odds) <= set['max']:
                    data_sets[set_name_home].append(data)
                elif set['min'] < float(away_pin_final_odds) <= set['max']:
                    data_sets [set_name_away].append(data)

        return data_sets


    # Order probs and odds by timestamp by small (earliest) to big (latest)
    def _sort_game_data_timestamp (self, bookie_list, game_data):
        probabilities = game_data ['probabilities']
        odds = game_data ['odds']
        for b_name in bookie_list:
            game_data ['probabilities'] [b_name] = collections.OrderedDict (
                sorted (probabilities [b_name].items (), reverse = False))
            game_data ['odds'] [b_name] = collections.OrderedDict (sorted (odds [b_name].items (), reverse = False))
        return game_data

