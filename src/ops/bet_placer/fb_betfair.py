import json
from src.ops.bet_placer.betfair import Betfair

class FBBetfair(Betfair):

    event_type_id = 1
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Match Odds'
    runner_name_draw = 'The Draw'

    team_names_mapping = {

        'AS Roma': 'Roma',

        'Tottenham Hotspur': 'Tottenham',
        'West Ham United' : 'West Ham',
        'Brighton   Hove Albion': 'Brighton',
        'Leicester City': 'Leicester',
        'Norwich City': 'Norwich',
        'Crystal Palace': 'C Palace',
        'Newcastle United': 'Newcastle',

        'Wigan Athletic': 'Wigan',

        'TSG Hoffenheim': 'Hoffenheim',
        'Bayer Leverkusen': 'Leverkusen',

        'Parana PR': 'Parana',
        'Operario Ferroviario PR': 'Operario PR',
        'Guarani SP': 'Guarani',
        'Coritiba PR': 'Coritiba',
        'Bragantino': 'Bragantino SP',
        'Atletico Clube Goianiense': 'Atletico Go',
        'Sport Club Recife PE': 'Sport Recife',

        'Atlanta United': 'Atlanta Utd',

        'Ventforet Kofu': 'Kofu',
        'Fagiano Okayama': 'Okayama',
        'JEF United Ichihara Chiba': 'Jef Utd Chiba',
        'Kashiwa Reysol': 'Kashiwa',
        'Kawasaki Frontale': 'Kawasaki',
        'Oita Trinita': 'Oita',
        'Ehime FC': 'Ehime',
        'Zweigen Kanazawa FC': 'Kanazawa',
        'Kagoshima United': 'Kagoshima Utd',
        'V-Varen Nagasaki': 'Nagasaki',
        'Tokyo Verdy': 'Tokyo-V',
        'Machida Zelvia': 'FC Machida',
        'Avispa Fukuoka': 'Fukuoka',
        'Mito Hollyhock': 'Mito',
        'Montedio Yamagata': 'Yamagata',
        'Tokushima Vortis': 'Tokushima',
        'Kyoto Sanga': 'Kyoto',
        'Omiya Ardija': 'Omiya',

        'Hebei HX Xingfu': 'Hebei CFFC',
        'Chongqing SWM Motors': 'Chongqing Lifan',
        'Dalian Aerbin': 'Dalian Yifang',
        'Henan Jianye': 'Henan',
        'Guangzhou Fuli FC': 'Guangzhou R&F',

        # Swedish Super League
        'VfL Osnabruck': 'VFL Osnabruck',
        'Heidenheimer': 'FC Heidenheim',
        'IK Sirius FK': 'Sirius',
        'AIK Solna': 'AIK',


        # Russian Super League
        'Spartak Tambov': 'FK Tambov',

        # Belgium 1
        'Mechelen': 'Yellow-Red Mechelen',
    }

    def place_match_odds_bet(self, game_data, betting_amount, debug_mode=False):

        if game_data['strategy'] == 'true_odds':
            return self._place_bet_for_true_odds(game_data, betting_amount, debug_mode)
        else:
            # Add other strategies later
            # bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
            print('*** No strategy is found. Skip placing bets. ***')
            pass

    def _place_bet_for_true_odds(self, game_data, betting_amount, debug_mode):
        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])

        bet_placing_outcome = dict()
        print(game_data)

        for key, bet_on_odds in game_data['true_odds'].items():
            if key == '1':
                bet_on_team = home_team_name
            elif key == '2':
                bet_on_team = away_team_name
            elif key == 'x':
                bet_on_team = self.runner_name_draw
            else:
                print('*** Wrong key! key = ' + key + ' ***')
                continue

            # Add the BetFair commission and profit margin on top of the min_odds_to_bet_on
            price = self._round_up_odds (
                (bet_on_odds * (1 + self.profit_margin) - 1)
                /
                (1-self.commission_rate)
                +
                1
            )
            bet_placing_outcome[key] = self._place_bet (
                home_team_name,
                away_team_name,
                bet_on_team,
                self.market_type_code_match_odds,
                betting_amount,
                price,
                debug_mode
            )
        return bet_placing_outcome

    def _unify_team_name(self, team_name):
        try:
            return self.team_names_mapping[team_name]
        except KeyError:
            return team_name
