import sys

sys.path.append('/Users/wangjiasun/python/ot')

from win007.observers.strategy_prefer_lower_ranked import Observer as StrategyLowerRanked
from win007.subject.upcoming_games import Subject as UpcomingGamesProcessor


processor = UpcomingGamesProcessor()
processor.register_observer(StrategyLowerRanked())
processor.get(filter())    # Get games starting in the next 5 mins.
processor.notify()  # Notify the strategy to handle these games.
