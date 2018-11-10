import urllib
import urllib.request
import urllib.error
import json
from src.ops.bet_placer.betfair import Betfair


class BBBetfair (Betfair):
    event_type_id = 7522
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Moneyline'

    def place_match_odds_bet (self, game_data, betting_amount):

        home_team_name = game_data ['home_team_name']
        away_team_name = game_data ['away_team_name']

        # If bet_on_market is 'preferred team win', bet on preferred team. Otherwise, bet on the other team.
        if game_data ['bet_on_market'] == 'preferred team win':
            bet_on_team = home_team_name if game_data ['preferred_team'] == 'home' else away_team_name
        elif game_data ['bet_on_market'] == 'preferred team lose':
            bet_on_team = home_team_name if game_data ['preferred_team'] == 'away' else away_team_name
        else:
            return 'cannot handle bet_on_market : ' + game_data ['bet_on_market']

        # Add the 4% BetFair charge on top of the min_odds_to_bet_on
        price = self._round_up_odds ((game_data ['min_odds_to_bet_on'] - 1) * 1.04 + 1)
        return self._place_bet (home_team_name, away_team_name, bet_on_team, self.market_type_code_match_odds,
                                betting_amount, price, game_data['strategy'])
