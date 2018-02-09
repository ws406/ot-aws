import json

#file_name = "/home/wyao/Downloads/Odds/England_Championship-2017-2018.json"
#file_name = "/home/wyao/Downloads/Odds/England_Championship-2016-2017.json"
#file_name = "/home/wyao/Downloads/Odds/English_Premier_League-2017-2018.json"
#file_name = "/home/wyao/Downloads/Odds/English_Premier_League-2016-2017.json"
#file_name = "/home/wyao/Downloads/Odds/Italian_SerieA-2017-2018.json"
#file_name = "/home/wyao/Downloads/Odds/Italian_SerieA-2016-2017.json"
#file_name = "/home/wyao/Downloads/Odds/Italian_SerieA-2015-2016.json"
#file_name = "/home/wyao/Downloads/Odds/Italian_SerieA-2014-2015.json"
#file_name = "/home/wyao/Downloads/Odds/Italian_SerieB-2017-2018.json"
#file_name = "/home/wyao/Downloads/Odds/Italian_SerieB-2016-2017.json"
#file_header = "/home/wyao/Downloads/Odds/Italian_SerieA-"
#file_header = "/home/wyao/Downloads/Odds/England_Championship-"
file_header = "/home/wyao/Downloads/Odds/English_Premier_League-"

betOneSide = 1.5
betDnb = 1.8
betNo = 2.5

def calculate_pre_commission_pnl(odds, prediction, result, goal_diff, dnb_odds, double_chance_odds):
    if odds < betOneSide:
        return 0;
    if odds < betDnb and odds >= betOneSide:
        if result == prediction:
            return odds - 1
        else:
            return -1
    # Place DNB bet.
    elif odds >= betDnb and odds < betNo:
        if double_chance_odds >= 1.3:
            if result == prediction or result == 'x':
                return double_chance_odds - 1
            else:
                return -1
        else:
            if result == prediction:
                return dnb_odds - 1
            elif result == 'x':
                return 0
            else:
                return -1
    else:
        #return 0
        if goal_diff > -1:
            return 0.3
        elif goal_diff == -1:
            return 0;
        else:
            return -1

from lib.win007.observers.compare_macau_hkjc.qualification_check import QualificationCheck
#from lib.win007.observers.prefer_lower_ranked.qualification_check import QualificationCheck

print("Evaluate hkjc-macau comparison")
file_name = file_header + "2017-2018.json"
right = 0
wrong = 0
miss = 0
profit = 0
predict_result = 'miss'
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        cur_round = match['rounds']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds, home_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
                predict_result = 'wrong'
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'],
                ", goal diff is ", match['home_score'] - match['away_score'], ", prediction is ", predict_result, ", round is ", cur_round)
        elif "away-win" in predict:
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'], away_dnb_odds, away_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
                predict_result = 'wrong'
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'],
                ", goal diff is ", match['away_score'] - match['home_score'], ", prediction is ", predict_result, ", round is ", cur_round)
        #print("Adding match:", league_id, game_id, season, QualificationCheck().is_qualified(match))
#    print("Profit: ", profit)

file_name = file_header + "2016-2017.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        cur_round = match['rounds']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds, home_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
                predict_result = 'wrong'
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'],
                ", goal diff is ", match['home_score'] - match['away_score'], ", prediction is ", predict_result, ", round is ", cur_round)
        elif "away-win" in predict:
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'], away_dnb_odds, away_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
                predict_result = 'wrong'
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'],
                ", goal diff is ", match['away_score'] - match['home_score'], ", prediction is ", predict_result, ", round is ", cur_round)

file_name = file_header + "2015-2016.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        cur_round = match['rounds']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds, home_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
                predict_result = 'wrong'
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'],
                ", goal diff is ", match['home_score'] - match['away_score'], ", prediction is ", predict_result, ", round is ", cur_round)
        elif "away-win" in predict:
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'], away_dnb_odds, away_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
                predict_result = 'wrong'
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'],
                ", goal diff is ", match['away_score'] - match['home_score'], ", prediction is ", predict_result, ", round is ", cur_round)

file_name = file_header + "2014-2015.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        cur_round = match['rounds']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds, home_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'],
                ", goal diff is ", match['home_score'] - match['away_score'], ", prediction is ", predict_result, ", round is ", cur_round)
        elif "away-win" in predict:
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'],away_dnb_odds, away_dc_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
                predict_result = 'right'
            elif local_profit < 0:
                wrong = wrong + 1
                predict_result = 'wrong'
            else:
                miss = miss + 1
                predict_result = 'miss'
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'],
                ", goal diff is ", match['away_score'] - match['home_score'], ", prediction is ", predict_result, ", round is ", cur_round)

total_games = right + wrong + miss
print("Profit: ", profit, ", right is ", right / total_games, ", wrong is ", wrong / total_games, ", miss is ", miss / total_games, ", total games ", total_games)

#print("Evaluate prefer lower rank team comparison")
#from lib.win007.observers.prefer_lower_ranked.qualification_check import QualificationCheck
#profit = 0
#with open(file_name) as json_file:
#    for match in matches:
#        game_id = match['game_id']
#        predict = QualificationCheck().is_qualified(match)
#        if "disqualified" in predict:
#            continue
#        elif "home-win" in predict:
#            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'], ", goal diff is ", match['home_score'] - match['away_score'])
#            profit = profit + calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'])
#        elif "away-win" in predict:
#            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'], ", goal diff is ", match['away_score'] - match['home_score'])
#            profit = profit + calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'])
#    print("Profit: ", profit)
