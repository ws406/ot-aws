from lib.strategy_finding.data_labeler.interface import DataLabelerInterface
from lib.win007.observers.same_direction.qualification_check import QualificationCheck

class DnbWinOnly(DataLabelerInterface):

    def label_data(self, matches: list):
        print("Running match labeler - DnbWinOnly")

        for match in matches:

            prediction = match['prediction']

            if prediction == QualificationCheck.prediction_home_win:
                match['home_away'] = '1'
                match['result'] = 1 if (match['home_score'] - match['away_score'] > 0) else 0
            elif prediction == QualificationCheck.prediction_away_win:
                match['home_away'] = '2'
                match['result'] = 1 if (match['away_score'] - match['home_score'] > 0) else 0
            else:
                raise ValueError('match prediction is not expected. Expect home_win or away_won, but got ' + prediction)

        print(str(len(matches)) + " labelled - win is labelled 1, others are labelled 0.")

        return matches
