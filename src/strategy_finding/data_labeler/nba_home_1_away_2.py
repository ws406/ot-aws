# Simply data labeller - home_win is 1 & away_win is 2
from src.strategy_finding.data_labeler.interface import DataLabelerInterface
from src.utils.logger import OtLogger


class NBAHome1Away2(DataLabelerInterface):

    def __init__(self, logger: OtLogger):
        super().__int__(logger)

    def label_data(self, data: list):
        self.logger.debug("Running match labeler - NBA-Home-1-Away-2")
        # for game_data in data:
        #     game_data['result'] = 1 if game_data['home_score'] > game_data['away_score'] else 2
        return data
