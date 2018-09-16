import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys


class Betfair:

    base_url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    event_type_id_soccer = 1
    bet_type_match_odds = 'MATCH_ODDS'

    def __init__(self, app_key, session_token):
        self.request_headers = \
            {'X-Application': app_key, 'X-Authentication': session_token, 'content-type': 'application/json'}

    def place_match_odds_bet(self, game_data):

        home_team_name = game_data['home_team_name']
        away_team_name = game_data['away_team_name']
        bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
        response_json = json.loads(self._get_market_catalogue(home_team_name, away_team_name, self.bet_type_match_odds))
        market_id, selection_id = self._get_match_odds_market_selection_id(response_json, bet_on_team)

        if not selection_id:
            self._execute_bet(market_id, selection_id, 1000)
        else:
            print("failed to place bet - cannot get selectionId'")

    def _execute_bet(self, market_id, selection_id, amount):
        filters = {}
        endpoint = "listMarketCatalogue"
        return self._call_api(json.dumps(self._query_builder(endpoint, filters)))

    def _get_match_odds_market_selection_id(self, response_json, bet_on_team):
        # Assert required fields
        try:
            # Assert values
            assert response_json['result'][0]['marketName'] == 'Match Odds', "'marketName' is not 'Match Odds'"
            for runner in response_json['result'][0]['runners']:
                if runner ['runnerName'] == bet_on_team:
                    return response_json['result'][0]['marketId'], runner ['selectionId']
        except AssertionError as ae:
            print ('Failed to place bet - ', str (ae))
        except KeyError as ke:
            print ('Failed to place bet - ', str (ke))

        return None

    def _get_market_catalogue(self, home_team_name, away_team_name, market_types):

        filters = {
            "eventTypeIds": [self.event_type_id_soccer],
            # "marketCountries": [country_code],
            "marketTypeCodes": [market_types],
            "textQuery": home_team_name + ' ' + away_team_name
        }
        endpoint = "listMarketCatalogue"
        return self._call_api(json.dumps(self._query_builder(endpoint, filters)))

    def _call_api(self, jsonrpc_req):
        try:
            req = urllib.request.Request(self.base_url, jsonrpc_req.encode('utf-8'), self.request_headers)
            # print(req.data)
            # print(req.full_url)
            # print(req.headers)
            response = urllib.request.urlopen(req)
            jsonResponse = response.read()
            return jsonResponse.decode('utf-8')
        except urllib.error.URLError as e:
            raise e
            # print('Oops no service available at ' + str(self.base_url))

    @staticmethod
    def _query_builder(endpoint, filters):
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


if __name__ == "__main__":
    data = {
        'gid': 1552193, 'league_id': 36, 'league_name': 'English Premier League', 'kickoff': 1537714800.0,
        'home_team_name': 'Arsenal', 'away_team_name': 'Everton', 'home_team_id': 19, 'away_team_id': 31,
        'preferred_team': 'home', 'bet_on_market': 'win', 'min_odds_to_bet_on': 1.5
    }

    # Betfair(input("API key:"), input("session token:")).place_bet(data)
    betfair = Betfair("4NTZimyPy6zJ8LDN", "bu4AI6Dvo8us4Gyus1yrTmRldawKhDtqLrxWlliyXB4=")

    bet_type = data['bet_on_market']
    if bet_type == 'win':
        betfair.place_match_odds_bet(data)
    # todo: add AH bet types later
    else:
        print('unrecognised bet type - ', bet_type)
