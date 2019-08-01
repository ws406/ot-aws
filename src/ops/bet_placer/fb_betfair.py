from src.ops.bet_placer.betfair import Betfair
from src.ops.game_predictor.fb_informed_odds import InformedOdds
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
from src.win007.observers.informed_odds.qualification_check import QualificationCheck as InformedOddsQualCheck


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
        'Luton Town': 'Luton',

        # GE 1 & 2
        'TSG Hoffenheim': 'Hoffenheim',
        'Bayer Leverkusen': 'Leverkusen',
        'Darmstadt': 'SV Darmstadt',
        'Erzgebirge Aue': 'Erzgebirge',
        'VfL Bochum': 'Bochum',
        'SV Wehen Wiesbaden': 'Wehen Wiesbaden',
        'Karlsruher SC': 'Karlsruhe',
        'St. Pauli': 'St Pauli',

        # BR 1 & 2
        'Parana PR': 'Parana',
        'Operario Ferroviario PR': 'Operario PR',
        'Guarani SP': 'Guarani',
        'Coritiba PR': 'Coritiba',
        'Bragantino': 'Bragantino SP',
        'Atletico Clube Goianiense': 'Atletico Go',
        'Sport Club Recife PE': 'Sport Recife',
        'Londrina PR': 'Londrina',
        'Palmeiras': 'SE Palmeiras',
        'Vasco da Gama': 'Vasco Da Gama',
        'Fluminense RJ': 'Fluminense',
        'Ceara': 'Ceara SC Fortaleza',
        'Internacional RS': 'Internacional',
        'Cruzeiro (MG)': 'Cruzeiro MG',
        'Atletico Paranaense': 'Atletico PR',
        'Chapecoense SC': 'Chapecoense',
        'Bahia BA': 'Bahia',
        'Botafogo RJ': 'Botafogo',
        'Avai FC SC': 'Avai',
        'Corinthians Paulista (SP)': 'Corinthians',
        'Atletico Mineiro': 'Atletico MG',

        # USA
        'Atlanta United': 'Atlanta Utd',
        'New England Revolution': 'New England',
        'Columbus Crew': 'Columbus',
        'DC United': 'DC Utd',
        'Minnesota United FC': 'Minnesota Utd',
        'Philadelphia Union': 'Philadelphia',
        'Colorado Rapids': 'Colorado',

        # JAP 1 & 2
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
        'Vissel Kobe': 'Kobe',
        'Gamba Osaka': 'G-Osaka',

        # CHINA 1
        'Hebei HX Xingfu': 'Hebei CFFC',
        'Chongqing SWM Motors': 'Chongqing Lifan',
        'Dalian Aerbin': 'Dalian Yifang',
        'Henan Jianye': 'Henan',
        'Guangzhou Fuli FC': 'Guangzhou R&F',
        'Tianjin Tianhai': 'Tianjin Quanjian',
        'Guangzhou Evergrande Taobao FC': 'Guangzhou FC',
        'Jiangsu Suning FC': 'Jiangsu Suning',
        'Shenzhen JiaZhaoye': 'Shenzhen FC',
        'Wuhan ZALL': 'Wuhan Zall',
        'Shanghai East Asia FC': 'Shanghai East Asia',

        # Swedish Super League
        'VfL Osnabruck': 'VFL Osnabruck',
        'Heidenheimer': 'FC Heidenheim',
        'IK Sirius FK': 'Sirius',
        'AIK Solna': 'AIK',
        'GIF Sundsvall': 'Sundsvall',
        'AFC Eskilstuna': 'AFC Utd',
        'Falkenberg': 'Falkenbergs',
        'IFK Norrkoping FK': 'Norrkoping',


        # Russian Super League
        'Spartak Tambov': 'FK Tambov',
        'FK Sochi': 'Sochi',
        'FC Krasnodar': 'FK Krasnodar',
        'Gazovik Orenburg': 'FC Orenburg',
        'Zenit St. Petersburg': 'Zenit St Petersburg',
        'Rostov FK': 'Rostov',
        'Lokomotiv Moscow': 'Lokomotiv',

        # Belgium 1
        'Mechelen': 'Yellow-Red Mechelen',
        'Standard Liege': 'Standard',
        'Mouscron Peruwelz': 'Royal Mouscron-peruwelz',
        'Red Star Waasland': 'Waasland-Beveren',
        'Sint-Truidense': 'Sint Truiden',
        'Oostende': 'KV Oostende',
        'KAA Gent': 'Gent',
        'KAS Eupen': 'Eupen',
        'Royal Antwerp': 'Antwerp',

        # FR 1 & 2
        'AJ Auxerre': 'Auxerre',
        'Troyes': 'ESTAC Troyes',
        'Ajaccio': 'AC Ajaccio',
        'Rodez Aveyron': 'Rodez',
        'Chamois Niortais': 'Niort',
        'Orleans US 45': 'Orleans',
        'Chambly FC': 'Chambly Oise',

    }

    def place_match_odds_bet(self, game_data, betting_amount, debug_mode=False):

        if game_data['strategy'] == TrueOdds.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, debug_mode)
        elif game_data['strategy'] == InformedOdds.strategy:
            return self._place_bet_for_informed_odds(game_data, betting_amount, debug_mode)
        else:
            # Add other strategies later
            # bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
            print('*** No strategy is found. Skip placing bets. ***')
            pass

    def _place_bet_for_informed_odds(self, game_data, betting_amount, debug_mode):
        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])
        bet_on_odds = game_data['bet_odds']

        print(game_data)

        if game_data['bet_direction'] == InformedOddsQualCheck.prediction_home_win:
            bet_on_team = home_team_name
            back_lay = self.back_bet
        elif game_data['bet_direction'] == InformedOddsQualCheck.prediction_away_win:
            bet_on_team = away_team_name
            back_lay = self.back_bet
        elif game_data['bet_direction'] == InformedOddsQualCheck.prediction_home_not_win:
            bet_on_team = home_team_name
            back_lay = self.lay_bet
        elif game_data['bet_direction'] == InformedOddsQualCheck.prediction_away_not_win:
            bet_on_team = away_team_name
            back_lay = self.lay_bet
        else:
            print('*** Wrong bet_direction! bet_direction = ' + game_data['bet_direction'] + ' ***')
            return

        # Add the BetFair commission and profit margin on top of the min_odds_to_bet_on
        price = self._round_up_odds (
            (bet_on_odds - 1)
            /
            (1-self.commission_rate)
            +
            1
        )
        return self._place_bet(
            home_team_name,
            away_team_name,
            bet_on_team,
            self.market_type_code_match_odds,
            betting_amount,
            price,
            debug_mode,
            back_lay
        )

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
                (bet_on_odds - 1)
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
                debug_mode,
                self.back_bet
            )
        return bet_placing_outcome

    def _unify_team_name(self, team_name):
        try:
            return self.team_names_mapping[team_name]
        except KeyError:
            return team_name
