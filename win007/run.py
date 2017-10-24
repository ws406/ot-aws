import sys

sys.path.append('/Users/wangjiasun/python/ot')

from win007.observers.strategy1 import Observer as Strategy1
from win007.subject.upcoming_games import Subject as UpcomingGamesProcessor


Strategy = Strategy1()
processor = UpcomingGamesProcessor()
processor.register_observer(Strategy)
processor.get(5)    # Get games starting in the next 5 mins.
processor.notify()  # Notify the strategy to handle these games.
