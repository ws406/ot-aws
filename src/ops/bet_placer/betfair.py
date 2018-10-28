import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys
import abc

class Betfair(abc.ABC):

    base_url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    market_name = ''
    event_type_id = ''

    def __init__(self, app_key, session_token):
        self.request_headers = \
            {'X-Application': app_key, 'X-Authentication': session_token, 'content-type': 'application/json'}

    @abc.abstractmethod
    def place_match_odds_bet(self, game_data, betting_amount):
        pass

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
            "eventTypeIds": [self.event_type_id],
            # "marketCountries": [country_code],
            "marketTypeCodes": [market_types],
            "textQuery": home_team_name + ' ' + away_team_name
        }
        print(filters)
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