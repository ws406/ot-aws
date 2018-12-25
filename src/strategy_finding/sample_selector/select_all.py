from src.strategy_finding.sample_selector.interface import SampleSelectorInterface
from src.utils.logger import OtLogger


class SelectAll(SampleSelectorInterface):

    def __init__(self, logger: OtLogger):
        super().__int__(logger)

    def get_selected_games_data(self, raw_data: dict):
        self.logger.debug("Running game selector - SelectAll")
        self.logger.debug(str(len(raw_data))+ " matches selected for analysis.")
        return raw_data
