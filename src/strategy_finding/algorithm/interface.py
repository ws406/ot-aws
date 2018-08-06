import abc
import numpy as np

class AlgorithmInterface(abc.ABC):

    def __int__(self):
        pass

    # Use algorithm to calculate PNL
    @abc.abstractmethod
    def get_results(self, header, featured_data: np.array):
        pass
