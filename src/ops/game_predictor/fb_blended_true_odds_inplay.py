import collections
from src.utils.logger import OtLogger
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds as TrueOddsSuper

# This game predictor provides true odds only
class TrueOddsInplay(TrueOddsSuper):

    benchmark_bookie = 'pinnacle'
    strategy = 'to_inplay'
    profit_margin = 0.02 # This is to ensure we win something.
    profit_margin2 = 0.05
    profit_margin3 = 0.15
    profitChoice2List = list()
    profitChoice3List = list()
    leagueDivOne = list()
    leagueDivTwo = list()
    filter_bookies = list()

    def __init__(self, logger: OtLogger):
        super().__init__(logger)

        # we choose the following liquid bookmakers odds as our filter
        self.filter_bookies.append('pinnacle')
        self.filter_bookies.append('easybet')
        self.filter_bookies.append('betclick')
        self.filter_bookies.append('setantabet')
        self.filter_bookies.append('championsbet')
        self.filter_bookies.append('tipico')
        self.filter_bookies.append('boylesports')
        self.filter_bookies.append('sbobet')
        self.filter_bookies.append('betway')
        self.filter_bookies.append('will_hill')
        self.filter_bookies.append('betcity')
        self.filter_bookies.append('bodog')
        self.filter_bookies.append('betfred')
        self.filter_bookies.append('skybet')
        self.filter_bookies.append('snai')
        self.filter_bookies.append('dafabet')

        self.leagueDivOne.append(31) # Spain 1
        self.leagueDivOne.append(11) # France 1
        self.leagueDivOne.append(60) # Chinese Super League
        self.leagueDivOne.append(21) # USA Major League Soccer
        self.leagueDivOne.append(17) # Holland Jupiler League
        self.leagueDivOne.append(27) # Swiss Super League
        self.leagueDivOne.append(3) # Austria Leagie 1
        self.leagueDivOne.append(10) # Russia
        self.leagueDivOne.append(7) # Denmark Super League
        self.leagueDivOne.append(9) # German Bundesliga 2
        self.leagueDivOne.append(693) # German Bundesliga 3
        self.leagueDivOne.append(119) # Ukrainian Premier League
        self.leagueDivOne.append(6) # Poland Super League
        self.leagueDivOne.append(133) # Croatia Super League
        self.leagueDivOne.append(25) # J-League Division 1
        self.leagueDivOne.append(4) # Brazil A
        self.leagueDivOne.append(34) # Italian Serie A
        #self.leagueDivOne.append(12) # France Ligue 2
        self.leagueDivOne.append(35) # England League 2
        self.leagueDivOne.append(39) # England League 1
        self.leagueDivOne.append(30) # Turkish Super Liga
        self.leagueDivOne.append(36) # English Premier league
        self.leagueDivOne.append(8) # Germany 1
        self.leagueDivOne.append(13) # Finland
        self.leagueDivOne.append(16) # Holland Eredivisie
        self.leagueDivOne.append(26) # Sweden
        self.leagueDivOne.append(124) # Romanian Liga I
        self.leagueDivOne.append(29) # Scottish Premier League
        self.leagueDivOne.append(23) # Portugal Primera Liga
        self.leagueDivOne.append(37) # England Championship
        self.leagueDivOne.append(32) # Greece Super League
        self.leagueDivOne.append(33) # Spanish Segunda Division
        self.leagueDivOne.append(22) # Norwegian Tippeligaen
        self.leagueDivOne.append(157) # Portugal Segunda Liga
        self.leagueDivOne.append(150) # Scottish Championship
        self.leagueDivOne.append(136) # Hungary NB I
        self.leagueDivOne.append(103) # champions League
        self.leagueDivOne.append(84) # English League Cup
        self.leagueDivOne.append(146) # English Nation League
        self.leagueDivOne.append(221) # Poland League 1
        self.leagueDivOne.append(121) # Swiss Challenge League
        self.leagueDivOne.append(308) # South Africa Premier League
        self.leagueDivOne.append(321) # Morocco Pro 1
        self.leagueDivOne.append(122) # Sweden Superettan
        self.leagueDivOne.append(700) # Thai Premier League
        self.leagueDivOne.append(90) # England FA Cup
        self.leagueDivOne.append(81) # Spanish Copa
        self.leagueDivOne.append(15) # Korea League
        self.leagueDivOne.append(89) # Copa Libertadores
        self.leagueDivOne.append(165) # Northern Ireland Premier League

        self.leagueDivTwo.append(5) # Belgian Pro League
        self.leagueDivTwo.append(137) # Czech First League
        self.leagueDivTwo.append(284) # J-League Division 2
        self.leagueDivTwo.append(358) # Brazil Serie B
        self.leagueDivTwo.append(235) # Russia League 1
        self.leagueDivTwo.append(193) # Algeria
        self.leagueDivTwo.append(138) # Belgian Second Division
        self.leagueDivTwo.append(1) # Ireland Premier Division
        self.leagueDivTwo.append(140) # Mexico Primera Division
        self.leagueDivTwo.append(766) # Vietnam
        self.leagueDivTwo.append(113) # Europa League
        self.leagueDivTwo.append(40) # Italian Serie B
        self.leagueDivTwo.append(273) # Australia A-League

        #self.profitChoice2List.append(12) # France Ligue 2
        self.profitChoice2List.append(29) # Scottish Premier League
        self.profitChoice2List.append(23) # Portugal Primera Liga
        self.profitChoice2List.append(37) # England Championship
        self.profitChoice2List.append(32) # Greece Super League
        self.profitChoice2List.append(33) # Spanish Segunda Division
        self.profitChoice2List.append(22) # Norwegian Tippeligaen
        self.profitChoice2List.append(34) # Italian Serie A
        self.profitChoice2List.append(35) # England League 2
        self.profitChoice2List.append(39) # England League 1
        self.profitChoice2List.append(30) # Turkish Super Liga
        self.profitChoice2List.append(136) # Hungary NB I
        self.profitChoice2List.append(8) # Germany 1
        self.profitChoice2List.append(60) #  Chinese Super League
        self.profitChoice2List.append(4) # Brazil A
        self.profitChoice2List.append(17) # Holland Jupiler League
        self.profitChoice2List.append(27) # Swiss Super League
        self.profitChoice2List.append(10) # Russia
        self.profitChoice2List.append(16) # Holland Eredivisie
        self.profitChoice2List.append(3) # Austria Leagie 1
        self.profitChoice2List.append(7) # Denmark Super League
        self.profitChoice2List.append(9) # German Bundesliga 2
        self.profitChoice2List.append(693) # German Bundesliga 3
        self.profitChoice2List.append(119) # Ukrainian Premier League
        self.profitChoice2List.append(6) # Poland Super League
        self.profitChoice2List.append(133) # Croatia Super League
        self.profitChoice2List.append(25) # J-League Division 1
        self.profitChoice2List.append(13) # Finland
        self.profitChoice2List.append(157) # Portugal Segunda Liga
        self.profitChoice2List.append(150) # Scottish Championship
        self.profitChoice2List.append(84) # English League Cup
        self.profitChoice2List.append(146) # England National League
        self.profitChoice2List.append(235) # Russia League 1
        self.profitChoice2List.append(138) # Belgium Second Division
        self.profitChoice2List.append(140) # Mexico Primera Division
        self.profitChoice2List.append(1) # Ireland Premier Division
        self.profitChoice2List.append(308) # South Africa Premier League
        self.profitChoice2List.append(321) # Morocco Pro 1
        self.profitChoice2List.append(122) # Sweden Superettan
        self.profitChoice2List.append(700) # Thai Premier League
        self.profitChoice2List.append(766) # Vietnam
        self.profitChoice2List.append(15) # Korea League

        self.profitChoice3List.append(5) # Belgian Pro League
        self.profitChoice3List.append(137) # Czech First League
        self.profitChoice3List.append(284) # J-League Division 2
        self.profitChoice3List.append(358) # Brazil Serie B
        self.profitChoice3List.append(221) # Poland League 1
        self.profitChoice3List.append(113) # Europa League
        self.profitChoice3List.append(103) # champions League
        self.profitChoice3List.append(40) # Italian Serie B

    def FindOddsWithOffsetTime(self, game_data, bookie, lookbackTime):
        matchInSeq = collections.OrderedDict(sorted(game_data['odds'][bookie].items()))
        kickoffTime = int(game_data['kickoff'])
        lastRecord = []
        lastRecord.append(0)
        lastRecord.append(0)
        for timeStr, prob in matchInSeq.items():
            time = int(float(timeStr))
            if timeStr == "final" or timeStr == "open" or time > kickoffTime:
                continue
            if time <= kickoffTime - lookbackTime:
                if time > lastRecord[0]:
                    lastRecord[0] = time
            if time <= kickoffTime:
                if time > lastRecord[1]:
                    lastRecord[1] = time
        if lastRecord[1] != 0:
            game_data['odds'][bookie][str(int(game_data['kickoff']))] = game_data['odds'][bookie][str(int(lastRecord[1]))]
        if lastRecord[0] != 0:
            return game_data['odds'][bookie][str(int(lastRecord[0]))]
        else:
            return None

    def _calc_true_odds(self, data, localProfitMargin):
        picked_bookie = list()
        if data['league_id'] in self.leagueDivTwo:
            picked_bookie.append('pinnacle')
        elif data['league_id'] in self.leagueDivOne:
            picked_bookie.append('pinnacle')
            picked_bookie.append('bet365')
            picked_bookie.append('betvictor')
        else:
            return False
        local_list_home = []
        local_list_draw = []
        local_list_away = []
        compareBestOdds = [0, 0, 0]
        is_qualifed = False

        try:
            for bookie in picked_bookie:
                benchmark_odds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
                #benchmark_odds = self.FindOddsWithOffsetTime(data, bookie, 0)
                home = float(benchmark_odds['1'])
                draw = float(benchmark_odds['x'])
                away = float(benchmark_odds['2'])
                local_list_home.append(home)
                local_list_draw.append(draw)
                local_list_away.append(away)
            for bookie in self.filter_bookies:
                try:
                    compareOdds = list(collections.OrderedDict(sorted(data['odds'][bookie].items())).values())[-1]
                except (TypeError, KeyError):
                    compareOdds = {}
                    compareOdds['1'] = 1.0
                    compareOdds['x'] = 1.0
                    compareOdds['2'] = 1.0
                #compareOdds = self.FindOddsWithOffsetTime(data, bookie, 0)
                if float(compareOdds['1']) > compareBestOdds[0]:
                    compareBestOdds[0] = float(compareOdds['1'])
                if float(compareOdds['x']) > compareBestOdds[1]:
                    compareBestOdds[1] = float(compareOdds['x'])
                if float(compareOdds['2']) > compareBestOdds[2]:
                    compareBestOdds[2] = float(compareOdds['2'])
        except Exception as e:
            self.logger.log('Why is the game disqualified? - ' + str(e))
            return is_qualifed

        home = self._get_average(local_list_home)
        draw = self._get_average(local_list_draw)
        away = self._get_average(local_list_away)
        return_rate = home * draw * away / (home * draw + draw * away + home * away)
        while return_rate < 0.999999:
            home = (3 * home) / (3 - ((1 - return_rate) * home))
            draw = (3 * draw) / (3 - ((1 - return_rate) * draw))
            away = (3 * away) / (3 - ((1 - return_rate) * away))
            return_rate = home * draw * away / (home * draw + draw * away + home * away)
        true_odds = dict()
        localProfitMargin = self.profit_margin
        if data['league_id'] in self.profitChoice2List:
            localProfitMargin = self.profit_margin2
        if data['league_id'] in self.profitChoice3List:
            localProfitMargin = self.profit_margin3
        print(data['game_id'], local_list_home, local_list_draw, local_list_away, home, draw, away)
        home = home * (1 + localProfitMargin)
        draw = draw * (1 + localProfitMargin)
        away = away * (1 + localProfitMargin)

        # we only bet at calc true odds, when benchmark bookmaker odds is better than our calc ones
        # the reason we want to do this, is try to avoid adverse selection
        self.logger.log('CompareBestOdds: ' + str(compareBestOdds))
        self.logger.log('Calculated odds: home: ' + str(home) + ', draw: ' + str(draw) + ',  away: '+ str(away))
        if compareBestOdds[0] >= home:
            true_odds['1'] = home
            is_qualifed = True
        if compareBestOdds[1] >= draw:
            true_odds['x'] = draw
            is_qualifed = True
        if compareBestOdds[2] >= away:
            true_odds['2'] = away
            is_qualifed = True

        if is_qualifed:
            return true_odds
        else:
            return False
