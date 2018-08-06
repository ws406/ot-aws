import abc


class FeatureBuilderInterface(abc.ABC):

    def __int__(self):
        pass

    # Use algorithm to calculate PNL
    @abc.abstractmethod
    def get_features(self, labelled_data: list):
        pass
