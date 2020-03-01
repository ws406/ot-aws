import collections
from src.utils.logger import OtLogger
from src.ops.game_predictor.fb_blended_true_odds import TrueOdds as TrueOddsSuper

# This game predictor provides true odds only
class TrueOddsInplay2(TrueOddsSuper):

    benchmark_bookie = 'pinnacle'
    strategy = 'to_inplay2'
    profit_margin = 0.02
    filter_bookies = list()
    filter_leagues = list()

    def __init__(self, logger: OtLogger):
        super().__init__(logger)

        # we choose the following liquid bookmakers odds as our filter
        self.filter_bookies.append('setantabet')
        self.filter_bookies.append('tipico')
        self.filter_bookies.append('betway')
        self.filter_bookies.append('betfred')
        self.filter_bookies.append('snai')
        self.filter_bookies.append('bovada')
        self.filter_bookies.append('bwin')
        self.filter_bookies.append('cashpoint')
        self.filter_bookies.append('betfair')

        self.filter_leagues.append(31)
        self.filter_leagues.append(11)
        self.filter_leagues.append(16)
        self.filter_leagues.append(25)
        self.filter_leagues.append(3)
        self.filter_leagues.append(157)
        self.filter_leagues.append(124)
        self.filter_leagues.append(192)
        self.filter_leagues.append(193)
        self.filter_leagues.append(119)
        self.filter_leagues.append(27)
        self.filter_leagues.append(235)
        self.filter_leagues.append(30)
        self.filter_leagues.append(136)
        self.filter_leagues.append(35)
        self.filter_leagues.append(8)
        self.filter_leagues.append(273)
        self.filter_leagues.append(140)
        self.filter_leagues.append(26)
        self.filter_leagues.append(122)
        self.filter_leagues.append(263)
        self.filter_leagues.append(103)
        self.filter_leagues.append(766)
        self.filter_leagues.append(21)

    def FindOddsWithOffsetTime(self, game_data, bookie, lookbackTime, lookbackCheck, backTime = 12.0):
        kickoffTime = int(game_data['kickoff'])
        if lookbackCheck:
            lastUpdateTime = int(list(collections.OrderedDict(sorted(game_data['odds'][bookie].items())).keys())[-1])
            if lastUpdateTime < kickoffTime - backTime * 60 * 60:
                return None
        matchInSeq = collections.OrderedDict(sorted(game_data['odds'][bookie].items()))
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
            game_data['odds'][bookie][int(game_data['kickoff'])] = game_data['odds'][bookie][int(lastRecord[1])]
        if lastRecord[0] != 0:
            return game_data['odds'][bookie][int(lastRecord[0])]
        else:
            return None

    def _calc_true_odds(self, data, localProfitMargin):
        picked_bookie = list()
        picked_bookie.append('pinnacle')
        picked_bookie.append('bet365')
        picked_bookie.append('betvictor')
        local_list_home = []
        local_list_draw = []
        local_list_away = []
        compareBestOdds = [0, 0, 0]
        is_qualifed = False
        if data['league_id'] not in self.filter_leagues:
            return is_qualifed
        try:
            for bookie in picked_bookie:
                benchmark_odds = None
                try:
                    benchmark_odds = self.FindOddsWithOffsetTime(data, bookie, 0, False)
                except (TypeError, KeyError):
                    continue
                if benchmark_odds == None:
                    continue
                home = float(benchmark_odds['1'])
                draw = float(benchmark_odds['x'])
                away = float(benchmark_odds['2'])
                local_list_home.append(home)
                local_list_draw.append(draw)
                local_list_away.append(away)
            if len(local_list_home) < len(picked_bookie):
                return is_qualifed
            for bookie in self.filter_bookies:
                try:
                    compareOdds = self.FindOddsWithOffsetTime(data, bookie, 0, False)
                except (TypeError, KeyError):
                    compareOdds = {}
                    compareOdds['1'] = 1.0
                    compareOdds['x'] = 1.0
                    compareOdds['2'] = 1.0
                if compareOdds == None:
                    compareOdds = {}
                    compareOdds['1'] = 1.0
                    compareOdds['x'] = 1.0
                    compareOdds['2'] = 1.0
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
