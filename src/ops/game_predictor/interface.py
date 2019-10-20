import abc


class GamePredictorInterface(abc.ABC):

    # TODO: use avro schema
    @abc.abstractmethod
    def get_prediction(self, data, profit_margin):
        pass
