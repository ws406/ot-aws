from lib.win007.observers.interface import ObserverInterface
from lib.win007.observers.compare_macau_hkjc.qualification_check import QualificationCheck


class Observer(ObserverInterface):

    qualification_checker = None

    def __init__(self):
        super(Observer, self).__init__()
        self.qualification_checker = QualificationCheck()
        pass

    def observer_run(self, data):
        print("Running strategy: compare macau and hkjc odds")
        print("Predicting " + str(len(data)) + " games:")
        for game_id, game_data in data.items():
            print("\tPrediction for game " + str(game_id) + " is: " + self.qualification_checker.is_qualified(game_data))
        pass
