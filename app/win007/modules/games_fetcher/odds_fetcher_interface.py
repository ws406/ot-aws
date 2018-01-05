import abc


class OddsFetcherInterface(abc.ABC):
    bids = []
    odds_url_pattern = 'http://1x2.nowscore.com/$GAME_ID$.js'

    def __init__(self, bids):
        self.bids = bids
        pass

    @abc.abstractmethod
    def get_odds(self, gid):
        pass
