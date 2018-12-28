import json
import glob
import pprint
import matplotlib.pyplot as plt
import pylab
from src.strategy_finding.sample_selector.divide_by_pin_odds import DivideByPinOdds
from src.utils.logger import OtLogger
from matplotlib import style


def plot_scores(bookie_list, score_sets):

    cm = pylab.get_cmap ('tab20c')
    style.use ('fivethirtyeight')
    num_rows = (len(score_sets.keys()) / len(score_sets.items())) * 2
    num_cols = 3
    fig_num = 1
    num_bookies = len(bookie_list)
    total_fig_in_one_plot = num_rows * num_cols
    lines = {}
    for ds_name, score_set in score_sets.items():
        for when, score in score_set.items():
            title = ds_name + '_' + when
            plt.subplot(num_rows, num_cols, fig_num)

            i = 0
            for bookie_name in bookie_list:
                color = cm (1. * i / num_bookies)
                if bookie_name not in score.keys():
                    continue
                lines[bookie_name], = (plt.plot (score [bookie_name].keys (), score [bookie_name].values (), color = color,
                                        label = bookie_name))
                i += 1
            plt.title(title)

            # If we have plotted enough in one diagram, print it and start again.
            if fig_num % total_fig_in_one_plot == 0:
                plt.figlegend(tuple(lines.values()), tuple(lines.keys()), ncol = num_bookies)
                plt.show ()
                fig_num = 1
                lines = {}
            else:
                fig_num += 1

def sort_bookies_by_init_prob(bookie_list, bookie_scores, sorted_data):
    _sort_by_probs(bookie_list, bookie_scores, sorted_data, 0)


def sort_bookies_by_final_prob(bookie_list, bookie_scores, sorted_data):
    _sort_by_probs(bookie_list, bookie_scores, sorted_data, -1)

def sort_bookies_by_prob_delta(bookie_list, bookie_scores, sorted_data):
    game_result = "1" if sorted_data ['home_score'] - sorted_data ['away_score'] > 0 else "2"

    prob_delta_bookie = {}
    for bookie_name in bookie_list:
        initial_prob = list(sorted_data ['probabilities'][bookie_name].items())[0][1][game_result]
        final_prob = list(sorted_data ['probabilities'][bookie_name].items())[-1][1][game_result]
        prob_delta_bookie[bookie_name] = final_prob - initial_prob

    _build_scores (prob_delta_bookie, bookie_scores, sorted_data)


def _sort_by_probs(bookie_list, bookie_scores, sorted_data, key):
    game_result = "1" if sorted_data ['home_score'] - sorted_data ['away_score'] > 0 else "2"

    prob_bookie = {}
    for bookie_name in bookie_list:
        prob_bookie [bookie_name] = list (sorted_data ['probabilities'] [bookie_name].items ()) [key] [1] [game_result]

    _build_scores(prob_bookie, bookie_scores, sorted_data)


def _build_scores(prob_bookie, bookie_scores, sorted_data):
    season = sorted_data ['season'][2:4]
    total_points = len (bookie_list)
    i = total_points//2

    for (bookie, prob) in sorted (prob_bookie.items (), key = lambda kv: kv [1], reverse = True):
        if bookie in bookie_scores:
            if season in bookie_scores [bookie]:
                bookie_scores [bookie][season] += total_points - i
            else:
                bookie_scores [bookie][season] = total_points - i
        else:
            bookie_scores [bookie] = {}
            bookie_scores [bookie][season] = total_points - i
        i += 1

############# Configuration ##################
# Get all data from file(s)
data_files = glob.glob("C:\\Users\wsun\\Documents\\projects\\ot-aws\\data\\basketball_all_odds_data\\backup\\*.json")
# data_files = glob.glob("C:\\Users\wsun\\Documents\\projects\\ot-aws\\data\\basketball_all_odds_data\\test\\*.json")

bookie_list = [
    "pinnacle",  # Pinnacle
    "will_hill",  # WH
    # "coral",
    # "Expekt",
    "vcbet",  # VcBet
    # "SNAI",
    "bet365",  # Bet365
    "betvictor",  # VcBet2
    # "Macauslot",
    "BWin",
    # "ChinaSlot",
    # "SB",
    "Betfair",
    # "5Dimes",
    # "Centrebet",
    "easybet",
    "ladbroke",
    # "marathon",
    # "marathonbet",
    # "skybet",
]

############# Functioning ##################
print(len(data_files), ' files to process...')
data = []
for f in data_files:
    print('processing file - ', f)
    with open (f) as f_data:
        tmp = json.load(f_data)
        data += tmp
print (len(data), ' games to process')


# Go through them one by one and do the following things:
# Rank bookies on 'initial odds'
# Rank bookies on 'odds at kickoff-55 mins'
# Rank bookies on 'final odds'
# Rank bookies on 'initial odds' - 'odds at kickoff-55 mins'

dividing_threshold = [
    {'min':1.0, 'max':1.5},
    {'min':1.5, 'max':1.95},
    {'min':1.95, 'max':100},
]

logger = OtLogger('ot')

data_sets = DivideByPinOdds(logger).get_sorted_game_data_sets(data, dividing_threshold, bookie_list)

# data_to_plot = {
#   '1.0_1.5_home': {
#       'init': {
#            'will_hill': 899,
#            ......
#       }
#       'final': {......}
#       'delta': {......}
#   }
#   '1.5_1.95_home': {......}
#   '1.95_100_home': {......}
# }

data_to_plot = {}

for ds_name, sorted_datas in data_sets.items():

    logger.debug('Processing ' + ds_name + ' with ' + str(len(sorted_datas)) + ' games')

    bookie_scores_by_init_prob = {}
    bookie_scores_by_final_prob = {}
    bookie_scores_by_prob_delta = {}

    # Score every game
    for sorted_data in sorted_datas:
        # print(sorted_data)
        sort_bookies_by_init_prob(bookie_list, bookie_scores_by_init_prob, sorted_data)
        sort_bookies_by_final_prob(bookie_list, bookie_scores_by_final_prob, sorted_data)
        sort_bookies_by_prob_delta(bookie_list, bookie_scores_by_prob_delta, sorted_data)

    pprint.pprint(bookie_scores_by_init_prob)
    pprint.pprint(bookie_scores_by_final_prob)
    pprint.pprint(bookie_scores_by_prob_delta)

    data_to_plot[ds_name] = {
        'init': bookie_scores_by_init_prob,
        'final': bookie_scores_by_final_prob,
        'delta': bookie_scores_by_prob_delta,
    }

plot_scores(bookie_list, data_to_plot)
