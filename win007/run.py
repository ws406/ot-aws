import sys
sys.path.append('/Users/wangjiasun/python/ot')
from win007.observers.strategy_prefer_lower_ranked import Observer as StrategyLowerRanked
from win007.subject.upcoming_games import Subject as UpcomingGamesProcessor
from win007.modules.games_fetcher.open_final_odds_fetcher import OpenFinalOddsFetcher

bid = [
    80,   # 澳门
    115,  # WH
    281,  # Bet365
    177,  # Pinnacle
]

processor = UpcomingGamesProcessor(OpenFinalOddsFetcher(bid))
processor.register_observer(StrategyLowerRanked())
games = processor.get_games(5)    # Get games starting in the next 5 mins.
processor.notify(games)  # Notify the strategy to handle these games.
