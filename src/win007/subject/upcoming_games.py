from src.win007.modules.games_fetcher.games_fetcher import GamesFetcher
from src.win007.subject.interface import SubjectInterface
from src.win007.modules.games_fetcher.football_odds_fetcher.abstract_odds_fetcher import AbstractOddsFetcher


class Subject(SubjectInterface):

    games_fetcher = None

    def __init__(self, odds_fetcher: AbstractOddsFetcher):
        self.games_fetcher = GamesFetcher(odds_fetcher)
        pass

    # Get games that are taking place in the next 'minutes' minutes
    def get_games(self, minutes, league_ids):
        if league_ids is None:
            games = self.games_fetcher.get_games_by_kickoff(minutes)
        else:
            games = self.games_fetcher.get_games_by_kickoff_and_league(minutes, league_ids)
        return games
