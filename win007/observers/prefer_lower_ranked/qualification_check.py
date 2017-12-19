#from win007.entities.game_odds import GameMainBookiesOdds
import json
from collections import defaultdict

'''
class decision_maker:
    def __init__(self):
        pass

    # This function takes the input data and makes a decision about whether this game is
    # qualified or not based on our strategy.
    #
    # The input data structure is illustrated in data_example.json file
    # The return is one of the three possibilities:
    # 1. None: nothing is qualified
    # 2. "1": home team is preferred
    # 3. "2": awa team is preferred
    def which_is_qualified(self, odds: GameMainBookiesOdds):
        odds['odds']['bookie_name']

        pass
'''
json_file = open("../data_example.json", "r").read()
my_json_dict = json.loads(json_file)

totalOdds = defaultdict(list)

for data in my_json_dict['odds'] : 
  if data['bookie_name'] == "macau_slot":
    if data['odds_type'] == "original":
      totalOdds['macau_0'] = data
    if data['odds_type'] == "final":
      totalOdds['macau_f'] = data
  elif data['bookie_name'] == "will_hill":
    if data['odds_type'] == "original":
      totalOdds['wh_o'] = data
    if data['odds_type'] == "final":
      totalOdds['wh_f'] = data
  elif data['bookie_name'] == "bet365":
    if data['odds_type'] == "original":
      totalOdds['bet365_o'] = data
    if data['odds_type'] == "final":
      totalOdds['bet365_f'] = data
  elif data['bookie_name'] == "pinnacle":
    if data['odds_type'] == "original":
      totalOdds['pin_o'] = data
    if data['odds_type'] == "final":
      totalOdds['pin_f'] = data
    
prediction = None

# 1. check ranking condition: to qualify, the team that ranks higher needs to have winning odds that is lower than 1.9
# Away team ranks lower or only one position higher than home team. E.g. home ranks 3, away ranks 2 or 4 or lower.
if (my_json_dict['away_team_rank'] - my_json_dict['home_team_rank'] > -1 ) and totalOdds['macau_o']['2'] < 1.9 :
    prediction = 2

# Home team ranks lower or only one position higher than away team. E.g. away ranks 3, home ranks 2 or 4 or lower.
elif (my_json_dict['home_team_rank'] - my_json_dict['away_team_rank'] > -1 ) and totalOdds['macau_o']['1'] < 1.9 :
    prediction = 1


# 2. Predict by odds trend. If all-final-odds is smaller than all-original-odds, predict that result.
if prediction == 2 and \
    totalOdds['macau_o']['1'] < totalOdds['macau_f']['1'] and totalOdds['macau_o']['2'] > totalOdds['macau_f']['2'] and \
    totalOdds['wh_o']['1'] < totalOdds['wh_f']['1'] and totalOdds['wh_o']['2'] > totalOdds['wh_f']['2'] and \
    totalOdds['ladbrokes1']['1'] < totalOdds['ladbrokes2']['1'] and totalOdds['ladbrokes1']['2'] > totalOdds['ladbrokes2']['2'] and \
    totalOdds['bet365_o']['1'] < totalOdds['bet365_f']['1'] and totalOdds['bet365_o']['2'] > totalOdds['bet365_f']['2'] and \
    totalOdds['pin_o']['1'] < totalOdds['pin_f']['1'] and totalOdds['pin_o']['2'] > totalOdds['pin_f']['2'] and \
    totalOdds['inter1']['1'] < totalOdds['inter2']['1'] and totalOdds['inter1']['2'] > totalOdds['inter2']['2'] :

    prediction = 2

elif prediction == 1 and \
    totalOdds['macau_o']['1'] > totalOdds['macau_f']['1'] and totalOdds['macau_o']['2'] < totalOdds['macau_f']['2'] and \
    totalOdds['wh_o']['1'] > totalOdds['wh_f']['1'] and totalOdds['wh_o']['2'] < totalOdds['wh_f']['2'] and \
    totalOdds['ladbrokes1']['1'] > totalOdds['ladbrokes2']['1'] and totalOdds['ladbrokes1']['2'] < totalOdds['ladbrokes2']['2'] and \
    totalOdds['bet365_o']['1'] > totalOdds['bet365_f']['1'] and totalOdds['bet365_o']['2'] < totalOdds['bet365_f']['2'] and \
    totalOdds['pin_o']['1'] > totalOdds['pin_f']['1'] and totalOdds['pin_o']['2'] < totalOdds['pin_f']['2'] :

    prediction = 1

#print prediction


'''
for data in totalOdds.items():
  print data
'''
