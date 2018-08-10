from src.ops.game_qualifier.rf_6_leagues import RF6Leagus
import json
game_qualifier = RF6Leagus()

# Put your game data here to test
data = json.loads(open('./data/football_all_odds_data/English Premier League-2016-2017.json').read())
i = 0
j = 0
for game in data:
	result = game_qualifier.is_game_qualified(data)
	print(result)
	if result is not False:
		i += 1
	else:
		j += 1

print (str(i) + " games qualified")
print (str(j) + " games disqualified")