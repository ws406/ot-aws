import json
import glob
import pprint
import matplotlib.pyplot as plt
import pylab
from src.strategy_finding.sample_selector.divide_by_pin_odds import DivideByPinOdds
from src.utils.logger import OtLogger
from matplotlib import style
import numpy as np
import collections


def calculate_game_numbers (game_datas, bookie_list):
    result = {}
    for bookie_name in bookie_list:
        result [bookie_name] = 0
    result ['all'] = 0

    for game_data in game_datas:
        in_all = 1
        for bookie_name in bookie_list:
            if bookie_name in game_data ['odds'].keys ():
                result [bookie_name] += 1
            else:
                in_all = 0
        result ['all'] += in_all

    return result

def plot_bar_x(results_to_plot: dict):
    # config
    style.use ('fivethirtyeight')

    # Sort the data: biggest first
    sorted_data = collections.OrderedDict (sorted (results_to_plot.items (), key = lambda kv: kv [1], reverse = True))
    logger.debug(list(sorted_data.items()))

    # this is for plotting purpose
    index = np.arange(len(results_to_plot.items()))
    plt.bar(index, list(sorted_data.values()))
    plt.xlabel('Bookies', fontsize=12)
    plt.ylabel('No of games', fontsize=12)
    plt.xticks(index, list(sorted_data.keys()), fontsize=12, rotation=30)
    plt.title('Number games per bookie')
    plt.show()

############# Configuration ##################
# Get all data from file(s)
data_files = glob.glob("C:\\Users\wsun\\Documents\\projects\\ot-aws\\data\\basketball_all_odds_data\\*.json")
# data_files = glob.glob("C:\\Users\wsun\\Documents\\projects\\ot-aws\\data\\basketball_all_odds_data\\test\\*.json")

bookie_list = [
    "pinnacle",  # Pinnacle
    "will_hill",  # WH
    "vcbet",  # VcBet
    "bet365",  # Bet365
    "betvictor",  # VcBet2
    "BWin",
    "Betfair",
    "easybet",
    "ladbroke",
    "unibet",
    "jetbull",
    "matchbook",
]
logger = OtLogger('ot')

############# Functioning ##################
logger.debug(str(len(data_files)) + ' files to process...')
data = []
for f in data_files:
    print('processing file - ', f)
    with open (f) as f_data:
        tmp = json.load(f_data)
        data += tmp

logger.debug (str(len(data)) + ' games in total')

results = calculate_game_numbers(data, bookie_list)
plot_bar_x(results)

