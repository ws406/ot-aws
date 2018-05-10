from lib.strategy_finding.sample_selector.interface import SampleSelectorInterface
from lib.win007.observers.same_direction.qualification_check import QualificationCheck

# TODO: need to figure out a way to balance the number of matches which qualified as right and wrong, so that the samples are even.

def Returns(favTeamOdds, dnbOdds, dcOdds):
    if favTeamOdds <= 1.83:
        return favTeamOdds - 1
    elif dnbOdds < 1.5: # bet 0/0.5
        return (favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2
    elif dcOdds < 1.5:
        return dnbOdds - 1
    elif dcOdds <= 2:
        return dcOdds - 1
    else:
        return 0

class TrendingOnlySelector(SampleSelectorInterface):

    def get_selected_games_data(self, raw_data: dict):
        print("Running game selector - TrendingOddsSelector")
        qualified_matches = []
        for match in raw_data:
            predict = QualificationCheck().is_qualified(match)
            if predict == QualificationCheck.disqualified:
               continue
            else:
                if predict == 'x':
                    continue
                if predict == '1':
                    home_dnb_odds = match['odds']['bet365']['final']['1'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                    home_dc_odds = match['odds']['bet365']['final']['1'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['1'] + match['odds']['bet365']['final']['x'])
                    if Returns(match['odds']['bet365']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient) < 0.5:
                        continue
                if predict == '2':
                    away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                    away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
                    if Returns(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient) < 0.5:
                        continue
                match['prediction'] = predict
                qualified_matches.append(match)
        print(str(len(qualified_matches)) + " matches selected for analysis.")
        return qualified_matches