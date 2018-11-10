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


if __name__ == "__main__":
    # Test bet placing
    data = {'away_team_name': 'Indiana Pacers', 'min_odds_to_bet_on': 1.86, 'home_team_id': 3, 'strategy': 'nba',
            'kickoff': 1541813400.0, 'bet_on_market': 'preferred team win', 'league_name': 'NBA',
            'details': 'preferred team win,prefer away,0.4757033248081842:0.5242966751918159,prob,0.4358:0.5642,2.05:1.86',
            'league_id': 1, 'home_team_name': 'Miami Heat', 'away_team_id': 10, 'preferred_team': 'away', 'gid': 325741}
    #
    # # Betfair(input("API key:"), input("session token:")).place_bet(data)
    BBBetfair ("4NTZimyPy6zJ8LDN", "wAQlfjE+iF6D6p1LBA8D3Y4WbHL9hGYoo0umTA4nLBk=").place_match_odds_bet(data, 2)
    #
    # bet_type = data['bet_on_market']
    # if bet_type == 'preferred team win' or bet_type == 'preferred team lose':
    #     result = betfair.place_match_odds_bet(data, 2)
    #     print (result)
    #     if result['status'] == 'error':
    #         print('error!!!')
    #     else:
    #         print('good!!!')
    # # todo: add AH bet types later
    # else:
    #     print('unrecognised bet type - ', bet_type)

    # Test _round_up_odds method
    # values = [1.23, 1.99, 2.00, 2.01, 2.3333333, 2.23, 2.06, 2.99, 3.01, 3.05, 3.9992, 3.3367, 3.776, 4.56, ]
    # for value in values:
    #     print(str(value) + ' => ' + str(BBBetfair('a', 'b')._round_up_odds(value)))

    # print (BBBetfair ("4NTZimyPy6zJ8LDN", "wAQlfjE+iF6D6p1LBA8D3Y4WbHL9hGYoo0umTA4nLBk=").does_this_bet_exist (
    #     '1.150961891'))

    # customerStrategyRefs: ["nbavbet"]


