import abc


class ObserverInterface(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def observer_run(self):
        pass
