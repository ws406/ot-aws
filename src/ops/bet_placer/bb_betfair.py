import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys


class Betfair:

    base_url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    event_type_id_basketball = 7522
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Moneyline'

    def __init__(self, app_key, session_token):
        self.request_headers = \
            {'X-Application': app_key, 'X-Authentication': session_token, 'content-type': 'application/json'}

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

    def _execute_bet(self, market_id, selection_id, size, price):
        parameters = {
            "marketId": market_id,
            "instructions": [
                {
                    "selectionId": selection_id,
                    "handicap": "0",
                    "side": "BACK",
                    "orderType": "LIMIT",
                    "limitOrder": {
                        "size": size,
                        "price": price,
                        "persistenceType": "PERSIST"
                    }
                }
            ]
        }
        endpoint = "placeOrders"
        bet_placer_response = self._call_api(json.dumps(self._order_request_builder(endpoint, parameters)))
        print("Bet placing result: ")
        print(bet_placer_response)
        return bet_placer_response

        # TODO: do this properly - 1st: matched bet; 2nd: unmatched bet
        # {"jsonrpc": "2.0", "result": {"status": "SUCCESS", "marketId": "1.150300702", "instructionReports": [
        #     {"status": "SUCCESS", "instruction": {"selectionId": 237486, "handicap": 0.0,
        #                                           "limitOrder": {"size": 2.0, "price": 1.83,
        #                                                          "persistenceType": "PERSIST"}, "orderType": "LIMIT",
        #                                           "side": "BACK"}, "betId": "142677701352",
        #      "placedDate": "2018-10-27T20:44:17.000Z", "averagePriceMatched": 1.95, "sizeMatched": 2.0,
        #      "orderStatus": "EXECUTION_COMPLETE"}]}, "id": 1}

        # {"jsonrpc": "2.0", "result": {"status": "SUCCESS", "marketId": "1.150300702", "instructionReports": [
        #     {"status": "SUCCESS", "instruction": {"selectionId": 237486, "handicap": 0.0,
        #                                           "limitOrder": {"size": 2.0, "price": 2.02,
        #                                                          "persistenceType": "PERSIST"}, "orderType": "LIMIT",
        #                                           "side": "BACK"}, "betId": "142677542553",
        #      "placedDate": "2018-10-27T20:42:48.000Z", "averagePriceMatched": 0.0, "sizeMatched": 0.0,
        #      "orderStatus": "EXECUTABLE"}]}, "id": 1}

        # bet_placer_result = bet_placer_response['result']
        # bet_placer_status = bet_placer_result['status']
        # if bet_placer_result == 'success'

    def _get_match_odds_market_selection_id(self, response_json, bet_on_team):
        # Assert required fields
        # Assert values
        get = response_json['result'][0]['marketName']
        expect = self.market_name
        error_string = "'marketName' is" + get + " instead of " + self.market_name
        assert get == expect, error_string
        for runner in response_json['result'][0]['runners']:
            if runner ['runnerName'] == bet_on_team:
                return response_json['result'][0]['marketId'], runner['selectionId']

        return None

    def _get_market_catalogue(self, home_team_name, away_team_name, market_types):

        filters = {
            "eventTypeIds": [self.event_type_id_basketball],
            # "marketCountries": [country_code],
            "marketTypeCodes": [market_types],
            "textQuery": home_team_name + ' ' + away_team_name
        }
        endpoint = "listMarketCatalogue"
        return self._call_api(json.dumps(self._query_request_builder(endpoint, filters)))

    def does_this_bet_exist(self, market_id):
        # TODO: the filters doesn't work!
        filters = {
            "marketIds": [str(market_id)]
        }
        endpoint = "listCurrentOrders"
        response = json.loads(self._call_api (json.dumps (self._query_request_builder (endpoint, filters))))

        try:
            bets = response['result']['currentOrders']
            if (len(bets) > 0):
                for bet in bets:
                    if str(bet['marketId']) == str(market_id):
                        return True
                return False
            else :
                return False

        except IndexError as ie:
            return False

    def _call_api(self, jsonrpc_req):
        try:
            req = urllib.request.Request(self.base_url, jsonrpc_req.encode('utf-8'), self.request_headers)
            response = urllib.request.urlopen(req)
            jsonResponse = response.read()
            return jsonResponse.decode('utf-8')
        except urllib.error.URLError as e:
            raise e

    @staticmethod
    def _query_request_builder(endpoint, filters):
        return {
            "jsonrpc": "2.0",
            "method": "SportsAPING/v1.0/" + endpoint,
            "params": {
                "filter": filters,
                "maxResults": 1,
                "marketProjection": ["RUNNER_METADATA"]
            },
            "id": 1
        }

    @staticmethod
    def _order_request_builder(endpoint, params):
        return {
            "jsonrpc": "2.0",
            "method": "SportsAPING/v1.0/" + endpoint,
            "params": params,
            "id": 1
        }


if __name__ == "__main__":
    # data = {
    #     'gid': 1552212, 'league_id': 36, 'league_name': 'English Premier League', 'kickoff': 1538229600.0,
    #     'home_team_name': 'Wolves', 'away_team_name': 'Southampton', 'home_team_id': 52, 'away_team_id': 30,
    #     'preferred_team': 'home', 'bet_on_market': 'win', 'min_odds_to_bet_on': 1.8
    # }

    data = {'gid': 338133, 'league_id': 1, 'league_name': 'NBA', 'kickoff': 1540684800.0,
            'home_team_name': 'Miami Heat', 'away_team_name': 'Portland Trail Blazers', 'home_team_id': 3,
            'away_team_id': 25, 'preferred_team': 'home', 'bet_on_market': 'preferred team win',
            'details': 'preferred team win,prefer home,0.4936061381074168:0.5063938618925831,prob,0.556:0.444,1.98:1.93',
            'min_odds_to_bet_on': 1.80}

    # Betfair(input("API key:"), input("session token:")).place_bet(data)
    betfair = Betfair("4NTZimyPy6zJ8LDN", "nC6W3lfWK8CFKSZbucfvPS0YKrTcSXa6hJ+ytdpd73w=")

    bet_type = data['bet_on_market']
    if bet_type == 'preferred team win' or bet_type == 'preferred team lose':
        betfair.place_match_odds_bet(data, 2)
    # todo: add AH bet types later
    else:
        print('unrecognised bet type - ', bet_type)
