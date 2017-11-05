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
    # The return is one of the three possibilites:
    # 1. None: nothing is qualified
    # 2. "1": home team is preferred
    # 3. "2": awa team is preferred
    def which_is_qualified(self, odds: GameMainBookiesOdds):
        odds['odds']['bookie_name']

        pass
'''
json_file = open("/home/wyao/Downloads/sunwangjia/data_example.json", "r").read()
my_json_dict = json.loads(json_file)

totalOdds = defaultdict(list)

for data in my_json_dict['odds'] : 
  if data['bookie_name'] == "macau_slot":
    if data['odds_type'] == "original":
      totalOdds['macau1'] = data
    if data['odds_type'] == "final":
      totalOdds['macau2'] = data
  elif data['bookie_name'] == "will_hill":
    if data['odds_type'] == "original":
      totalOdds['wh1'] = data
    if data['odds_type'] == "final":
      totalOdds['wh2'] = data
  elif data['bookie_name'] == "ladbrokes":
    if data['odds_type'] == "original":
      totalOdds['ladbrokes1'] = data
    if data['odds_type'] == "final":
      totalOdds['ladbrokes2'] = data
  elif data['bookie_name'] == "bet365":
    if data['odds_type'] == "original":
      totalOdds['bet3651'] = data
    if data['odds_type'] == "final":
      totalOdds['bet3652'] = data
  elif data['bookie_name'] == "pinnacle":
    if data['odds_type'] == "original":
      totalOdds['pi1'] = data
    if data['odds_type'] == "final":
      totalOdds['pi2'] = data
  elif data['bookie_name'] == "interwetten":
    if data['odds_type'] == "original":
      totalOdds['inter1'] = data
    if data['odds_type'] == "final":
      totalOdds['inter2'] = data
    
prediction = None
if totalOdds['macau1']['1'] < totalOdds['macau2']['1'] and totalOdds['macau1']['2'] > totalOdds['macau2']['2'] and \
  totalOdds['wh1']['1'] < totalOdds['wh2']['1'] and totalOdds['wh1']['2'] > totalOdds['wh2']['2'] and \
  totalOdds['ladbrokes1']['1'] < totalOdds['ladbrokes2']['1'] and totalOdds['ladbrokes1']['2'] > totalOdds['ladbrokes2']['2'] and \
  totalOdds['bet3651']['1'] < totalOdds['bet3652']['1'] and totalOdds['bet3651']['2'] > totalOdds['bet3652']['2'] and \
  totalOdds['pi1']['1'] < totalOdds['pi2']['1'] and totalOdds['pi1']['2'] > totalOdds['pi2']['2'] and \
  totalOdds['inter1']['1'] < totalOdds['inter2']['1'] and totalOdds['inter1']['2'] > totalOdds['inter2']['2'] :
  prediction = 2
elif totalOdds['macau1']['1'] > totalOdds['macau2']['1'] and totalOdds['macau1']['2'] < totalOdds['macau2']['2'] and \
  totalOdds['wh1']['1'] > totalOdds['wh2']['1'] and totalOdds['wh1']['2'] < totalOdds['wh2']['2'] and \
  totalOdds['ladbrokes1']['1'] > totalOdds['ladbrokes2']['1'] and totalOdds['ladbrokes1']['2'] < totalOdds['ladbrokes2']['2'] and \
  totalOdds['bet3651']['1'] > totalOdds['bet3652']['1'] and totalOdds['bet3651']['2'] < totalOdds['bet3652']['2'] and \
  totalOdds['pi1']['1'] > totalOdds['pi2']['1'] and totalOdds['pi1']['2'] < totalOdds['pi2']['2'] and \
  totalOdds['inter1']['1'] > totalOdds['inter2']['1'] and totalOdds['inter1']['2'] < totalOdds['inter2']['2'] :
  prediction = 1

print prediction

if my_json_dict['home_team_rank'] > my_json_dict['away_team_rank'] and totalOdds['macau2']['2'] < 1.9 and prediction == 2 :
  prediction = 2
elif my_json_dict['home_team_rank'] < my_json_dict['away_team_rank'] and totalOdds['macau2']['1'] < 1.9 and prediction == 1 :
  prediction = 1
else
  prediction = None

print prediction

'''
for data in totalOdds.items():
  print data
'''
