import sys
sys.path.append('/Users/wangjiasun/python/ot')
from win007.observers.strategy_prefer_lower_ranked import Observer as StrategyLowerRanked
from win007.observers.strategy_prefer_much_stronger_team import Observer as StrategyStrongerTeam
from win007.subject.upcoming_games import Subject as UpcomingGamesProcessor
from win007.modules.games_fetcher.open_final_odds_fetcher import OpenFinalOddsFetcher
from pprint import pprint

# These data is used for
bids = {
    80: "macau_slot",   # 澳门
    115: "will_hill",  # WH
    281: "bet365",  # Bet365
    177: "pinnacle",  # Pinnacle
}

minutes = 1240
league_ids = [
    34,  # IT1
    40,  # IT2

    36,  # EPL
    37,  # ENC
    39,  # EFL1
    35,  # EFL2

    31,  # ES1
    33,  # ES2

    8,   # GE1
    9,   # GE2

    11,  # FR1
    12,  # FR2

    16,  # HO1
    17,  # HO2

    25,  # JAP1
    284, # JAP2

    4,   # BRA1
    358, # BRA2

    23,  # POTG1
    29,  # SCOT1
    30,  # TUR1
    5,   # BEL1
    26,  # SWE1
    22,  # NOR1
    27,  # SW1
    10,  # RUS1
    30,  # TUR1
    2,   # ARG1
    21,  # USA1
    415, # CHILE1
    140, # MEX1
    50,  # CHN1
    15,  # KOR1
    273, # AUS
    292, # TEST
]

print("Start...")
processor = UpcomingGamesProcessor(OpenFinalOddsFetcher(bids))

# Register all observers which are strategy executors
processor.register_observer(StrategyLowerRanked())
processor.register_observer(StrategyStrongerTeam())

# Get required data from process
print("Getting games that will start in the next " + str(minutes) + " mins and from "
      + str(len(league_ids)) + " leagues..")
games = processor.get_games(minutes, league_ids)    # Get games starting in the next 5 mins.
# pprint(games)
print(str(len(games)) + " games found")

# Notify all observers to action using the games data
processor.notify(games)  # Notify the strategy to handle these games.
