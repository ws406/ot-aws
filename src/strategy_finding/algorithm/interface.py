import abc
import numpy as np
from src.utils.logger import OtLogger


class AlgorithmInterface(abc.ABC):

    def __int__(self, logger: OtLogger):
        self.logger = logger

    # Use algorithm to calculate PNL
    @abc.abstractmethod
    def get_results(self, header, featured_data: np.array):
        pass
