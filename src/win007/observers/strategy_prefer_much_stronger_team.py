from src.win007.observers.interface import ObserverInterface


class PreferStrongerTeamObserver(ObserverInterface):

    def __init__(self):
        super(PreferStrongerTeamObserver, self).__init__()
        pass

    def observer_run(self, data):
        print("Running strategy: prefer much stronger team")
        # print(data)
        pass
