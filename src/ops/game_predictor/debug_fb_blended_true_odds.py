from src.ops.game_predictor.interface import GamePredictorInterface


# This class is only used for testing purpose
class TrueOdds(GamePredictorInterface):



    def get_prediction(self, data):
        return_data = dict()
        return_data['true_odds'] = {
            '1': 10,
            'x': 10,
            '2': 10,
        }
        return_data['gid'] = data ['game_id']
        return_data['league_id'] = data ['league_id']
        return_data['league_name'] = data ['league_name']
        return_data['kickoff'] = data ['kickoff']
        return_data['home_team_name'] = data ['home_team_name']
        return_data['away_team_name'] = data ['away_team_name']
        return_data['home_team_id'] = data ['home_team_id']
        return_data['away_team_id'] = data ['away_team_id']
        return_data['strategy'] = "true_odds"
        return return_data

