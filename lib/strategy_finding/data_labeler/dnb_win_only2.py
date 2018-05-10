from lib.strategy_finding.data_labeler.interface import DataLabelerInterface
from lib.win007.observers.same_direction.qualification_check import QualificationCheck

class DnbWinOnly2(DataLabelerInterface):

    def label_data(self, data: list):
        print("Running match labeler - DnbWinOnly2")

        for match in data:

            prediction = match['prediction']

            if prediction == QualificationCheck.prediction_home_win:
                match['home_away'] = '1'
                match['result'] = 1
            elif prediction == QualificationCheck.prediction_away_win:
                match['home_away'] = '2'
                match['result'] = 2
            else:
                raise ValueError('match prediction is not expected. Expect home_win or away_won, but got ' + prediction)

        return data
