from typing import List


class GameMainBookiesOdds:

    bookies_odds = None

    def __init__(self, game_bookies_odds: List[GameBookieOdds]):
        self.bookies_odds = game_bookies_odds
        pass


class GameBookieOdds:

    bookie_name = None
    odds_type = None
    odds_1 = None
    odds_x = None
    odds_2 = None

    def __init__(
        self,
        bookie_name,
        odds_type,
        odds_1,
        odds_x,
        odds_2
    ):
        self.bookie_name = bookie_name
        self.odds_type = odds_type
        self.odds_1 = odds_1
        self.odds_x = odds_x
        self.odds_2 = odds_2
