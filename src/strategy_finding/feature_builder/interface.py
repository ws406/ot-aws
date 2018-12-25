import abc
from src.utils.logger import OtLogger


class FeatureBuilderInterface(abc.ABC):

    def __int__(self, logger: OtLogger):
        self.logger = logger
        pass

    # Use algorithm to calculate PNL
    @abc.abstractmethod
    def get_features(self, labelled_data: list):
        pass
