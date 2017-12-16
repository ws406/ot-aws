from win007.models.games_fetcher import GamesFetcher
from win007.subject.interface import SubjectInterface


class Subject(SubjectInterface):

    games_fetcher = None

    def __init__(self):
        self.games_fetcher = GamesFetcher()
        pass

    # Get games that are taking place in the next 'minutes' minutes
    def get(self, minutes):
        games = self.games_fetcher.get_games()
        # Notify observers
        self.notify()
        return
