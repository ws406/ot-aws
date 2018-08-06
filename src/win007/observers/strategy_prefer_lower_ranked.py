from src.win007.observers.interface import ObserverInterface
from src.win007.observers.prefer_lower_ranked.qualification_check import QualificationCheck


class PreferLowerRankedObserver(ObserverInterface):

    qualification_checker = None

    def __init__(self):
        super(PreferLowerRankedObserver, self).__init__()
        self.qualification_checker = QualificationCheck()
        pass

    def observer_run(self, data):
        print("Running strategy: lower ranked team with low odds")
        print("Predicting " + str(len(data)) + " games:")
        for game_id, game_data in data.items():
            print("\tPrediction for game " + str(game_id) + " is: " + self.qualification_checker.is_qualified(game_data))
        pass
