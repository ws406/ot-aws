from win007.observers.interface import ObserverInterface


class Observer(ObserverInterface):

    def __init__(self):
        super(Observer, self).__init__()
        pass

    def observer_run(self, data):
        print("Running strategy: prefer much stronger team")
        # print(data)
        pass
