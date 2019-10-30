import urllib
import urllib.request
import urllib.error
import json
from src.ops.bet_placer.betfair import Betfair
from src.ops.game_predictor.bb_blended_true_odds import TrueOdds


class BBBetfair (Betfair):
    event_type_id = 7522
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Moneyline'

    team_names_mapping = {}

    def place_match_odds_bet(self, game_data, betting_amount, debug_mode=False):

        if game_data['strategy'] == TrueOdds.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, debug_mode)
        else:
            # Add other strategies later
            # bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
            self.logger.exception('*** No strategy is found. Skip placing bets. ***')
            pass

    def _place_bet_for_true_odds(self, game_data, betting_amount, debug_mode):
        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])

        bet_placing_outcome = dict()
        # self.logger.log(game_data)

        for key, bet_on_odds in game_data['true_odds'].items():
            if key == '1':
                bet_on_team = home_team_name
            elif key == '2':
                bet_on_team = away_team_name
            else:
                self.logger.exception('*** Wrong key! key = ' + key + ' ***')
                continue

            # Add the BetFair commission and profit margin on top of the min_odds_to_bet_on
            price = self._round_up_odds (
                (bet_on_odds - 1)
                /
                (1-self.commission_rate)
                +
                1
            )
            #print("BET:", bet_on_team, price)
            bet_placing_outcome[key] = self._place_bet (
                home_team_name,
                away_team_name,
                bet_on_team,
                self.market_type_code_match_odds,
                betting_amount,
                price,
                debug_mode,
                self.back_bet
            )
        return bet_placing_outcome

    def _unify_team_name(self, team_name):
        try:
            return self.team_names_mapping[team_name]
        except KeyError:
            return team_name
