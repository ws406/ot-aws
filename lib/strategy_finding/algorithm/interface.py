import abc


class AlgorithmInterface(abc.ABC):

    def __int__(self):
        pass

    # Use algorithm to calculate PNL
    @abc.abstractmethod
    def get_results(self, featured_data: dict):
        pass
