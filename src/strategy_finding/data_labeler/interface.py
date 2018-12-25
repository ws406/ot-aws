import abc
from src.utils.logger import OtLogger


class DataLabelerInterface(abc.ABC):

    def __int__(self, logger:OtLogger):
        self.logger = logger
        pass

    @abc.abstractmethod
    def label_data(self, data: list):
        pass
