from src.ops.bet_placer.betfair import Betfair
from src.ops.game_predictor.fb_blended_true_odds_2_lowest_odds import TrueOddsLower2
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
from src.ops.game_predictor.fb_blended_true_odds_inplay import TrueOddsInplay


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
        'Crystal Palace': 'Crystal Palace',
        'Newcastle United': 'Newcastle',
        'Manchester City': 'Man City',
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
        'Nottingham Forest': 'Nottm Forest',
        'West Bromwich(WBA)': 'West Brom',

        'Leeds United': 'Leeds',
        'Huddersfield Town': 'Huddersfield',
        'Derby County': 'Derby',

        # England League 1
        'Accrington Stanley': 'Accrington',
        'Bolton Wanderers': 'Bolton',
        'Sunderland A.F.C': 'Sunderland',
        'Doncaster Rovers': 'Doncaster',
        'Peterborough United': 'Peterborough',
        'Ipswich Town': 'Ipswich',
        'Lincoln City': 'Lincoln',
        'Oxford United': 'Oxford Utd',
        'Milton Keynes Dons': 'MK Dons',
        'Southend United': 'Southend',
        'Rotherham United': 'Rotherham',
        'Shrewsbury Town': 'Shrewsbury',
        'Tranmere Rovers': 'Tranmere',
        'Burton Albion': 'Burton',
        'Wycombe Wanderers': 'Wycombe',
        'Coventry City': 'Coventry',

        # England League 2
        'Bradford City': 'Bradford',
        'Carlisle United': 'Carlisle',
        'Cambridge United': 'Cambridge Utd',
        'Swindon Town': 'Swindon',
        'Colchester United': 'Colchester',
        'Crewe Alexandra': 'Crewe',
        'Forest Green Rovers': 'Forest Green',
        'Stevenage Borough': 'Stevenage',
        'Grimsby Town': 'Grimsby',
        'Macclesfield Town': 'Macclesfield',
        'Exeter City': 'Exeter',
        'Northampton Town': 'Northampton',
        'Oldham Athletic': 'Oldham',
        'Plymouth Argyle': 'Plymouth',
        'Cheltenham Town': 'Cheltenham',
        'Mansfield Town': 'Mansfield',
        'Scunthorpe United': 'Scunthorpe',

        # England Nation League
        'Yeovil Town': 'Yeovil',
        'Aldershot Town': 'Aldershot',
        'Stockport County': 'Stockport',
        'Chorley FC': 'Chorley',
        'Dover Athletic': 'Dover',
        'Ebbsfleet United': 'Ebbsfleet Utd',
        'Halifax Town': 'FC Halifax Town',
        'Notts County': 'Notts Co',
        'Hartlepool United': 'Hartlepool',
        'Dagenham Redbridge': 'Dag and Red',
        'Maidenhead United': 'Maidenhead',
        'Sutton United': 'Sutton Utd',
        'Torquay United': 'Torquay',
        'AFC Telford United': 'Telford',
        'Curzon Ashton FC': 'Curzon Ashton',
        'Boston United': 'Boston Utd',
        'Kettering Town': 'Kettering',
        'Chester FC': 'Chester',
        'Southport FC': 'Southport',
        'Hereford United': 'Hereford FC',
        'Kidderminster Harriers': 'Kidderminster',
        'Bradford Park Avenue': 'Bradford PA',
        'Gloucester City': 'Gloucester',
        'Braintree Town': 'Braintree',
        'Chelmsford City': 'Chelmsford',
        'Chippenham Town': 'Chippenham',
        'Hemel Hempstead Town': 'Hemel Hempstead',
        'St Albans City': 'St Albans',
        'Hungerford Town': 'Hungerford',
        'Maidstone United': 'Maidstone Utd',
        'Havant   Waterlooville': 'Havant and W',
        'Eastbourne Borough': 'Eastbourne',
        'Dorking': 'Dorking Wanderers',
        'Welling United': 'Welling Utd',
        'Wealdstone FC': 'Wealdstone',
        'Hampton Richmond Borough': 'Hampton and Richmond',

        # Scot 1 && 2
        'Saint Mirren': 'St Mirren',
        'Saint Johnstone': 'St Johnstone',
        'Celtic FC': 'Celtic',
        'Glasgow Rangers': 'Rangers',
        'Heart of Midlothian': 'Hearts',
        'Hamilton Academical': 'Hamilton',
        'Ross County': 'Ross Co',
        'Dundee United': 'Dundee Utd',
        'Ayr United': 'Ayr',
        'Alloa Athletic': 'Alloa',
        'Dunfermline Athletic': 'Dunfermline',
        'Greenock Morton': 'Morton',
        'Partick Thistle': 'Partick',
        'Inverness': 'Inverness CT',

        # GE 1 & 2 & 3
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
        'TSV 1860 Munchen': '1860 Munich',
        'MSV Duisburg': 'Duisburg',
        'Preuben Munster': 'Preussen Munster',
        'Eintracht Braunschweig': 'Braunschweig',
        'Uerdingen KFC 05': 'Uerdingen',
        'Magdeburg': 'FC Magdeburg',
        'SV Waldhof Mannheim': 'Waldhof Mannheim',
        'Zwickau': 'FSV Zwickau',
        'SG Sonnenhof Grossaspach': 'SG Sonnenhof',
        'Viktoria koln': 'Viktoria Koln',
        'Bayern Munchen (Youth)': 'Bayern Munich II',

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
        'Fortaleza': 'Fortaleza EC',
        'Internacional RS': 'Internacional',
        'Cruzeiro (MG)': 'Cruzeiro MG',
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

        # Australia
        'Sydney FC': 'Sydney',
        'Adelaide United FC': 'Adelaide United',
        'Western Sydney': 'Western Sydney Wanderers',
        'Western United FC': 'Western United',

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

        # Spain
        'SD Amorebieta': 'Amorebieta',
        'Badajoz': 'CD Badajoz',
        'Pena Azagresa': 'CD Pena Azagresa',
        'Cultural Leonesa': 'Leonesa',
        'Las Rozas': 'CD Las Rozas',
        'SCR Pena Deportiva': 'Santa Eulalia',
        'Haro Deportivo': 'Haro',
        'SD Laredo': 'CD Laredo',
        'UE Cornella': 'Cornella',
        'Gimnastic Tarragona': 'Gimnastic',
        'UE Olot': 'Olot',
        'Merida AD': 'Merida',
        'CF La Nucia': 'La Nucia',
        'CD Becerril': 'Becerril',
        'CD Linares Deportivo': 'Linares Deportivo',
        'Lorca Deportiva FC': 'Lorca Deportiva CF',

        # POR 1 && 2
        'Vitoria Setubal': 'Setubal',
        'Boavista FC': 'Boavista',
        'Sporting Braga': 'Braga',
        'FC Porto': 'Porto',
        'Rio Ave': 'Aves',
        'Vitoria Guimaraes': 'Guimaraes',
        'Pacos de Ferreira': 'Pacos Ferreira',
        'CD Tondela': 'Tondela',
        'Viseu': 'Academico de Viseu',
        'Cova Piedade': 'Cova da Piedade',
        'GD Chaves': 'Chaves',
        'SL Benfica B': 'Benfica B',
        'Estoril': 'Estoril Praia',
        'Nacional da Madeira': 'CD Nacional Funchal',
        'Casa Pia AC': 'Casa Pia',
        'CD Mafra': 'Mafra',
        'Academica Coimbra': 'Academica',
        'SC Covilha': 'Covilha',
        'SC Farense': 'Farense',

        # IT 1
        'Inter Milan': 'Inter',
        'AS Roma': 'Roma',

        # IT 2
        'Pordenone Calcio SSD' : 'Pordenone',
        'ACD Virtus Entella' : 'Entella',
        'Cosenza Calcio 1914': 'Cosenza',
        'Cremonese': 'US Cremonese',

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

        # Romania
        'CS Universitatea Craiova': 'Universitatea Craiova',
        'Sepsi': 'ACS Sepsi OSK',
        'AFC Hermannstadt': 'Hermannstadt',
        'Dinamo Bucuresti': 'Dinamo Bucharest',
        'FC Astra Giurgiu': 'Astra Giurgiu',
        'CS Voluntari': 'FC Voluntari',
        'FC Viitorul Constanta': 'Viitorul Constanta',
        'Politehnica Iasi': 'CSMS Iasi',
        'Steaua Bucuresti': 'FCSB',
        'FC Clinceni': 'Academica Clinceni',

        # Finland
        'Vaasa VPS': 'VPS',
        'Honka Espoo': 'Honka',
        'SJK Seinajoen': 'SJK',
        'Inter Turku': 'FC Inter',
        'Ilves Tampere': 'Ilves',
        'RoPS Rovaniemi': 'RoPS',
        'KuPs': 'KuPS',

        # Greece
        'SKODA Xanthi': 'Xanthi',
        'Panaitolikos Agrinio': 'Panaitolikos',
        'OFI Crete': 'OFI',
        'Atromitos Athens': 'Atromitos',
        'Aris Thessaloniki': 'Aris',
        'Volos NFC': 'NFC Volos',
        'PAOK Saloniki': 'PAOK',

        # Morocco
        'Raja Casablanca Atlhletic': 'Raja Casablanca',
        'Renaissance Zmamra': 'Club R Zemamra',
        'IRT Itihad de Tanger': 'IRT Tanger',
        'Hassania Agadir': 'HUSA Agadir',
        'RCOZ Oued Zem': 'Rapide Club Oued Zem',
        'Raja de Beni Mellal': 'Raja Beni Mellal',
        'MCO Mouloudia Oujda': 'Mouloudia dOujda',
        'DHJ Difaa Hassani Jadidi': 'DHJ El Jadida',
        'Olympique de Safi': 'Olympic Safi',
        'Union Touarga Sport Rabat': 'FUS Rabat',
        'Maghrib Association Tetouan': 'Moghreb Athletic Tetouan',
        'Renaissance Sportive de Berkane': 'RSB Berkane',
        'OCK Olympique de Khouribga': 'Olympique Khouribga',

        # Mexico
        'Club America': 'CF America',

        # Northen Irish
        'Institute FC': 'Institute',
        'Warrenpoint Town': 'Warrenpoint',
        'Glentoran FC': 'Glentoran',
        'Linfield FC': 'Linfield',
        'Ballymena United': 'Ballymena',
        'Glenavon Lurgan': 'Glenavon',
        'Dungannon Swifts': 'Dungannon',
        'Larne FC': 'Larne',
    }

    def place_match_odds_bet(self, game_data, betting_amount, debug_mode=False):

        strategy = game_data['strategy']

        if strategy == TrueOddsInplay.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, self.persistence_persist, debug_mode)
        elif strategy == TrueOddsLower2.strategy or strategy == TrueOdds.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, self.persistence_lapse, debug_mode)
        else:
            # Add other strategies later
            # bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
            self.logger.exception('*** No strategy is found. Skip placing bets. ***')
            pass

    def _place_bet_for_true_odds(self, game_data, betting_amount, persistence, debug_mode):
        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])
        strategy = game_data['strategy']

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
                self.back_bet,
                strategy,
                persistence
            )
        return bet_placing_outcome

    def _unify_team_name(self, team_name):
        try:
            return self.team_names_mapping[team_name]
        except KeyError:
            return team_name
