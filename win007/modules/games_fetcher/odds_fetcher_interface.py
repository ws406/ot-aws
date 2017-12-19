import abc


class OddsFetcherInterface(abc.ABC):
    bid = []
    odds_url_pattern = 'http://www.nowgoal.com/1x2/old_$GAME_ID$.htm'

    def __init__(self, bid):
        self.bid = bid
        pass

    @abc.abstractmethod
    def get_odds(self, gid):
        pass
