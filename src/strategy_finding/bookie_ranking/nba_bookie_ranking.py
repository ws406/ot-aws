import json
import glob
import collections
import pprint
import matplotlib.pyplot as plt
import pylab


def plot_scores(bookie_list, scores):

    cm = pylab.get_cmap ('tab20')
    i = 0
    for bookie_name in bookie_list:
        color = cm (1. * i / len(bookie_list))
        if bookie_name not in scores.keys():
            continue
        plt.plot(scores[bookie_name].keys(), scores[bookie_name].values(), color=color, label=bookie_name)
        i += 1

    plt.legend()
    plt.show()


# Order probs and odds by timestamp by small (earliest) to big (latest)
def sort_game_data_timestamp(bookie_list, game_data):
    probabilities = game_data['probabilities']
    odds = game_data['odds']
    for b_name in bookie_list:
        game_data['probabilities'][b_name] = collections.OrderedDict(sorted(probabilities[b_name].items(), reverse=False))
        game_data['odds'][b_name] = collections.OrderedDict(sorted(odds[b_name].items(), reverse=False))
    return game_data


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
    season = sorted_data ['season']
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
data_files = glob.glob("C:\\Users\wsun\\Documents\\projects\\ot-aws\\data\\basketball_all_odds_data\\*.json")
# data_files = glob.glob("C:\\Users\wsun\\Documents\\projects\\ot-aws\\src\\strategy_finding\\bookie_ranking\\test.json")
# data_files = glob.glob("C:\\Users\wsun\\Documents\\projects\\ot-aws\\test.json")
bookie_list = [
    "pinnacle",  # Pinnacle
    "will_hill",  # WH
    # "coral",
    "Expekt",
    "vcbet",  # VcBet
    "SNAI",
    "bet365",  # Bet365
    "betvictor",  # VcBet2
    # "Macauslot",
    "BWin",
    # "ChinaSlot",
    "SB",
    "Betfair",
    # "5Dimes",
    # "Centrebet",
    "easybet",
    "ladbroke",
    # "marathon",
    # "marathonbet",
    "skybet",
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

# The scores look like this
# {
#     'vcbet': {'2014-2015': 524,
#               '2015-2016': 940,
#               '2016-2017': 1090,
#               '2017-2018': 1490,
#               '2018-2019': 312},
#     'will_hill': {'2014-2015': 565,
#                   '2015-2016': 1091,
#                   '2016-2017': 1246,
#                   '2017-2018': 1210,
#                   '2018-2019': 256}
# }
bookie_scores_by_init_prob = {}
bookie_scores_by_final_prob = {}
bookie_scores_by_prob_delta = {}

for game_data in data:
    try:
        sorted_data = sort_game_data_timestamp(bookie_list, game_data)
    except KeyError as ke:
        print(ke)
        continue
    # print(sorted_data)
    sort_bookies_by_init_prob(bookie_list, bookie_scores_by_init_prob, sorted_data)
    sort_bookies_by_final_prob(bookie_list, bookie_scores_by_final_prob, sorted_data)
    sort_bookies_by_prob_delta(bookie_list, bookie_scores_by_prob_delta, sorted_data)

pprint.pprint(bookie_scores_by_init_prob)
pprint.pprint(bookie_scores_by_final_prob)
pprint.pprint(bookie_scores_by_prob_delta)

plot_scores(bookie_list, bookie_scores_by_init_prob)
plot_scores(bookie_list, bookie_scores_by_final_prob)
plot_scores(bookie_list, bookie_scores_by_prob_delta)

#### Conclusion ########
# Most accurate initial and final probs are from: easybet, will_hill and pinnacle
# Least accurate initial and final probs is from: ladbrokes
# Features selection ideas:
#  - final_easy_bet
#  - delta_easy_bet
#  - final_easy_bet - final_ladbrokes