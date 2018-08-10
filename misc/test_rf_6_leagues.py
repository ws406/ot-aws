from src.ops.game_qualifier.rf_6_leagues import RF6Leagus
import json
game_qualifier = RF6Leagus()

# Put your game data here to test
i = 0
j = 0

file_name = "/home/wyao/workspace/ot-aws/data/football_all_odds_data/English Premier League-2016-2017.json"
with open(file_name) as json_file:
    matches = json.load(json_file)
    for data in matches:
        result = game_qualifier.is_game_qualified(data)
        print(result)
        if result is not False:
            i += 1
        else:
            j += 1

print (str(i) + " games qualified")
print (str(j) + " games disqualified")