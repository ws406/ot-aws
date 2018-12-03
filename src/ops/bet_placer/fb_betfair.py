import json
from src.ops.bet_placer.betfair import Betfair

class FBBetfair(Betfair):

    event_type_id = 1
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Match Odds'

    team_names_mapping = {
        'AS Roma': 'Roma',
        'Tottenham Hotspur': 'Tottenham',
        'West Ham United' : 'West Ham',
        'Brighton   Hove Albion': 'Brighton',
        'Leicester City': 'Leicester',
        'Wigan Athletic': 'Wigan',
        'Norwich City': 'Norwich',
        'TSG Hoffenheim': 'Hoffenheim',
        'Crystal Palace': 'C Palace',
        'Bayer Leverkusen': 'Leverkusen',
    }

    def place_match_odds_bet(self, game_data, betting_amount):

        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])

        bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name

        # Add the 4% BetFair charge on top of the min_odds_to_bet_on
        price = self._round_up_odds ((game_data ['min_odds_to_bet_on'] - 1) * 1.04 + 1)
        return self._place_bet (home_team_name, away_team_name, bet_on_team, self.market_type_code_match_odds, betting_amount,
                         price)

    def _unify_team_name(self, teamname):
        try:
            return self.team_names_mapping[teamname]
        except KeyError:
            return teamname
