import sys
sys.path.append('/Users/wangjiasun/python/ot')
from win007.observers.strategy_prefer_lower_ranked import Observer as StrategyLowerRanked
from win007.observers.strategy_prefer_much_stronger_team import Observer as StrategyStrongerTeam
from win007.subject.upcoming_games import Subject as UpcomingGamesProcessor
from win007.modules.games_fetcher.open_final_odds_fetcher import OpenFinalOddsFetcher

# These data is used for
bid = [
    80,   # 澳门
    115,  # WH
    281,  # Bet365
    177,  # Pinnacle
]

processor = UpcomingGamesProcessor(OpenFinalOddsFetcher(bid))

# Register all observers which are strategy executors
processor.register_observer(StrategyLowerRanked())
processor.register_observer(StrategyStrongerTeam())

# Get required data from process
games = processor.get_games(5)    # Get games starting in the next 5 mins.

# Notify all observers to action using the games data
processor.notify(games)  # Notify the strategy to handle these games.
