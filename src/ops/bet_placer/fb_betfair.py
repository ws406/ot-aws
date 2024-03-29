from src.ops.bet_placer.betfair import Betfair
from src.ops.game_predictor.fb_blended_true_odds_2_lowest_odds import TrueOddsLower2
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds
from src.ops.game_predictor.fb_blended_true_odds2 import BlendTrueOdds
from src.ops.game_predictor.fb_blended_true_odds_away import BlendTrueAwayOdds
from src.ops.game_predictor.fb_blended_true_odds_home import BlendTrueHomeOdds
from src.ops.game_predictor.fb_blended_true_odds_inplay import TrueOddsInplay
from src.ops.game_predictor.fb_blended_true_odds_inplay2 import TrueOddsInplay2
from src.ops.game_predictor.fb_blended_true_odds_inplay3 import TrueOddsInplay3
from src.ops.game_predictor.fb_blended_true_odds_strong_team import TrueOddsStrongTeam

class FBBetfair(Betfair):

    event_type_id = 1
    market_type_code_match_odds = 'MATCH_ODDS'
    market_name = 'Match Odds'
    runner_name_draw = 'The Draw'
    team_names_mapping = {
        # EPL & EC
        'Tottenham Hotspur': 'Tottenham',
        'West Ham United': 'West Ham',
        'Brighton Hove Albion': 'Brighton',
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
        'Dagenham   Redbridge': 'Dag and Red',
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
        'Borussia Dortmund (Youth)': 'Dortmund II',
        'SC Verl' : 'Verl',
        'Te Cu Kukuh Atta Seip': 'SV Turkgucu-Ataspor',
        'Havelse': 'TSV Havelse',
        'SC Freiburg (Youth)': 'Freiburg II',

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
        'Vitoria BA': 'EC Vitoria Salvador',
        'Sampaio Correa': 'Sampaio Correa FC',
        'Nautico (PE)': 'Nautico PE',
        'Confianca SE': 'Confianca',

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
        'Nashville': 'Nashville SC',
        'Club Internacional de Futbol Miami': 'Inter Miami CF',

        # KOR 1
        'Jeju United': 'Jeju Utd',
        'Ulsan Hyundai FC': 'Ulsan Hyundai Horang-i',
        'Sangju Sangmu Phoenix': 'Sangju Sangmu',
        'Gyeongnam FC': 'Gyeongnam',
        'Suwon Samsung Bluewings': 'Suwon Bluewings',
        'Busan I Park': 'Busan IPark',
        'Gwangju Football Club': 'Gwangju FC',

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
        'Thespa Kusatsu': 'Thespakusatsu Gunma',
        'Giravanz Kitakyushu': 'Kitakyushu',

        # CHINA 1
        'Hebei FC': 'Hebei CFFC',
        'Chongqing Liangjiang Athletic': 'Chongqing Lifan',
        'Dalian Pro': 'Dalian Yifang',
        'Henan Songshan Longmen': 'Henan',
        'Guangzhou Fuli FC': 'Guangzhou R&F',
        'Tianjin Tigers': 'Tianjin Teda',
        'Guangzhou Evergrande Taobao FC': 'Guangzhou FC',
        'Jiangsu Suning FC': 'Jiangsu Suning',
        'Shenzhen JiaZhaoye': 'Shenzhen FC',
        'Wuhan FC': 'Wuhan Zall',
        'Shanghai Port': 'Shanghai East Asia',
        'Shandong Taishan': 'Shandong Luneng',
        'Qingdao FC': 'Qingdao Huanghai FC',
        'Cangzhou Mighty Lions': 'Shijiazhuang Yongchang FC',

        # Australia
        'Sydney FC': 'Sydney',
        'Adelaide United FC': 'Adelaide United',
        'Western Sydney': 'Western Sydney Wanderers',
        'Western United FC': 'Western United',
        'FC Macarthur': 'Macarthur FC',

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
        'Osters IF': 'Osters',
        'Varbergs BoIS FC': 'Varbergs BoIS',

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
        'Khimki': 'FC Khimki',
        'Krylya Sovetov': 'Kryliya Sovetov',
        'Akron Togliatti': 'Akron-L Togliatti',
        'Chertanovo Moscow': 'FK Chertanovo',
        'Baltika Kaliningrad': 'Baltika',
        'Veles': 'FK Veles Moscow',
        'Dinamo Briansk': 'Dinamo Bryansk',
        'FK Krasnodar II': 'Krasnodar II',
        'FK Nizhny Novgorod': 'FC Olimpiyets NN',
        'Torpedo moskva': 'FK Torpedo Moskva',
        'Tom Tomsk': 'Tomsk',
        'Tekstilshchik Ivanovo': 'Tekstilshchik',
        'SKA Khabarovsk': 'SKA-Khabarovsk',
        'Irtysh 1946 Omsk': 'FK Irtysh Omsk',
        'FK Chayka K-SR': 'FC Chayka',
        'Shinnik Yaroslavl': 'Shinnik',
        'Neftekhimik Nizhnekamsk': 'Neftekhimik',

        # Belgium 1
        'Mechelen': 'Yellow-Red Mechelen',
        'Standard Liege': 'Standard',
        'Mouscron Peruwelz': 'Royal Mouscron-Peruwelz',
        'Red Star Waasland': 'Waasland-Beveren',
        'Sint-Truidense': 'Sint Truiden',
        'Oostende': 'KV Oostende',
        'KAA Gent': 'Gent',
        'KAS Eupen': 'Eupen',
        'Royal Antwerp': 'Antwerp',
        'Racing Genk': 'Genk',
        'Oud Heverlee': 'Oud-Heverlee Leuven',
        'Beerschot Wilrijk': 'KFCO Beerschot Wilrijk',
        'Saint Gilloise': 'Union St Gilloise',
        'Seraing United': 'Seraing Utd',

        # France
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
        'Bastia Borgo': 'FC Bastia-Borgo',
        'USL Dunkerque': 'Dunkerque',
        'Pau FC': 'Pau',
        'Quevilly': 'Quevilly Rouen',
        'Sete FC': 'Sete',
        'Bourg Peronnas': 'Bourg-en-Bresse',
        'Cholet So': 'Cholet SO',
        'Villefranche': 'Villefranche Beaujolais',

        # Nor1
        'Sarpsborg 08': 'Sarpsborg',
        'Odd Grenland': 'Odds BK',
        'Tromso IL': 'Tromso',
        'Mjondalen IF': 'Mjondalen',
        'Kristiansund BK': 'Kristiansund',

        # Holland
        'AFC Ajax': 'Ajax',
        'Groningen': 'FC Groningen',
        'FC Twente Enschede': 'FC Twente',
        'PSV Eindhoven': 'PSV',
        'Heracles Almelo': 'Heracles',
        'SC Heerenveen': 'Heerenveen',
        'AZ Alkmaar': 'Az Alkmaar',
        'Dordrecht': 'FC Dordrecht',
        'SC Cambuur': 'Cambuur Leeuwarden',
        'Volendam': 'FC Volendam',
        'Almere City FC': 'Almere City',
        'Jong Ajax (Youth)': 'Jong Ajax Amsterdam',
        'FC Utrecht (Youth)': 'Jong FC Utrecht',
        'AZ Alkmaar (Youth)': 'Jong AZ Alkmaar',
        'Excelsior SBV' : 'Excelsior',
        'Jong PSV Eindhoven (Youth)' : 'Jong PSV Eindhoven',

        # Spain
        'FC Barcelona': 'Barcelona',
        'Real Valladolid': 'Valladolid',
        'Real Betis': 'Betis',
        'RCD Espanyol': 'Espanyol',
        'Granada CF': 'Granada',
        'Real Zaragoza': 'Zaragoza',
        'Deportivo La Coruna': 'Deportivo',
        'Real Oviedo': 'Oviedo',
        'AD Alcorcon': 'Alcorcon',
        'SD Huesca': 'Huesca',
        'CD Lugo': 'Lugo',
        'Extremadura': 'Extremadura UD',
        'Pena Azagresa': 'CD Pena Azagresa',
        'SD Laredo': 'CD Laredo',
        'UE Cornella': 'Cornella',
        'Gimnastic Tarragona': 'Gimnastic',
        'UE Olot': 'Olot',
        'CD Becerril': 'Becerril',
        'CD Linares Deportivo': 'Linares Deportivo',
        'Lorca Deportiva FC': 'Lorca Deportiva CF',
        'Alaves B': 'CD Alaves B',
        'SD Amorebieta': 'Amorebieta',
        'Calahorra': 'CD Calahorra',
        'Osasuna B': 'CA Osasuna II',
        'CF Salmantino': 'Salmantino',
        'CD Guijuelo': 'Guijuelo',
        'Real Union Irun': 'Real Union',
        'Haro Deportivo': 'Haro',
        'Cultural Leonesa': 'Leonesa',
        'RCD Espanyol B': 'Espanyol B',
        'Castellon': 'CD Castellon',
        'Granada CF B': 'Granada B',
        'Atletico Sanluqueno': 'Atletico Sanluqueno CF',
        'Sevilla Atletico': 'Sevilla B',
        'Merida AD': 'Merida',
        'Pontevedra': 'Pontevedra CF',
        'CF Internacional De Madrid': 'CF Internacional Madrid',
        'Celta vigo b': 'Celta Vigo B',
        'UD Melilla': 'Melilla UD',
        'Baleares': 'Atletico Baleares',
        'SCR Pena Deportiva': 'Santa Eulalia',
        'Atletico de Madrid B': 'Atletico Madrid II',
        'Las Rozas': 'CD Las Rozas',
        'coruxo FC': 'Coruxo',
        'UD San Sebastian Reyes': 'SS Reyes',
        'UD Ibiza': 'Ibiza Eivissa',
        'Union Langreo': 'UP Langreo',
        'Real Oviedo B': 'Real Oviedo II',
        'Marino luanco': 'Marino Luanco',
        'Sporting de Gijon B': 'Sporting Gijon B',
        'Las Palmas Atletico': 'UD Las Palmas II',
        'Burgos CF': 'Burgos',
        'Barakaldo CF': 'Barakaldo',
        'CD Tudelano': 'Tudelano',
        'Real Valladol B': 'Valladolid B',
        'UD Levante B': 'Atletico Levante UD',
        'AE Prat': 'Prat',
        'CF La Nucia': 'La Nucia',
        'Valencia CF Mestalla': 'Valencia-Mestalla',
        'CF Badalona': 'Badalona',
        'Real Balompedica Linense': 'Linense',
        'CF Talavera de la Reina': 'Talavera CF',
        'UD Marbella': 'Marbella',
        'C.D. San Fernando Isleno': 'San Fernando CD',
        'Badajoz': 'CD Badajoz',
        'Real Sociedad B': 'Sociedad B',

        # POR 1 && 2
        'Vitoria Setubal': 'Setubal',
        'Boavista FC': 'Boavista',
        'Sporting Braga': 'Braga',
        'FC Porto': 'Porto',
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
        'FC Famalicao': 'Famalicao',
        'FC Arouca': 'Arouca',
        'Clube Desportivo Trofense': 'CD Trofense',

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
        'Vaduz': 'FC Vaduz',
        'Stade Ouchy': 'Stade Lausanne-Ouchy',

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
        'Debrecin VSC': 'DEBRECENI VSC',
        'Ferencvarosi TC': 'Ferencvaros',
        'ZalaegerzsegTE': 'Zalaegerszeg',
        'Diosgyor VTK': 'Diosgyori',
        'Budapest Honved': 'Honved',
        'Paksi SE Honlapja': 'Paks',
        'Mezokovesd Zsory': 'Mezokovesd-Zsory',
        'Videoton Puskas Akademia': 'Puskas Akademia',
        'Fehervar Videoton': 'MOL Vidi',
        'Varda SE': 'Kisvarda',
        'Dafuji cloth MTE': 'Budafoki',
        'Ujpesti': 'Ujpest',
        'MTK Hungaria': 'MTK Budapest',
        'Gyirmot SE': 'Gyirmot',

        # Croatia
        'ZNK Osijek': 'Osijek',
        'NK Varteks Varazdin': 'Varazdin',
        'Istra 1961 Pula': 'NK Istra',
        'NK Lokomotiva Zagreb': 'Lokomotiva',
        'Slaven Koprivnica': 'Slaven Belupo',
        'HNK Sibenik': 'Sibenik',

        # Turkey
        'Besiktas JK': 'Besiktas',
        'Yeni Malatyaspor': 'Malatyaspor',
        'Caykur Rizespor': 'Rizespor',
        'Gaziantep Buyuksehir Belediyesi': 'Gaziantep FK',
        'Istanbul Buyuksehir Belediyesi': 'Basaksehir',
        'Karagumruk': 'Fatih Karagumruk Istanbul',
        'Menemen Belediye Spor': 'Menemen Belediyespor',
        'Manisa BB Spor': 'Manisa FK',

        # Romania
        'CS Universitatea Craiova': 'Universitatea Craiova',
        'Universitatea Craiova': 'FC U Craiova 1948',
        'Sepsi': 'ACS Sepsi OSK',
        'AFC Hermannstadt': 'Hermannstadt',
        'Dinamo Bucuresti': 'Dinamo Bucharest',
        'FC Astra Giurgiu': 'Astra Giurgiu',
        'CS Voluntari': 'FC Voluntari',
        'FC Viitorul Constanta': 'Viitorul Constanta',
        'Politehnica Iasi': 'CSMS Iasi',
        'Steaua Bucuresti': 'FCSB',
        'FC Clinceni': 'Academica Clinceni',
        'SCM Argesul Pitesti': 'Arges Pitesti',
        'FC UT Arad': 'UTA Arad',

        # Finland
        'Vaasa VPS': 'VPS',
        'Honka Espoo': 'Honka',
        'SJK Seinajoen': 'SJK',
        'Inter Turku': 'FC Inter',
        'Ilves Tampere': 'Ilves',
        'RoPS Rovaniemi': 'RoPS',
        'KuPs': 'KuPS',
        'TPS Turku': 'TPS',
        'FC Haka': 'Haka',

        # Greece
        'SKODA Xanthi': 'Xanthi',
        'Panaitolikos Agrinio': 'Panaitolikos',
        'OFI Crete': 'OFI',
        'Atromitos Athens': 'Atromitos',
        'Aris Thessaloniki': 'Aris',
        'Volos NFC': 'NFC Volos',
        'PAOK Saloniki': 'PAOK',
        'Pas Giannina': 'PAS Giannina',

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
        'Atletico San Luis': 'San Luis',
        'CDSyC Cruz Azul': 'Cruz Azul',
        'Club Tijuana': 'Tijuana',
        'Tigres UANL': 'Tigres',
        'Pumas U.N.A.M.': 'Pumas UNAM',
        'Chivas Guadalajara': 'Guadalajara',
        'Club Leon': 'Leon',
        'Queretaro FC': 'Querétaro',

        # Northen Irish
        'Institute FC': 'Institute',
        'Warrenpoint Town': 'Warrenpoint',
        'Glentoran FC': 'Glentoran',
        'Linfield FC': 'Linfield',
        'Ballymena United': 'Ballymena',
        'Glenavon Lurgan': 'Glenavon',
        'Dungannon Swifts': 'Dungannon',
        'Larne FC': 'Larne',

        # Egypt
        'FC Masr': 'Masr Club',
        'Al-Ittihad Alexandria': 'Al Ittihad (EGY)',
        'Talaea EI-Gaish': 'El Geish',
        'Misr Elmaqasah': 'Misr El Makasa',
        'EL Ahly': 'Al Ahly Cairo',
        'Aswan': 'Aswan FC',
        'Haras El Hedoud': 'Haras El Hodood',
        'EL Masry': 'Al-Masry',
        'El Mokawloon El Arab': 'Al Mokawloon',
        'Smouha SC' : 'Smouha',
        'Wadi Degla SC': 'Wadi Degla',
        'Pyramids FC': 'Pyramids',
        'Enppi': 'ENPPI',
        'El Entag Al Harby': 'El Entag El Harby',
        'Ceramica Cleopatra FC': 'Ceramica Cleopatra',
        'NBE SC': 'National Bank',

        # Poland
        'Jagiellonia Bialystok': 'Jagiellonia Bialystock',
        'Podbeskidzie Bielsko-Biala': 'Podbeskidzie B-B',
        'Legia Warszawa': 'Legia Warsaw',

        # Ireland
        'Waterford United': 'Waterford',
        'St. Patricks Athletic': 'St Patricks',

        # VietNam & Thailand
        'The Cong': 'Viettel FC',
        'Sai Gon FC': 'Sai Gon',
        'SHB Da Nang': 'Shb Da Nang',
        'XM Hai Phong FC': 'Hai Phong',
        'Than Quang Ninh': 'Quang Ninh',
        'Becamex Binh Duong': 'Binh Duong',
        'T T Hanoi': 'Ha Noi T and T',
        'CLB TPHCM': 'Ho Chi Minh City',
        'Nam Dinh FC': 'Nam Dinh',
        'Ratchaburi FC': 'Ratchaburi',
        'Muang Thong United': 'Muangthong Utd',
        'Chonburi Shark FC': 'Chonburi',
        'BEC Tero Sasana': 'Police Tero',
        'Trat FC': 'Trat',
        'Chiangrai United': 'Chiangrai Utd',
        'Buriram United': 'Buriram Utd',
        'Suphanburi FC': 'Suphanburi',
        'Bangkok United FC': 'Bangkok Utd',
        'Prachuap Khiri Khan': 'Prachuap',
        'Bangkok Glass': 'BG Pathumthani United',
        'Samut Prakan City': 'Samut Prakan',

         # Europe
        'Omonia Nicosia FC': 'Omonia',
        'Ludogorets Razgrad': 'Ludogorets',
        'Qarabag': 'Qarabag FK',
        'LASK Linz': 'Lask Linz',
        'Maccabi Petah Tikva FC': 'Maccabi Petach Tikva',
        'Hapoel Hadera': 'Hapoel Eran Hadera',
        'Ashdod MS': 'FC Ashdod',
        'Hapoel Natzrat Illit': 'Hapoel Nof HaGalil',
        'Hapoel Bnei Sakhnin FC': 'Bnei Sakhnin',

        'Liverpool URU': 'Liverpool Montevideo',
        'Deportes Tolima': 'Tolima',
        'CA River Plate': 'River Plate (Uru)',
        'Defensa Y Justicia': 'Defensa y Justicia',
        'Estudiantes Merida FC': 'Estudiantes de Merida',
        'FBC Melgar': 'Melgar',
        'Caracas FC': 'Caracas',
        'CA Penarol': 'Penarol',
        'Sol de America': 'Sol de America (Par)',
        'Univ Catolica': 'Univ Catolica (Chile)',
        'Club Sport Emelec': 'Emelec',
        'Independiente': 'CA Independiente',
        'Atletico Junior Barranquilla': 'CD Junior',
    }

    def place_match_odds_bet(self, game_data, betting_amount, debug_mode=False):

        strategy = game_data['strategy']

        if strategy == TrueOddsInplay.strategy or strategy == TrueOddsStrongTeam.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, self.persistence_persist, debug_mode)
        elif strategy == TrueOddsLower2.strategy or strategy == TrueOdds.strategy or strategy == BlendTrueOdds.strategy or strategy == TrueOddsInplay2.strategy or strategy == TrueOddsInplay3.strategy or strategy == BlendTrueHomeOdds.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, self.persistence_lapse, debug_mode)
        elif strategy == BlendTrueAwayOdds.strategy:
            return self._place_bet_for_true_odds(game_data, betting_amount, self.persistence_lapse, debug_mode, False)
        else:
            # Add other strategies later
            # bet_on_team = home_team_name if game_data['preferred_team'] == 'home' else away_team_name
            self.logger.exception('*** No strategy is found. Skip placing bets. ***')
            pass

    def _place_bet_for_true_odds(self, game_data, betting_amount, persistence, debug_mode, betOnHome = True):
        home_team_name = self._unify_team_name(game_data['home_team_name'])
        away_team_name = self._unify_team_name(game_data['away_team_name'])
        strategy = game_data['strategy']

        bet_placing_outcome = dict()
        # self.logger.log(game_data)

        for key, bet_on_odds in game_data['true_odds'].items():
            if key == '1':
                if game_data['side'] == "BACK":
                    bet_type = self.back_bet
                    amount = betting_amount
                    price = self._round_up_odds(bet_on_odds)
                elif game_data['side'] == "LAY":
                    bet_type = self.lay_bet
                    amount = self._round_up_amount(betting_amount / (float(list(game_data['odds'].values())[0]) - 1))
                    price = self._round_down_odds(bet_on_odds)
                if betOnHome:
                    bet_on_team = home_team_name
                else:
                    bet_on_team = away_team_name
            elif key == '-1':
                bet_type = self.lay_bet
                if betOnHome:
                    bet_on_team = home_team_name
                else:
                    bet_on_team = away_team_name
                lay_odds = 1.0 + 1.0 / (bet_on_odds - 1.0) # convert it to lay odds
                price = self._round_down_odds(lay_odds) # round lay odds to proper tick
                amount = self._round_up_amount(betting_amount / (price - 1))
            elif key == '2':
                if game_data['side'] == "BACK":
                    bet_type = self.back_bet
                    amount = betting_amount
                    price = self._round_up_odds(bet_on_odds)
                elif game_data['side'] == "LAY":
                    bet_type = self.lay_bet
                    amount = self._round_up_amount(betting_amount / (float(list(game_data['odds'].values())[0]) - 1))
                    price = self._round_down_odds(bet_on_odds)
                bet_on_team = away_team_name
            elif key == 'x':
                bet_type = self.back_bet
                amount = betting_amount
                price = self._round_up_odds(bet_on_odds)
                bet_on_team = self.runner_name_draw
            else:
                self.logger.exception('*** Wrong key! key = ' + key + ' ***')
                continue

            self.logger.log(bet_on_team + ' ' + bet_type + ' ' + str(price) + ' ' + str(amount))
            bet_placing_outcome[key] = self._place_bet (
                home_team_name,
                away_team_name,
                bet_on_team,
                self.market_type_code_match_odds,
                amount,
                price,
                debug_mode,
                bet_type,
                strategy,
                persistence
            )
        return bet_placing_outcome

    def _unify_team_name(self, team_name):
        try:
            return self.team_names_mapping[team_name]
        except KeyError:
            return team_name
