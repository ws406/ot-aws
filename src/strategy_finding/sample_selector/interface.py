import abc
from src.utils.logger import OtLogger


class SampleSelectorInterface(abc.ABC):

    def __int__(self, logger: OtLogger):
        self.logger = logger

    # Use algorithm to calculate PNL
    @abc.abstractmethod
    def get_selected_games_data(self, raw_data: dict):
        pass
