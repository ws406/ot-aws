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

def IsPredictRight(favTeamOdds, dnbOdds, dcOdds, predict, result, goalDiff, awayTeamOdds):
    if favTeamOdds <= 1.83:
        if predict == result:
            return [favTeamOdds - 1, 1]
        else:
            return [favTeamOdds - 1, -1]
    elif dnbOdds < 1.5: # bet 0/0.5
        if goalDiff > 0:
            return [(favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2, 1]
        elif goalDiff == 0:
            return [(favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2, -0.5]
        else:
            return [(favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2, -1]
    elif dcOdds < 1.5:
        if predict == result:
            return [dnbOdds - 1, 1]
        elif result == 'x':
            return [dnbOdds - 1, 0]
        else:
            return [dnbOdds - 1, -1]
    elif dcOdds <= 2:
        if predict == result or result == 'x':
            return [dcOdds - 1, 1]
        else:
            return [dcOdds - 1, -1]
    else:
        if goalDiff >= 0:
            return [0.3, 1]
        elif goalDiff == -1:
            return [0.3, 0]
        else:
            return [0.3, -1]

class TrendingOddsSelector(SampleSelectorInterface):

    def get_selected_games_data(self, raw_data: dict):
        print("Running game selector - TrendingOddsSelector")
        qualified_matches = []
        coefficient = 0.95
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
                    result = IsPredictRight(match['odds']['bet365']['final']['1'], home_dnb_odds * coefficient, home_dc_odds * coefficient, '1', match['result'], match['home_score'] - match['away_score'], match['odds']['bet365']['final']['2'])
                    match['potentialReturn'] = result[0]
                    if result[1] > 0:
                        match['result'] = 1
                    elif result[1] <= 0:
                        match['result'] = 0
                if predict == '2':
                    away_dnb_odds = match['odds']['bet365']['final']['2'] * (match['odds']['bet365']['final']['x'] - 1) / match['odds']['bet365']['final']['x']
                    away_dc_odds = match['odds']['bet365']['final']['2'] * match['odds']['bet365']['final']['x'] / (match['odds']['bet365']['final']['2'] + match['odds']['bet365']['final']['x'])
                    if Returns(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient) < 0.5:
                        continue
                    result = IsPredictRight(match['odds']['bet365']['final']['2'], away_dnb_odds * coefficient, away_dc_odds * coefficient, '2', match['result'], match['away_score'] - match['home_score'], match['odds']['bet365']['final']['1'])
                    match['potentialReturn'] = result[0]
                    if result[1] > 0:
                        match['result'] = 1
                    elif result[1] <= 0:
                        match['result'] = 0
                match['prediction'] = predict
                qualified_matches.append(match)
        print(str(len(qualified_matches)) + " matches selected for analysis.")
        return qualified_matches