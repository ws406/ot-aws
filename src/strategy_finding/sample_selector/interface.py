import abc


class SampleSelectorInterface(abc.ABC):

    def __int__(self):
        pass

    # Use algorithm to calculate PNL
    @abc.abstractmethod
    def get_selected_games_data(self, raw_data: dict):
        pass
