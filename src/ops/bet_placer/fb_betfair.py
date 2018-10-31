import json
from src.ops.bet_placer.betfair import Betfair

class FBBetfair(Betfair):

    event_type_id = 1
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Match Odds'

    team_names_mapping = {
        'AS Roma': 'Roma',
        'Tottenham Hotspur': 'Tottenham'
    }

    def place_match_odds_bet(self, game_data, betting_amount):

        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])

        bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name

        # Add the 4% BetFair charge on top of the min_odds_to_bet_on
        price = self._round_up_odds ((game_data ['min_odds_to_bet_on'] - 1) * 1.04 + 1)
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
        except IndexError as ie:
            print ("failed to place bet - cannot get selectionId'")


    def _unify_team_name(self, teamname):
        try:
            return self.team_names_mapping[teamname]
        except KeyError:
            return teamname


if __name__ == "__main__":

    data = {'gid': 1585150, 'league_id': 34, 'league_name': 'Italian Serie A', 'kickoff': 1540755000.0,
            'home_team_name': 'Napoli', 'away_team_name': 'AS Roma', 'home_team_id': 1419, 'away_team_id': 174,
            'preferred_team': 'home', 'bet_on_market': 'win', 'min_odds_to_bet_on': 1.57}

    # Betfair(input("API key:"), input("session token:")).place_bet(data)
    betfair = FBBetfair("4NTZimyPy6zJ8LDN", "nC6W3lfWK8CFKSZbucfvPS0YKrTcSXa6hJ+ytdpd73w=")

    bet_type = data['bet_on_market']
    if bet_type == 'win':
        betfair.place_match_odds_bet(data, 2)
    # todo: add AH bet types later
    else:
        print('unrecognised bet type - ', bet_type)
