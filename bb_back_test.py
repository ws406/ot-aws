import json
import glob
from src.utils.logger import OtLogger
from src.ops.game_predictor.bb_blended_true_odds import TrueOdds


############# Configuration ##################
# Get all data from file(s)
data_files = glob.glob("./data/basketball_all_odds_data/National Basketball Association-2019-2020.json")

bids = {
    281: "bet365",  # Bet365
    177: "pinnacle",  # Pinnacle
    81:  "betvictor",  # Bet Victor
    80: "macau_slot",  # Macao Slot
    90: "easybet",  # EasyBet
    545: "sb",
    82: "ladbroke",
    474: "sbobet",
    115: "will_hill",  # WH
    432: "hkjc",  # HKJC
    # 104: "interwetten"  # Interwetten
    156: "betfred",
    110: "snai",
    463: "betclick",
    167: "skybet",
}

############# Functioning ##################
print(len(data_files), ' files to process...')
data = []
for f in data_files:
    print('processing file - ', f)
    with open (f) as f_data:
        tmp = json.load(f_data)
        data += tmp
    # break
print (len(data), ' games to process')


logger = OtLogger('ot')
gamePredictor = TrueOdds (logger)

bf_commission = 0.02


def rank(data):
    results_matrix = {}
    results_matrix['number_of_games'] = 0
    move_on = False
    max_odds = 3.5

    for game in data:

        # print(game['game_id'])
        # 1: lowest odds, 3: highest odds

        profit_margin = 0
        while profit_margin <= 10:
            # print("profit_margin: ", profit_margin/100)
            if profit_margin not in results_matrix:
                results_matrix[profit_margin] = {
                    'pnl_1': 0,
                    'pnl_2': 0,
                    'pnl_12': 0,
                }
            betting_details = gamePredictor.get_prediction(game, profit_margin/100)

            if betting_details is False:
                logger.log ("--- Game " + str(game['game_id']) + " is not qualified. ---")
                move_on = True
                break

            # sorted_odds is like [('2', 1.4), ('1', 2.1), ('x', 3)]
            sorted_odds = sorted_x = sorted(betting_details['true_odds'].items(), key=lambda kv: kv[1])
            odds_to_bet_1 = sorted_odds[0][1]
            result_to_bet_1 = sorted_odds[0][0]

            odds_to_bet_2 = sorted_odds[1][1]
            result_to_bet_2 = sorted_odds[1][0]

            if odds_to_bet_2 > max_odds or odds_to_bet_1 > max_odds:
                logger.log ("--- Game " + str(game['game_id']) + " is not qualified. Odds too high ---")
                move_on = True
                break

            if game['home_score'] > game['away_score']:
                result = '1'
            else:
                result = '2'

            if result_to_bet_1 == result:
                results_matrix[profit_margin]['pnl_1'] = \
                    results_matrix[profit_margin]['pnl_1'] + (odds_to_bet_1 - 1) * (1 - bf_commission)
                results_matrix[profit_margin]['pnl_2'] = results_matrix[profit_margin]['pnl_2'] - 1
            else:
                results_matrix[profit_margin]['pnl_1'] = results_matrix[profit_margin]['pnl_1'] - 1
                results_matrix[profit_margin]['pnl_2'] = \
                    results_matrix[profit_margin]['pnl_2'] + (odds_to_bet_2 - 1) * (1 - bf_commission)

            results_matrix[profit_margin]['pnl_12'] = results_matrix[profit_margin]['pnl_1'] + results_matrix[profit_margin]['pnl_2']

            profit_margin += 1
        if move_on:
            move_on = False
            continue
        else:
            results_matrix['number_of_games'] += 1

    logger.log(results_matrix)

rank(data)
# TODO:
# 1. filter by season
# 2. filter by league
# 3. build csv file
