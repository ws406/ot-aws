from lib.strategy_finding.sample_selector.interface import SampleSelectorInterface
from lib.win007.observers.same_direction.qualification_check import QualificationCheck

class TrendingOnlySelector(SampleSelectorInterface):

    def get_selected_games_data(self, matches: dict):
        print("Running game selector - TrendingOnlySelector")
        qualified_matches = []
        for match in matches:
            predict = QualificationCheck().is_qualified(match)
            if predict == QualificationCheck.disqualified:
               continue
            else:
                match['prediction'] = predict
                qualified_matches.append(match)
        print(str(len(qualified_matches)) + " matches selected for analysis.")
        return qualified_matches
