import json
from lib.win007.observers.compare_macau_hkjc.qualification_check import QualificationCheck
#import decimal

#file_name = "/home/wyao/Downloads/Odds/England_Championship-2017-2018.json"
#file_name = "/home/wyao/Downloads/Odds/English_Premier_League-2017-2018.json"
file_name = "/home/wyao/Downloads/Odds/Italian_SerieA-2017-2018.json"
#file_name = "/home/wyao/Downloads/Odds/Italian_SerieB-2017-2018.json"

def Calculate_odds(odds, prediction, result, goal_diff):
    if odds < 1.6:
        if result == prediction:
            return odds - 1
        else:
            return -1
    elif odds >= 1.6 and odds < 3:
        if result == prediction:
            return odds * 0.8 - 1
        elif result == 'x':
            return 0
        else:
            return -1
    else:
        if goal_diff >= -1:
            return odds * 0.4 - 1
        else:
            return -1

print("Evaluate hkjc-macau comparison")
profit = 0
with open(file_name) as json_file:
    matches = json.load(json_file)
    for match in matches:
        game_id = match['game_id']
        league_id = match['league_id']
        season = match['season']
        match['probabilities'] = match['probability']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'], ", goal diff is ", match['home_score'] - match['away_score'])
            profit = profit + Calculate_odds(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'])
        elif "away-win" in predict:
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'], ", goal diff is ", match['away_score'] - match['home_score'])
            profit = profit + Calculate_odds(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'])
        #print("Adding match:", league_id, game_id, season, QualificationCheck().is_qualified(match))
    print("Profit: ", profit)

print("Evaluate prefer lower rank team comparison")
from lib.win007.observers.prefer_lower_ranked.qualification_check import QualificationCheck
right = 0
wrong = 0
profit = 0
with open(file_name) as json_file:
    for match in matches:
        match['probabilities'] = match['probability']
        predict = QualificationCheck().is_qualified(match)
        if "disqualified" in predict:
            continue
        elif "home-win" in predict:
            print("Game: ", game_id, "predicted home win, odds is ", match['odds']['bet365']['final']['1'], ", result is ", match['result'], ", goal diff is ", match['home_score'] - match['away_score'])
            profit = profit + Calculate_odds(match['odds']['bet365']['final']['1'], '1', match['result'], match['home_score'] - match['away_score'])
        elif "away-win" in predict:
            print("Game: ", game_id, "predicted away win, odds is ", match['odds']['bet365']['final']['2'], ", result is ", match['result'], ", goal diff is ", match['away_score'] - match['home_score'])
            profit = profit + Calculate_odds(match['odds']['bet365']['final']['2'], '2', match['result'], match['away_score'] - match['home_score'])
    print("Profit: ", profit)
