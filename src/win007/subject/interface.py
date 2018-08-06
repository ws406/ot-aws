import abc
from src.win007.observers.interface import ObserverInterface


class SubjectInterface(abc.ABC):

    __observers = []

    def register_observer(self, observer: ObserverInterface):
        self.__observers.append(observer)

    def notify(self, data):
        for o in self.__observers:
            o.observer_run(data)
