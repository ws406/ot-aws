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

    # Get the number of columns in the data set
    @abc.abstractmethod
    def get_num_cols(self):
        pass

    # Get the headers of the dataset
    @abc.abstractmethod
    def get_header(self):
        pass
