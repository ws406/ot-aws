import abc

class DataLabelerInterface(abc.ABC):

    def __int__(self):
        pass

    @abc.abstractmethod
    def label_data(self, data: list):
        pass
