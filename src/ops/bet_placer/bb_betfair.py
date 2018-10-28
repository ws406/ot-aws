import urllib
import urllib.request
import urllib.error
import json
from src.ops.bet_placer.betfair import Betfair

class BBBetfair(Betfair):

    event_type_id = 7522
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Moneyline'

    def place_match_odds_bet(self, game_data, betting_amount):

        home_team_name = game_data['home_team_name']
        away_team_name = game_data['away_team_name']

        # If bet_on_market is 'preferred team win', bet on preferred team. Otherwise, bet on the other team.
        if game_data['bet_on_market'] == 'preferred team win':
            bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
        elif game_data['bet_on_market'] == 'preferred team lose':
            bet_on_team = home_team_name if game_data ['preferred_team'] == 'away' else away_team_name
        else:
            return 'cannot handle bet_on_market : ' + game_data['bet_on_market']

        # Add the 4% BetFair charge on top of the min_odds_to_bet_on
        price = round((game_data['min_odds_to_bet_on']-1)*1.04+1, 2)
        try:
            response_json = json.loads(self._get_market_catalogue(home_team_name, away_team_name, self.market_type_code_match_odds))
            market_id, selection_id = self._get_match_odds_market_selection_id(response_json, bet_on_team)

            # TODO: next step is to check amount and make sure existing bets' amount is enough
            if self.does_this_bet_exist(market_id):
                print('Bet is already made!')
                return 'Bet is already made!'

            if selection_id:
                return self._execute_bet(market_id, selection_id, betting_amount, price)
            else:
                print("failed to place bet - cannot get selectionId'")
                # todo: check if it is success
                print(response_json)
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    # data = {
    #     'gid': 1552212, 'league_id': 36, 'league_name': 'English Premier League', 'kickoff': 1538229600.0,
    #     'home_team_name': 'Wolves', 'away_team_name': 'Southampton', 'home_team_id': 52, 'away_team_id': 30,
    #     'preferred_team': 'home', 'bet_on_market': 'win', 'min_odds_to_bet_on': 1.8
    # }

    data = {'gid': 325656, 'league_id': 1, 'league_name': 'NBA', 'kickoff': 1540767600.0,
            'home_team_name': 'Dallas Mavericks', 'away_team_name': 'Utah Jazz', 'home_team_id': 17, 'away_team_id': 20,
            'preferred_team': 'away', 'bet_on_market': 'preferred team lose',
            'details': 'preferred team lose,prefer away,0.3657957244655582:0.6342042755344418,prob,0.5324:0.4676,2.67:1.54',
            'min_odds_to_bet_on': 2.67}

    # Betfair(input("API key:"), input("session token:")).place_bet(data)
    betfair = BBBetfair("4NTZimyPy6zJ8LDN", "nC6W3lfWK8CFKSZbucfvPS0YKrTcSXa6hJ+ytdpd73w=")

    bet_type = data['bet_on_market']
    if bet_type == 'preferred team win' or bet_type == 'preferred team lose':
        betfair.place_match_odds_bet(data, 2)
    # todo: add AH bet types later
    else:
        print('unrecognised bet type - ', bet_type)
