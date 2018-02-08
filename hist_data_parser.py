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
file_header = "/home/wyao/Downloads/Odds/Italian_SerieA-"

def calculate_pre_commission_pnl(odds, prediction, result, goal_diff, dnb_odds):
    if odds < 1.5:
        return 0;
    if odds <= 1.9 and odds >= 1.5:
        if result == prediction:
            return odds - 1
        else:
            return -1
    # Place DNB bet.
    elif odds > 1.9 and odds < 2.8:
        if result == prediction:
            return dnb_odds - 1
        elif result == 'x':
            return 0
        else:
            return -1
    else:
        if goal_diff >= -1:
            return 0.4
        else:
            return -1

#from lib.win007.observers.compare_macau_hkjc.qualification_check import QualificationCheck
from lib.win007.observers.prefer_lower_ranked.qualification_check import QualificationCheck

print("Evaluate hkjc-macau comparison")
file_name = file_header + "2017-2018.json"
right = 0
wrong = 0
miss = 0
profit = 0
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'], ", goal diff is ", match['home_score'] - match['away_score'])
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1
        elif "away-win" in predict:
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'], ", goal diff is ", match['away_score'] - match['home_score'])
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'], away_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1
        #print("Adding match:", league_id, game_id, season, QualificationCheck().is_qualified(match))
#    print("Profit: ", profit)

file_name = file_header + "2016-2017.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'], ", goal diff is ", match['home_score'] - match['away_score'])
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1
        elif "away-win" in predict:
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'], ", goal diff is ", match['away_score'] - match['home_score'])
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'],away_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1

file_name = file_header + "2015-2016.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'], ", goal diff is ", match['home_score'] - match['away_score'])
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1
        elif "away-win" in predict:
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'], ", goal diff is ", match['away_score'] - match['home_score'])
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'], away_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1

file_name = file_header + "2014-2015.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'], ", goal diff is ", match['home_score'] - match['away_score'])
            home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'], home_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1
        elif "away-win" in predict:
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'], ", goal diff is ", match['away_score'] - match['home_score'])
            away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
            local_profit = calculate_pre_commission_pnl(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'],away_dnb_odds)
            profit = profit + local_profit
            if local_profit > 0:
                right = right + 1
            elif local_profit < 0:
                wrong = wrong + 1
            else:
                miss = miss + 1

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
