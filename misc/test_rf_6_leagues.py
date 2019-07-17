from src.ops.game_predictor.rf_6_leagues import RF6Leagus
import json
game_qualifier = RF6Leagus()

# Put your game data here to test
i = 0
j = 0

# file_name = "./data/football_all_odds_data/English Premier League-2017-2018.json"
file_name = "./test_data.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for data in matches:
        print("gid: ", data['game_id'])
        result = game_qualifier.get_prediction(data)
        print(result)
        if result is not False:
            i += 1
        else:
            j += 1

print (str(i) + " games qualified")
print (str(j) + " games disqualified")
