import abc


class OddsFetcherInterface(abc.ABC):
    bids = []
    # odds_url_pattern = 'http://1x2.nowscore.com/%game_id%.js'
    odds_url_pattern = 'http://1x2d.win007.com/%game_id%.js'

    def __init__(self, bids):
        self.bids = bids
        pass

    @abc.abstractmethod
    def get_odds(self, gid):
        pass

    @abc.abstractclassmethod
    def get_game_metadata(self, gid):
        pass