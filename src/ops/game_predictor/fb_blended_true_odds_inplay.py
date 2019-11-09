import collections
from src.utils.logger import OtLogger
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds as TrueOddsSuper

# This game predictor provides true odds only
class TrueOddsInplay(TrueOddsSuper):

    benchmark_bookie = 'pinnacle'
    strategy = 'to_inplay'
    profit_margin = 0.02 # This is to ensure we win something.
    profit_margin2 = 0.01
    profitChoice2List = list()
    leagueDivTwo = list()
    leagueDivThree = list()
    leagueDivFour = list()
    filter_bookies = list()

    def __init__(self, logger: OtLogger):
        super().__init__(logger)

        # we choose the following liquid bookmakers odds as our filter
        self.filter_bookies.append('pinnacle')
        self.filter_bookies.append('bet365')
        self.filter_bookies.append('sb')
        self.filter_bookies.append('sbobet')
        self.filter_bookies.append('easybet')
        self.filter_bookies.append('betclick')
        self.filter_bookies.append('skybet')
        self.filter_bookies.append('coral')


        self.leagueDivTwo.append(36) # English Premier league
        self.leagueDivTwo.append(8) # Germany 1

        self.leagueDivThree.append(5) # Belgium 1
        self.leagueDivThree.append(13) # Finland
        self.leagueDivThree.append(4) # Brazil A
        self.leagueDivThree.append(358) # Brazil B

        self.leagueDivFour.append(26) # Sweden

        self.profitChoice2List.append(12)
        self.profitChoice2List.append(29)
        self.profitChoice2List.append(34)


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
            picked_bookie.append('betvictor')
        elif data['league_id'] in self.leagueDivThree:
            picked_bookie.append('pinnacle')
            picked_bookie.append('bet365')
            picked_bookie.append('betvictor')
            picked_bookie.append('sb')
        elif data['league_id'] in self.leagueDivFour:
            picked_bookie.append('pinnacle')
        else:
            picked_bookie.append('pinnacle')
            picked_bookie.append('bet365')
            picked_bookie.append('betvictor')
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
            #self.logger.log('missing odds - ' + str(e))
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
        if data['league_id'] in self.profitChoice2List:
            localProfitMargin = self.profit_margin2
        home = home * (1 + localProfitMargin)
        draw = draw * (1 + localProfitMargin)
        away = away * (1 + localProfitMargin)

        # we only bet at calc true odds, when benchmark bookmaker odds is better than our calc ones
        # the reason we want to do this, is try to avoid adverse selection
        #self.logger.log(str(data['game_id']), 'compareBestOdds: ')
        #self.logger.log(compareBestOdds)
        #self.logger.log('home: ' + str(home) + ', draw: ' + str(draw) + ',  away: '+ str(away))
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
