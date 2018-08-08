import abc


class GameQualifierInterface(abc.ABC):

    # TODO: use avro schema
    @abc.abstractmethod
    def is_game_qualified(self, data):
        pass
