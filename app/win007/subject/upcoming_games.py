from win007.modules.games_fetcher.games_fetcher import GamesFetcher
from win007.subject.interface import SubjectInterface
from win007.modules.games_fetcher.odds_fetcher_interface import OddsFetcherInterface


class Subject(SubjectInterface):

    games_fetcher = None

    def __init__(self, odds_fetcher: OddsFetcherInterface):
        self.games_fetcher = GamesFetcher(odds_fetcher)
        pass

    # Get games that are taking place in the next 'minutes' minutes
    def get_games(self, minutes, league_ids):
        games = self.games_fetcher.get_games(minutes, league_ids)
        return games
