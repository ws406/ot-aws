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
        self.filter_leagues.append(3)
        self.filter_leagues.append(10)
        self.filter_leagues.append(119)
        self.filter_leagues.append(16)
        self.filter_leagues.append(146)
        self.filter_leagues.append(137)
        self.filter_leagues.append(12)
        self.filter_leagues.append(29)
        self.filter_leagues.append(113)

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
        picked_bookie.append('ladbroke')
        picked_bookie.append('betvictor')
        local_list_home = []
        local_list_draw = []
        local_list_away = []
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

        self.logger.log('Calculated odds: home: ' + str(home) + ', draw: ' + str(draw) + ',  away: '+ str(away))
        if home <= 7:
            true_odds['1'] = home
            is_qualifed = True
        if draw <= 7:
            true_odds['x'] = draw
            is_qualifed = True
        if away <= 7:
            true_odds['2'] = away
            is_qualifed = True

        if is_qualifed:
            return true_odds
        else:
            return False
