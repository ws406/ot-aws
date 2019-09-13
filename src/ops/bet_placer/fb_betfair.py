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
        # EPL & EC
        'Tottenham Hotspur': 'Tottenham',
        'West Ham United' : 'West Ham',
        'Brighton   Hove Albion': 'Brighton',
        'Leicester City': 'Leicester',
        'Norwich City': 'Norwich',
        'Crystal Palace': 'C Palace',
        'Newcastle United': 'Newcastle',
        'Manchester City': 'Manchester',
        'Sheffield United': 'Sheff Utd',
        'Manchester United': 'Man Utd',
        'Bournemouth AFC': 'Bournemouth',

        'Wigan Athletic': 'Wigan',
        'Luton Town': 'Luton',
        'Cardiff City': 'Cardiff',
        'Stoke City': 'Stoke',
        'Queens Park Rangers (QPR)': 'QPR',
        'Blackburn Rovers': 'Blackburn',
        'Charlton Athletic': 'Charlton',
        'Birmingham City': 'Birmingham',
        'Sheffield Wednesday': 'Sheff Wed',
        'Swansea City': 'Swansea',
        'Hull City': 'Hull',
        'Preston North End': 'Preston',
        'Sunderland A.F.C': 'Sunderland',
        'Oxford United': 'Oxford Utd',
        'Wycombe Wanderers': 'Wycombe',
        'Bolton Wanderers': 'Bolton',
        'Nottingham Forest': 'Nottm Forest',
        'West Bromwich(WBA)': 'West Brom',

        'Stevenage Borough': 'Stevenage',
        'Rotherham United': 'Rotherham',
        'Peterborough United': 'Peterborough',
        'Shrewsbury Town': 'Shrewsbury',
        'Coventry City': 'Coventry',
        'Southend United': 'Southend',
        'Milton Keynes Dons': 'MK Dons',
        'Exeter City': 'Exeter',
        'Macclesfield Town': 'Macclesfield',
        'Mansfield Town': 'Mansfield',
        'Lincoln City': 'Lincoln',
        'Accrington Stanley': 'Accrington',
        'Burton Albion': 'Burton',
        'Ipswich Town': 'Ipswich',
        'Doncaster Rovers': 'Doncaster',
        'Tranmere Rovers': 'Tranmere',
        'Leeds United': 'Leeds',
        'Huddersfield Town': 'Huddersfield',
        'Derby County': 'Derby',

        # Scot 1
        'Saint Mirren': 'St Mirren',
        'Saint Johnstone': 'St Johnstone',
        'Celtic FC': 'Celtic',
        'Glasgow Rangers': 'Rangers',
        'Heart of Midlothian': 'Hearts',
        'Hamilton Academical': 'Hamilton',
        'Ross County': 'Ross Co',

        # GE 1 & 2
        'TSG Hoffenheim': 'Hoffenheim',
        'Bayer Leverkusen': 'Leverkusen',
        'Darmstadt': 'SV Darmstadt',
        'Erzgebirge Aue': 'Erzgebirge',
        'VfL Bochum': 'Bochum',
        'SV Wehen Wiesbaden': 'Wehen Wiesbaden',
        'Karlsruher SC': 'Karlsruhe',
        'St. Pauli': 'St Pauli',
        'Hannover 96': 'Hannover',
        'Heidenheimer': 'FC Heidenheim',
        'VfB Stuttgart': 'Stuttgart',
        'Bayern Munchen': 'Bayern Munich',
        'VfL Wolfsburg': 'Wolfsburg',
        'SC Freiburg': 'Freiburg',
        'FSV Mainz 05': 'Mainz',
        'Borussia Dortmund': 'Dortmund',
        'Borussia Monchengladbach': 'Mgladbach',
        'SC Paderborn 07': 'Paderborn',

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
        'Cruzeiro (MG)': 'Cruzeiro',
        'Atletico Paranaense': 'Atletico PR',
        'Chapecoense SC': 'Chapecoense',
        'Bahia BA': 'Bahia',
        'Botafogo RJ': 'Botafogo',
        'Avai FC SC': 'Avai',
        'Corinthians Paulista (SP)': 'Corinthians',
        'Atletico Mineiro': 'Atletico MG',
        'CRB AL': 'CRB',
        'Centro Sportivo Alagoano': 'CSA',
        'Gremio (RS)': 'Gremio',

        # USA
        'Atlanta United': 'Atlanta Utd',
        'New England Revolution': 'New England',
        'Columbus Crew': 'Columbus',
        'DC United': 'DC Utd',
        'Minnesota United FC': 'Minnesota Utd',
        'Philadelphia Union': 'Philadelphia',
        'Colorado Rapids': 'Colorado',
        'New York City Football Club': 'New York City',
        'FC Kansas City': 'Kansas City',

        # KOR 1
        'Jeju United': 'Jeju Utd',
        'Ulsan Hyundai FC': 'Ulsan Hyundai Horang-i',
        'Sangju Sangmu Phoenix': 'Sangju Sangmu',
        'Gyeongnam FC': 'Gyeongnam',
        'Suwon Samsung Bluewings': 'Suwon Bluewings',

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
        'Yokohama Marinos': 'Yokohama FM',
        'Shimizu S-Pulse': 'Shimizu',
        'Hiroshima Sanfrecce': 'Hiroshima',
        'Consadole Sapporo': 'Sapporo',
        'Shonan Bellmare': 'Shonan',
        'Kashima Antlers': 'Kashima',
        'Vegalta Sendai': 'Sendai',
        'Jubilo Iwata': 'Iwata',
        'Cerezo Osaka': 'C-Osaka',
        'Urawa Red Diamonds': 'Urawa',
        'Nagoya Grampus': 'Nagoya',
        'Matsumoto Yamaga FC': 'Matsumoto',
        'Sagan Tosu': 'Tosu',

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
        'IK Sirius FK': 'Sirius',
        'AIK Solna': 'AIK',
        'GIF Sundsvall': 'Sundsvall',
        'AFC Eskilstuna': 'AFC Utd',
        'Falkenberg': 'Falkenbergs',
        'IFK Norrkoping FK': 'Norrkoping',
        'Helsingborg': 'Helsingborgs',
        'Kalmar': 'Kalmar FF',

        # Russian Super League
        'Spartak Tambov': 'FK Tambov',
        'FK Sochi': 'Sochi',
        'FC Krasnodar': 'FK Krasnodar',
        'Gazovik Orenburg': 'FC Orenburg',
        'Zenit St. Petersburg': 'Zenit St Petersburg',
        'Rostov FK': 'Rostov',
        'Lokomotiv Moscow': 'Lokomotiv',
        'Ural Sverdlovsk Oblast': 'Ural',
        'Dynamo Moscow': 'Dinamo Moscow',
        'Terek Grozny': 'Akhmat Grozny',

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
        'Racing Genk': 'Genk',

        # FR 1 & 2
        'AJ Auxerre': 'Auxerre',
        'Troyes': 'ESTAC Troyes',
        'Ajaccio': 'AC Ajaccio',
        'Rodez Aveyron': 'Rodez',
        'Chamois Niortais': 'Niort',
        'Orleans US 45': 'Orleans',
        'Chambly FC': 'Chambly Oise',
        'Stade Brestois': 'Brest',
        'Saint Etienne': 'St Etienne',
        'Paris Saint Germain (PSG)': 'Paris St-G',

        # Nor1
        'Sarpsborg 08': 'Sarpsborg',
        'Odd Grenland': 'Odds BK',
        'Tromso IL': 'Tromso',
        'Mjondalen IF': 'Mjondalen',
        'Kristiansund BK': 'Kristiansund',

        # HO 1
        'AFC Ajax': 'Ajax',
        'Groningen': 'FC GRONINGEN',
        'FC Twente Enschede': 'FC Twente',
        'PSV Eindhoven': 'PSV',
        'Heracles Almelo': 'Heracles',
        'SC Heerenveen': 'Heerenveen',
        'AZ Alkmaar': 'Az Alkmaar',
        'Jong PSV Eindhoven (Youth)': 'Jong PSV Eindhoven',

        # HO 2
        'Dordrecht': 'FC Dordrecht',
        'SC Cambuur': 'Cambuur Leeuwarden',
        'Volendam': 'FC Volendam',
        'Almere City FC': 'Almere City',
        'Jong Ajax (Youth)': 'Jong Ajax Amsterdam',
        'FC Utrecht (Youth)': 'Jong FC Utrecht',
        'AZ Alkmaar (Youth)': 'Jong AZ Alkmaar',
        'Excelsior SBV' : 'Excelsior',
        'Jong PSV Eindhoven (Youth)' : 'Jong PSV Eindhoven',

        # PO 1
        'FC Famalicao': 'Famalicao',
        'Legia Warszawa': 'Legia Warsaw',


        # ES 1
        'FC Barcelona': 'Barcelona',
        'Real Valladolid': 'Valladolid',
        'Real Betis': 'Betis',
        'RCD Espanyol': 'Espanyol',
        'Real Sociedad': 'Sociedad',
        'Granada CF': 'Granada',

        # ES 2
        'Real Zaragoza': 'Zaragoza',
        'Deportivo La Coruna': 'Deportivo',
        'Real Oviedo': 'Oviedo',
        'AD Alcorcon': 'Alcorcon',
        'SD Huesca': 'Huesca',
        'CD Lugo': 'Lugo',
        'Extremadura': 'Extremadura UD',

        # POR 1
        'Vitoria Setubal': 'Setubal',
        'Boavista FC': 'Boavista',
        'Sporting Braga': 'Braga',
        'FC Porto': 'Porto',
        'Rio Ave': 'Aves',
        'Vitoria Guimaraes': 'Guimaraes',
        'Pacos de Ferreira': 'Pacos Ferreira',

        # IT 1
        'Inter Milan': 'Inter',
        'AS Roma': 'Roma',

        # IT 2
        'Pordenone Calcio SSD' : 'Pordenone',
        'ACD Virtus Entella' : 'Entella',

        # DEN 1
        'Randers FC': 'Randers',
        'Odense BK': 'OB',
        'Brondby IF': 'Brondby',
        'Nordsjaelland': 'FC Nordsjaelland',
        'Aarhus AGF': 'AGF',
        'Sonderjyske': 'SonderjyskE',
        'Aalborg': 'AaB',

        # Swiss
        'St. Gallen': 'St Gallen',
        'Basel': 'FC Basel',
        'FC Sion': 'Sion',

        # Austria
        'Austria Wien': 'Austria Vienna',
        'Trenkwalder Admira Wacker': 'Admira Wacker',
        'Rapid Wien': 'Rapid Vienna',
        'TSV Hartberg': 'Hartberg',
        'Rheindorf Altach': 'SCR Altach',
        'St.Polten': 'St Polten',

        # Ukrain
        'FC Shakhtar Donetsk': 'Shakhtar',
        'FC Karpaty Lviv': 'Karpaty',
        'Olimpic Donetsk': 'Olimpik Donetsk',
        'PFC Oleksandria': 'Oleksandria',
        'Dynamo Kyiv': 'Dynamo Kiev',
        'Desna Chernihiv': 'FK Desna Chernihiv',
        'FC Vorskla Poltava': 'Vorskla',

        # Czech
        'Sparta Praha': 'Sparta Prague',
        'Baumit Jablonec': 'FK Jablonec',
        'FC Viktoria Plzen': 'Plzen',
        'Slavia Praha': 'Slavia Prague',
        'Synot Slovacko': 'Slovacko',
        'Tescoma Zlin': 'Zlin',
        'Dynamo Ceske Budejovice': 'Ceske Budejovice',
        'Opava': 'SFC Opava',
        'Marila Pribram': 'Pribram',

        # Hungary:
        'Debrecin VSC': 'Debrecen',
        'Ferencvarosi TC': 'Ferencvaros',
        'ZalaegerzsegTE': 'Zalaegerszeg',
        'Diosgyor VTK': 'Diosgyori',
        'Budapest Honved': 'Honved',
        'Paksi SE Honlapja': 'Paks',
        'Mezokovesd Zsory': 'Mezokovesd-Zsory',
        'Videoton Puskas Akademia': 'PUSKAS AKADEMIA',
        'Fehervar Videoton': 'MOL Vidi',
        'Varda SE': 'Kisvarda',

        # Croatia
        'ZNK Osijek': 'Osijek',
        'NK Varteks Varazdin': 'Varazdin',
        'Istra 1961 Pula': 'NK Istra',
        'NK Lokomotiva Zagreb': 'Lokomotiva',
        'Slaven Koprivnica': 'Slaven Belupo',

        # Turkey
        'Besiktas JK': 'Besiktas',
        'Yeni Malatyaspor': 'Malatyaspor',
        'Caykur Rizespor': 'Rizespor',
        'Gaziantep Buyuksehir Belediyesi': 'Gaziantep FK',
        'Istanbul Buyuksehir Belediyesi': 'Basaksehir',
    }

    def place_match_odds_bet(self, game_data, betting_amount, debug_mode=False):

        if game_data['strategy'] == TrueOdds.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, debug_mode)
        elif game_data['strategy'] == InformedOdds.strategy:
            return self._place_bet_for_informed_odds(game_data, betting_amount, debug_mode)
        else:
            # Add other strategies later
            # bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
            self.logger.exception('*** No strategy is found. Skip placing bets. ***')
            pass

    def _place_bet_for_informed_odds(self, game_data, betting_amount, debug_mode):
        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])
        bet_on_odds = game_data['bet_odds']

        # Add the BetFair commission and profit margin on top of the min_odds_to_bet_on
        price = self._round_up_odds (
            (bet_on_odds - 1)
            /
            (1-self.commission_rate)
            +
            1
        )

        amount = betting_amount

        if game_data['bet_direction'] == InformedOddsQualCheck.prediction_home_win:
            bet_on_team = home_team_name
            back_lay = self.back_bet

        elif game_data['bet_direction'] == InformedOddsQualCheck.prediction_away_win:
            bet_on_team = away_team_name
            back_lay = self.back_bet
        elif game_data['bet_direction'] == InformedOddsQualCheck.prediction_home_not_win:
            bet_on_team = home_team_name
            back_lay = self.lay_bet
            # for laybet: winning = liability / (odds - 1), while liability = betting_amount
            amount = round(betting_amount / (price - 1), 2)
        elif game_data['bet_direction'] == InformedOddsQualCheck.prediction_away_not_win:
            bet_on_team = away_team_name
            back_lay = self.lay_bet
            amount = round(betting_amount / (price - 1), 2)
        else:
            self.logger.exception('*** Wrong bet_direction! bet_direction = ' + game_data['bet_direction'] + ' ***')
            return

        return self._place_bet(
            home_team_name,
            away_team_name,
            bet_on_team,
            self.market_type_code_match_odds,
            amount,
            price,
            debug_mode,
            back_lay
        )

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
            elif key == 'x':
                bet_on_team = self.runner_name_draw
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
