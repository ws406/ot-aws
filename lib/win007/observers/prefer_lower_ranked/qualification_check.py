class QualificationCheck:

    prediction_home_win = 'home-win'
    prediction_away_win = 'away-win'
    disqualified = 'disqualified'

    condition_open_odds_ok_home = '*** home-team-open-odds-qualify ***'
    condition_open_odds_ok_away = '*** away-team-open-odds-qualify ***'
    condition_open_odds_disqualify = 'open-odds-disqualify'

    def __init__(self):
        pass

    def is_qualified(self, game_data):

        open_odds_condition = self.condition_open_odds_disqualify
        prediction = self.disqualified
        exceptions = None

        try:
            # 1. check ranking condition: to qualify, the team that ranks lower needs to have winning odds that is lower than 1.9
            # Away team ranks lower or only one position higher than home team. E.g. home ranks 3, away ranks 2 or 4 or lower.
            if (game_data['away_team_rank'] - game_data['home_team_rank'] > -1) and \
                            game_data['odds']['macau_slot']['open']['2'] <= 1.90:
                open_odds_condition = self.condition_open_odds_ok_away

            # Home team ranks lower or only one position higher than away team. E.g. away ranks 3, home ranks 2 or 4 or lower.
            elif (game_data['home_team_rank'] - game_data['away_team_rank'] > -1 ) and \
                            game_data['odds']['macau_slot']['open']['1'] <= 1.90:
                open_odds_condition = self.condition_open_odds_ok_home

            # 2. Predict by odds trend. If all-final-odds is smaller than all-original-odds, predict that result.
            if open_odds_condition == self.condition_open_odds_ok_away and \
                game_data['odds']['macau_slot']['open']['1'] < game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] > game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] < game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] > game_data['odds']['will_hill']['final']['2'] and \
                game_data['odds']['bet365']['open']['1'] < game_data['odds']['bet365']['final']['1'] and \
                game_data['odds']['bet365']['open']['2'] > game_data['odds']['bet365']['final']['2'] and \
                game_data['odds']['pinnacle']['open']['1'] < game_data['odds']['pinnacle']['final']['1'] and \
                    game_data['odds']['pinnacle']['open']['2'] > game_data['odds']['pinnacle']['final']['2']:

                prediction = self.prediction_away_win

            elif open_odds_condition == self.condition_open_odds_ok_home  and \
                game_data['odds']['macau_slot']['open']['1'] > game_data['odds']['macau_slot']['final']['1'] and \
                game_data['odds']['macau_slot']['open']['2'] < game_data['odds']['macau_slot']['final']['2'] and \
                game_data['odds']['will_hill']['open']['1'] > game_data['odds']['will_hill']['final']['1'] and \
                game_data['odds']['will_hill']['open']['2'] < game_data['odds']['will_hill']['final']['2'] and \
                game_data['odds']['bet365']['open']['1'] > game_data['odds']['bet365']['final']['1'] and \
                game_data['odds']['bet365']['open']['2'] < game_data['odds']['bet365']['final']['2'] and \
                game_data['odds']['pinnacle']['open']['1'] > game_data['odds']['pinnacle']['final']['1'] and \
                    game_data['odds']['pinnacle']['open']['2'] < game_data['odds']['pinnacle']['final']['2']:

                prediction = self.prediction_home_win


        except (TypeError, KeyError):
            exceptions = 'missing required odds'

        if open_odds_condition != self.condition_open_odds_disqualify:
            prediction += ' - ' + open_odds_condition

        if exceptions is not None:
            prediction += ' - ' + exceptions

        return prediction
