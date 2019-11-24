from src.ops.game_predictor.bb_blended_true_odds import TrueOdds as TrueOddsSuper
from src.utils.logger import OtLogger

# This game predictor provides true odds only
class TrueOddsBetweenRange(TrueOddsSuper):
    strategy = 'to_odds_between_range'
    profit_margin = 0.02 # This is to ensure we win something.
    max_odds = 3
    min_odds = 1.2

    def _calc_true_odds(self, data, localProfitMargin):

        true_odds = self._calc_raw_true_odds(data, localProfitMargin)
        self.logger.debug('full true odds: ' + str(true_odds))
        if not self.min_odds <= true_odds['1'] <= self.max_odds:
            true_odds.pop('1')
        if not self.min_odds <= true_odds['2'] <= self.max_odds:
            true_odds.pop('2')

        # If not odds left:
        if not true_odds:
            self.logger.debug('game disqualified, max odds is: ' + str(self.max_odds) +
                              'mins odds is: ' + str(self.min_odds))
            return False

        return true_odds

if __name__ == '__main__':
    logger = OtLogger('../../../logs/ops_bb_true_odds.log')
    operator = TrueOddsBetweenRange(logger)

    data = {"game_id": 362311, "home_score": 91, "away_score": 123, "home_half_score": 41, "away_half_score": 62, "result": "2", "league_id": 1, "season": "2019-2020", "league_name": "National Basketball Association", "kickoff": 1572649800.0, "home_team_name": "Orlando Magic", "away_team_name": "Milwaukee Bucks", "home_team_id": 6, "away_team_id": 12, "odds": {"easybet": {"1572649260": {"1": "2.6", "2": "1.47"}, "1572649140": {"1": "2.5", "2": "1.5"}, "1572640740": {"1": "2.6", "2": "1.52"}, "1572638580": {"1": "2.46", "2": "1.57"}, "1572612180": {"1": "2.6", "2": "1.52"}, "1572607140": {"1": "2.7", "2": "1.49"}, "1572592200": {"1": "2.6", "2": "1.52"}, "1572591240": {"1": "2.7", "2": "1.49"}, "1572590040": {"1": "2.6", "2": "1.52"}, "1572587160": {"1": "2.7", "2": "1.49"}, "1572578640": {"1": "2.6", "2": "1.52"}, "1572578100": {"1": "2.6", "2": "1.53"}}, "pinnacle": {"1572648960": {"1": "2.63", "2": "1.55"}, "1572648720": {"1": "2.64", "2": "1.55"}, "1572646440": {"1": "2.62", "2": "1.55"}, "1572646200": {"1": "2.61", "2": "1.55"}, "1572643620": {"1": "2.6", "2": "1.56"}, "1572643500": {"1": "2.59", "2": "1.56"}, "1572642360": {"1": "2.6", "2": "1.56"}, "1572635040": {"1": "2.59", "2": "1.56"}, "1572632700": {"1": "2.6", "2": "1.56"}, "1572631320": {"1": "2.63", "2": "1.55"}, "1572630300": {"1": "2.64", "2": "1.55"}, "1572630180": {"1": "2.63", "2": "1.55"}, "1572629820": {"1": "2.64", "2": "1.55"}, "1572629700": {"1": "2.66", "2": "1.54"}, "1572627780": {"1": "2.65", "2": "1.54"}, "1572624420": {"1": "2.64", "2": "1.54"}, "1572622560": {"1": "2.64", "2": "1.55"}, "1572620220": {"1": "2.63", "2": "1.55"}, "1572619440": {"1": "2.62", "2": "1.55"}, "1572618540": {"1": "2.61", "2": "1.55"}, "1572617220": {"1": "2.61", "2": "1.56"}, "1572615240": {"1": "2.65", "2": "1.54"}, "1572614040": {"1": "2.64", "2": "1.54"}, "1572612300": {"1": "2.63", "2": "1.55"}, "1572608220": {"1": "2.62", "2": "1.55"}, "1572607020": {"1": "2.66", "2": "1.54"}, "1572604500": {"1": "2.63", "2": "1.55"}, "1572601500": {"1": "2.62", "2": "1.55"}, "1572599160": {"1": "2.6", "2": "1.56"}, "1572595560": {"1": "2.59", "2": "1.56"}, "1572594240": {"1": "2.58", "2": "1.57"}, "1572593940": {"1": "2.66", "2": "1.54"}, "1572586800": {"1": "2.69", "2": "1.53"}, "1572586380": {"1": "2.68", "2": "1.53"}, "1572584880": {"1": "2.67", "2": "1.53"}, "1572582300": {"1": "2.67", "2": "1.54"}, "1572573840": {"1": "2.64", "2": "1.55"}, "1572573720": {"1": "2.66", "2": "1.54"}, "1572561900": {"1": "2.72", "2": "1.52"}, "1572561300": {"1": "2.83", "2": "1.48"}, "1572558300": {"1": "2.83", "2": "1.49"}, "1572551280": {"1": "2.83", "2": "1.48"}, "1572551160": {"1": "2.88", "2": "1.47"}}, "will_hill": {"1572617580": {"1": "2.65", "2": "1.54"}, "1572617340": {"1": "2.55", "2": "1.57"}, "1572617160": {"1": "2.65", "2": "1.54"}, "1572614040": {"1": "2.7", "2": "1.53"}, "1572608100": {"1": "2.65", "2": "1.54"}, "1572607080": {"1": "2.7", "2": "1.53"}, "1572594300": {"1": "2.65", "2": "1.54"}, "1572569820": {"1": "2.7", "2": "1.53"}, "1572562860": {"1": "2.65", "2": "1.54"}, "1572561900": {"1": "2.7", "2": "1.53"}, "1572551640": {"1": "2.75", "2": "1.5"}, "1572551460": {"1": "2.85", "2": "1.47"}}, "coral": {"1572648900": {"1": "2.5", "2": "1.55"}, "1572645540": {"1": "2.45", "2": "1.57"}, "1572590940": {"1": "2.5", "2": "1.53"}, "1572570300": {"1": "2.63", "2": "1.5"}}, "Expekt": {"1572633300": {"1": "2.46", "2": "1.55"}, "1572626460": {"1": "2.51", "2": "1.53"}, "1572607920": {"1": "2.48", "2": "1.55"}, "1572595980": {"1": "2.43", "2": "1.57"}, "1572573840": {"1": "2.51", "2": "1.54"}, "1572562440": {"1": "2.56", "2": "1.52"}, "1572547080": {"1": "2.67", "2": "1.48"}}, "vcbet": {"1572649560": {"1": "2.7", "2": "1.533"}, "1572649140": {"1": "2.625", "2": "1.55"}, "1572648900": {"1": "2.6", "2": "1.55"}, "1572648780": {"1": "2.625", "2": "1.55"}, "1572648420": {"1": "2.6", "2": "1.55"}, "1572645720": {"1": "2.55", "2": "1.571"}, "1572633060": {"1": "2.5", "2": "1.55"}, "1572626160": {"1": "2.55", "2": "1.533"}, "1572607140": {"1": "2.5", "2": "1.55"}, "1572594480": {"1": "2.45", "2": "1.571"}, "1572573900": {"1": "2.55", "2": "1.533"}, "1572561900": {"1": "2.625", "2": "1.5"}, "1572546960": {"1": "2.75", "2": "1.45"}}, "Macauslot": {"1572585720": {"1": "2.5", "2": "1.45"}}, "BWin": {"1572648900": {"1": "2.5", "2": "1.55"}, "1572645540": {"1": "2.45", "2": "1.57"}, "1572590940": {"1": "2.55", "2": "1.53"}, "1572553740": {"1": "2.65", "2": "1.5"}}, "SB": {"1572649740": {"1": "2.28", "2": "1.56"}, "1572649380": {"1": "2.31", "2": "1.55"}, "1572648060": {"1": "2.55", "2": "1.55"}, "1572647340": {"1": "2.55", "2": "1.54"}, "1572646200": {"1": "2.46", "2": "1.58"}, "1572645300": {"1": "2.55", "2": "1.55"}, "1572638520": {"1": "2.46", "2": "1.58"}, "1572594420": {"1": "2.56", "2": "1.54"}, "1572594360": {"1": "2.44", "2": "1.58"}, "1572592440": {"1": "2.6", "2": "1.52"}, "1572591960": {"1": "2.56", "2": "1.54"}, "1572580920": {"1": "2.56", "2": "1.53"}}, "bet365": {"1572649020": {"1": "2.67", "2": "1.52"}, "1572635100": {"1": "2.6", "2": "1.55"}, "1572620340": {"1": "2.65", "2": "1.54"}, "1572618120": {"1": "2.6", "2": "1.55"}, "1572617280": {"1": "2.55", "2": "1.57"}, "1572594420": {"1": "2.6", "2": "1.55"}, "1572562020": {"1": "2.65", "2": "1.54"}, "1572561900": {"1": "2.67", "2": "1.52"}, "1572555720": {"1": "2.75", "2": "1.47"}}, "ChinaSlot": {"1572607260": {"1": "2.64", "2": "1.25"}, "1572583980": {"1": "2.52", "2": "1.28"}, "1572572460": {"1": "2.41", "2": "1.31"}}, "5Dimes": {"1572638640": {"1": "2.6", "2": "1.59"}, "1572619560": {"1": "2.65", "2": "1.57"}, "1572617640": {"1": "2.6", "2": "1.59"}, "1572570300": {"1": "2.7", "2": "1.54"}}, "Betfair": {"1572649080": {"1": "2.76", "2": "1.56"}, "1572648780": {"1": "2.78", "2": "1.55"}, "1572648660": {"1": "2.76", "2": "1.55"}, "1572648420": {"1": "2.74", "2": "1.55"}, "1572648300": {"1": "2.72", "2": "1.57"}, "1572648240": {"1": "2.74", "2": "1.57"}, "1572648120": {"1": "2.7", "2": "1.57"}, "1572648000": {"1": "2.74", "2": "1.57"}, "1572647760": {"1": "2.74", "2": "1.56"}, "1572647460": {"1": "2.74", "2": "1.57"}, "1572647220": {"1": "2.72", "2": "1.56"}, "1572646980": {"1": "2.76", "2": "1.56"}, "1572646680": {"1": "2.74", "2": "1.56"}, "1572646440": {"1": "2.76", "2": "1.56"}, "1572645900": {"1": "2.74", "2": "1.56"}, "1572645780": {"1": "2.72", "2": "1.57"}, "1572645540": {"1": "2.78", "2": "1.56"}, "1572644880": {"1": "2.72", "2": "1.56"}, "1572644700": {"1": "2.76", "2": "1.56"}, "1572644460": {"1": "2.74", "2": "1.56"}, "1572644340": {"1": "2.72", "2": "1.56"}, "1572643800": {"1": "2.74", "2": "1.56"}, "1572643560": {"1": "2.72", "2": "1.57"}, "1572643260": {"1": "2.74", "2": "1.56"}, "1572642900": {"1": "2.74", "2": "1.57"}, "1572642480": {"1": "2.68", "2": "1.58"}, "1572642240": {"1": "2.68", "2": "1.59"}, "1572642060": {"1": "2.64", "2": "1.59"}, "1572641820": {"1": "2.66", "2": "1.59"}, "1572640020": {"1": "2.64", "2": "1.59"}, "1572639840": {"1": "2.64", "2": "1.6"}, "1572639600": {"1": "2.64", "2": "1.59"}, "1572639540": {"1": "2.62", "2": "1.6"}, "1572638040": {"1": "2.66", "2": "1.59"}, "1572637380": {"1": "2.68", "2": "1.58"}, "1572636060": {"1": "2.66", "2": "1.59"}, "1572635400": {"1": "2.66", "2": "1.58"}, "1572633300": {"1": "2.68", "2": "1.58"}, "1572632580": {"1": "2.72", "2": "1.56"}, "1572630480": {"1": "2.72", "2": "1.57"}, "1572627060": {"1": "2.72", "2": "1.56"}, "1572626460": {"1": "2.74", "2": "1.56"}, "1572625140": {"1": "2.72", "2": "1.57"}, "1572622680": {"1": "2.7", "2": "1.57"}, "1572622020": {"1": "2.72", "2": "1.57"}, "1572620760": {"1": "2.7", "2": "1.57"}, "1572620100": {"1": "2.68", "2": "1.58"}, "1572619560": {"1": "2.7", "2": "1.57"}, "1572617640": {"1": "2.74", "2": "1.56"}, "1572615120": {"1": "2.78", "2": "1.55"}, "1572612960": {"1": "2.8", "2": "1.55"}, "1572609180": {"1": "2.78", "2": "1.55"}, "1572608520": {"1": "2.76", "2": "1.55"}, "1572606060": {"1": "2.76", "2": "1.56"}, "1572605400": {"1": "2.7", "2": "1.57"}, "1572602880": {"1": "2.68", "2": "1.58"}, "1572599100": {"1": "2.66", "2": "1.58"}, "1572597840": {"1": "2.72", "2": "1.57"}, "1572597240": {"1": "2.76", "2": "1.56"}, "1572595980": {"1": "2.72", "2": "1.57"}, "1572595320": {"1": "2.74", "2": "1.56"}, "1572594720": {"1": "2.72", "2": "1.57"}, "1572588360": {"1": "2.72", "2": "1.56"}, "1572587100": {"1": "2.68", "2": "1.56"}, "1572586500": {"1": "2.68", "2": "1.57"}, "1572585840": {"1": "2.66", "2": "1.56"}, "1572585240": {"1": "2.76", "2": "1.55"}, "1572582720": {"1": "2.74", "2": "1.55"}, "1572580200": {"1": "2.76", "2": "1.55"}, "1572575220": {"1": "2.8", "2": "1.55"}, "1572574560": {"1": "2.74", "2": "1.55"}, "1572573840": {"1": "2.74", "2": "1.54"}, "1572573180": {"1": "2.74", "2": "1.52"}, "1572572460": {"1": "2.74", "2": "1.49"}, "1572571800": {"1": "2.56", "2": "1.49"}, "1572570300": {"1": "2.6", "2": "1.47"}, "1572569640": {"1": "2.6", "2": "1.48"}, "1572565620": {"1": "2.74", "2": "1.46"}, "1572564600": {"1": "2.74", "2": "1.47"}, "1572560460": {"1": "2.74", "2": "1.46"}, "1572559860": {"1": "2.38", "2": "1.45"}}, "unibet": {"1572647340": {"1": "2.6", "2": "1.52"}, "1572647220": {"1": "2.7", "2": "1.5"}, "1572645780": {"1": "2.55", "2": "1.54"}, "1572641460": {"1": "2.5", "2": "1.56"}, "1572611700": {"1": "2.63", "2": "1.52"}, "1572606660": {"1": "2.5", "2": "1.56"}, "1572580200": {"1": "2.63", "2": "1.52"}, "1572558060": {"1": "2.8", "2": "1.47"}}, "ladbroke": {"1572645660": {"1": "2.45", "2": "1.57"}, "1572591000": {"1": "2.5", "2": "1.53"}, "1572553920": {"1": "2.62", "2": "1.5"}}, "matchbook": {"1572648900": {"1": "2.64", "2": "1.56"}, "1572648180": {"1": "2.65", "2": "1.56"}, "1572647520": {"1": "2.68", "2": "1.56"}, "1572646860": {"1": "2.67", "2": "1.56"}, "1572646140": {"1": "2.65", "2": "1.57"}, "1572645420": {"1": "2.63", "2": "1.57"}, "1572644760": {"1": "2.67", "2": "1.57"}, "1572644040": {"1": "2.67", "2": "1.58"}, "1572643380": {"1": "2.63", "2": "1.58"}, "1572641280": {"1": "2.62", "2": "1.58"}, "1572639840": {"1": "2.61", "2": "1.58"}, "1572638460": {"1": "2.62", "2": "1.57"}, "1572633780": {"1": "2.63", "2": "1.57"}, "1572632820": {"1": "2.75", "2": "1.56"}, "1572631680": {"1": "2.73", "2": "1.56"}, "1572628020": {"1": "2.67", "2": "1.56"}, "1572623820": {"1": "2.66", "2": "1.58"}, "1572621660": {"1": "2.66", "2": "1.56"}, "1572615180": {"1": "2.67", "2": "1.56"}, "1572602700": {"1": "2.64", "2": "1.56"}, "1572601200": {"1": "2.62", "2": "1.56"}, "1572599100": {"1": "2.62", "2": "1.57"}, "1572598440": {"1": "2.61", "2": "1.5"}, "1572597840": {"1": "2.61", "2": "1.57"}, "1572597240": {"1": "2.33", "2": "1.38"}, "1572595980": {"1": "2.18", "2": "1.42"}, "1572594720": {"1": "2.18", "2": "1.39"}, "1572590940": {"1": "2.18", "2": "1.56"}, "1572587760": {"1": "2.18", "2": "1.45"}}, "marathon": {"1572646560": {"1": "2.63", "2": "1.55"}, "1572633180": {"1": "2.6", "2": "1.56"}, "1572630300": {"1": "2.66", "2": "1.54"}, "1572629580": {"1": "2.68", "2": "1.53"}, "1572629100": {"1": "2.66", "2": "1.54"}, "1572628680": {"1": "2.68", "2": "1.53"}, "1572628140": {"1": "2.69", "2": "1.53"}, "1572626400": {"1": "2.68", "2": "1.53"}, "1572621360": {"1": "2.66", "2": "1.54"}, "1572617880": {"1": "2.63", "2": "1.55"}, "1572614340": {"1": "2.68", "2": "1.53"}, "1572609780": {"1": "2.66", "2": "1.54"}, "1572607320": {"1": "2.68", "2": "1.53"}, "1572602100": {"1": "2.63", "2": "1.55"}, "1572595620": {"1": "2.6", "2": "1.56"}, "1572594480": {"1": "2.69", "2": "1.53"}, "1572592680": {"1": "2.72", "2": "1.52"}, "1572592620": {"1": "2.66", "2": "1.54"}, "1572589140": {"1": "2.82", "2": "1.49"}, "1572574080": {"1": "2.78", "2": "1.5"}, "1572574020": {"1": "2.75", "2": "1.51"}, "1572563400": {"1": "2.78", "2": "1.5"}, "1572556920": {"1": "2.93", "2": "1.46"}, "1572552660": {"1": "2.97", "2": "1.45"}}, "skybet": {"1572562260": {"1": "2.5", "2": "1.5"}, "1572562140": {"1": "2.63", "2": "1.45"}, "1572562080": {"1": "2.5", "2": "1.5"}, "1572551280": {"1": "2.63", "2": "1.45"}}, "marathonbet": {"1572646860": {"1": "2.63", "2": "1.55"}, "1572633780": {"1": "2.6", "2": "1.56"}, "1572631680": {"1": "2.66", "2": "1.54"}, "1572628020": {"1": "2.68", "2": "1.53"}, "1572621660": {"1": "2.66", "2": "1.54"}, "1572608160": {"1": "2.68", "2": "1.53"}, "1572602700": {"1": "2.63", "2": "1.55"}, "1572599460": {"1": "2.6", "2": "1.56"}, "1572593460": {"1": "2.72", "2": "1.52"}, "1572590940": {"1": "2.82", "2": "1.49"}, "1572564600": {"1": "2.78", "2": "1.5"}, "1572556920": {"1": "2.93", "2": "1.46"}, "1572552660": {"1": "2.97", "2": "1.45"}}, "betvictor": {"1572546900": {"1": "2.75", "2": "1.45"}}}, "probabilities": {"easybet": {"1572649260": {"1": 0.3611793611793612, "2": 0.6388206388206389}, "1572649140": {"1": 0.375, "2": 0.625}, "1572640740": {"1": 0.3689320388349514, "2": 0.6310679611650486}, "1572638580": {"1": 0.3895781637717121, "2": 0.6104218362282877}, "1572612180": {"1": 0.3689320388349514, "2": 0.6310679611650486}, "1572607140": {"1": 0.3556085918854415, "2": 0.6443914081145585}, "1572592200": {"1": 0.3689320388349514, "2": 0.6310679611650486}, "1572591240": {"1": 0.3556085918854415, "2": 0.6443914081145585}, "1572590040": {"1": 0.3689320388349514, "2": 0.6310679611650486}, "1572587160": {"1": 0.3556085918854415, "2": 0.6443914081145585}, "1572578640": {"1": 0.3689320388349514, "2": 0.6310679611650486}, "1572578100": {"1": 0.37046004842615016, "2": 0.62953995157385}}, "pinnacle": {"1572648960": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572648720": {"1": 0.36992840095465396, "2": 0.630071599045346}, "1572646440": {"1": 0.37170263788968827, "2": 0.6282973621103118}, "1572646200": {"1": 0.37259615384615385, "2": 0.6274038461538461}, "1572643620": {"1": 0.375, "2": 0.625}, "1572643500": {"1": 0.3759036144578313, "2": 0.6240963855421686}, "1572642360": {"1": 0.375, "2": 0.625}, "1572635040": {"1": 0.3759036144578313, "2": 0.6240963855421686}, "1572632700": {"1": 0.375, "2": 0.625}, "1572631320": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572630300": {"1": 0.36992840095465396, "2": 0.630071599045346}, "1572630180": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572629820": {"1": 0.36992840095465396, "2": 0.630071599045346}, "1572629700": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572627780": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572624420": {"1": 0.3684210526315789, "2": 0.631578947368421}, "1572622560": {"1": 0.36992840095465396, "2": 0.630071599045346}, "1572620220": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572619440": {"1": 0.37170263788968827, "2": 0.6282973621103118}, "1572618540": {"1": 0.37259615384615385, "2": 0.6274038461538461}, "1572617220": {"1": 0.37410071942446044, "2": 0.6258992805755395}, "1572615240": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572614040": {"1": 0.3684210526315789, "2": 0.631578947368421}, "1572612300": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572608220": {"1": 0.37170263788968827, "2": 0.6282973621103118}, "1572607020": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572604500": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572601500": {"1": 0.37170263788968827, "2": 0.6282973621103118}, "1572599160": {"1": 0.375, "2": 0.625}, "1572595560": {"1": 0.3759036144578313, "2": 0.6240963855421686}, "1572594240": {"1": 0.3783132530120482, "2": 0.6216867469879519}, "1572593940": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572586800": {"1": 0.36255924170616116, "2": 0.6374407582938388}, "1572586380": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572584880": {"1": 0.3642857142857143, "2": 0.6357142857142858}, "1572582300": {"1": 0.3657957244655582, "2": 0.6342042755344418}, "1572573840": {"1": 0.36992840095465396, "2": 0.630071599045346}, "1572573720": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572561900": {"1": 0.35849056603773577, "2": 0.6415094339622641}, "1572561300": {"1": 0.3433874709976798, "2": 0.6566125290023201}, "1572558300": {"1": 0.34490740740740744, "2": 0.6550925925925927}, "1572551280": {"1": 0.3433874709976798, "2": 0.6566125290023201}, "1572551160": {"1": 0.33793103448275863, "2": 0.6620689655172414}}, "will_hill": {"1572617580": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572617340": {"1": 0.3810679611650486, "2": 0.6189320388349514}, "1572617160": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572614040": {"1": 0.36170212765957444, "2": 0.6382978723404256}, "1572608100": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572607080": {"1": 0.36170212765957444, "2": 0.6382978723404256}, "1572594300": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572569820": {"1": 0.36170212765957444, "2": 0.6382978723404256}, "1572562860": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572561900": {"1": 0.36170212765957444, "2": 0.6382978723404256}, "1572551640": {"1": 0.35294117647058826, "2": 0.6470588235294118}, "1572551460": {"1": 0.34027777777777773, "2": 0.6597222222222222}}, "coral": {"1572648900": {"1": 0.3827160493827161, "2": 0.6172839506172839}, "1572645540": {"1": 0.39054726368159204, "2": 0.609452736318408}, "1572590940": {"1": 0.3796526054590571, "2": 0.6203473945409429}, "1572570300": {"1": 0.36319612590799033, "2": 0.6368038740920097}}, "Expekt": {"1572633300": {"1": 0.38653366583541143, "2": 0.6134663341645885}, "1572626460": {"1": 0.37871287128712877, "2": 0.6212871287128713}, "1572607920": {"1": 0.38461538461538464, "2": 0.6153846153846154}, "1572595980": {"1": 0.39249999999999996, "2": 0.6074999999999999}, "1572573840": {"1": 0.3802469135802469, "2": 0.619753086419753}, "1572562440": {"1": 0.37254901960784315, "2": 0.6274509803921569}, "1572547080": {"1": 0.3566265060240964, "2": 0.6433734939759036}}, "vcbet": {"1572649560": {"1": 0.3621545003543586, "2": 0.6378454996456414}, "1572649140": {"1": 0.37125748502994016, "2": 0.62874251497006}, "1572648900": {"1": 0.3734939759036145, "2": 0.6265060240963857}, "1572648780": {"1": 0.37125748502994016, "2": 0.62874251497006}, "1572648420": {"1": 0.3734939759036145, "2": 0.6265060240963857}, "1572645720": {"1": 0.3812181509342393, "2": 0.6187818490657607}, "1572633060": {"1": 0.3827160493827161, "2": 0.6172839506172839}, "1572626160": {"1": 0.37545922116091107, "2": 0.6245407788390889}, "1572607140": {"1": 0.3827160493827161, "2": 0.6172839506172839}, "1572594480": {"1": 0.39069883113653314, "2": 0.6093011688634669}, "1572573900": {"1": 0.37545922116091107, "2": 0.6245407788390889}, "1572561900": {"1": 0.3636363636363637, "2": 0.6363636363636365}, "1572546960": {"1": 0.3452380952380952, "2": 0.6547619047619047}}, "Macauslot": {"1572585720": {"1": 0.3670886075949367, "2": 0.6329113924050633}}, "BWin": {"1572648900": {"1": 0.3827160493827161, "2": 0.6172839506172839}, "1572645540": {"1": 0.39054726368159204, "2": 0.609452736318408}, "1572590940": {"1": 0.375, "2": 0.625}, "1572553740": {"1": 0.3614457831325302, "2": 0.6385542168674698}}, "SB": {"1572649740": {"1": 0.40625000000000006, "2": 0.59375}, "1572649380": {"1": 0.40155440414507776, "2": 0.5984455958549223}, "1572648060": {"1": 0.37804878048780494, "2": 0.6219512195121951}, "1572647340": {"1": 0.3765281173594133, "2": 0.6234718826405868}, "1572646200": {"1": 0.39108910891089105, "2": 0.6089108910891088}, "1572645300": {"1": 0.37804878048780494, "2": 0.6219512195121951}, "1572638520": {"1": 0.39108910891089105, "2": 0.6089108910891088}, "1572594420": {"1": 0.375609756097561, "2": 0.624390243902439}, "1572594360": {"1": 0.39303482587064675, "2": 0.6069651741293531}, "1572592440": {"1": 0.3689320388349514, "2": 0.6310679611650486}, "1572591960": {"1": 0.375609756097561, "2": 0.624390243902439}, "1572580920": {"1": 0.37408312958435214, "2": 0.625916870415648}}, "bet365": {"1572649020": {"1": 0.3627684964200477, "2": 0.6372315035799523}, "1572635100": {"1": 0.3734939759036145, "2": 0.6265060240963857}, "1572620340": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572618120": {"1": 0.3734939759036145, "2": 0.6265060240963857}, "1572617280": {"1": 0.3810679611650486, "2": 0.6189320388349514}, "1572594420": {"1": 0.3734939759036145, "2": 0.6265060240963857}, "1572562020": {"1": 0.3675417661097853, "2": 0.6324582338902148}, "1572561900": {"1": 0.3627684964200477, "2": 0.6372315035799523}, "1572555720": {"1": 0.34834123222748814, "2": 0.6516587677725119}}, "ChinaSlot": {"1572607260": {"1": 0.3213367609254499, "2": 0.6786632390745502}, "1572583980": {"1": 0.3368421052631579, "2": 0.6631578947368422}, "1572572460": {"1": 0.3521505376344086, "2": 0.6478494623655915}}, "5Dimes": {"1572638640": {"1": 0.37947494033412893, "2": 0.6205250596658712}, "1572619560": {"1": 0.37203791469194314, "2": 0.6279620853080569}, "1572617640": {"1": 0.37947494033412893, "2": 0.6205250596658712}, "1572570300": {"1": 0.36320754716981135, "2": 0.6367924528301887}}, "Betfair": {"1572649080": {"1": 0.36111111111111116, "2": 0.6388888888888888}, "1572648780": {"1": 0.3579676674364896, "2": 0.6420323325635103}, "1572648660": {"1": 0.35962877030162416, "2": 0.6403712296983758}, "1572648420": {"1": 0.3613053613053613, "2": 0.6386946386946386}, "1572648300": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572648240": {"1": 0.36426914153132245, "2": 0.6357308584686774}, "1572648120": {"1": 0.36768149882903983, "2": 0.6323185011709602}, "1572648000": {"1": 0.36426914153132245, "2": 0.6357308584686774}, "1572647760": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572647460": {"1": 0.36426914153132245, "2": 0.6357308584686774}, "1572647220": {"1": 0.3644859813084112, "2": 0.6355140186915887}, "1572646980": {"1": 0.36111111111111116, "2": 0.6388888888888888}, "1572646680": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572646440": {"1": 0.36111111111111116, "2": 0.6388888888888888}, "1572645900": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572645780": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572645540": {"1": 0.359447004608295, "2": 0.6405529953917051}, "1572644880": {"1": 0.3644859813084112, "2": 0.6355140186915887}, "1572644700": {"1": 0.36111111111111116, "2": 0.6388888888888888}, "1572644460": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572644340": {"1": 0.3644859813084112, "2": 0.6355140186915887}, "1572643800": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572643560": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572643260": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572642900": {"1": 0.36426914153132245, "2": 0.6357308584686774}, "1572642480": {"1": 0.37089201877934275, "2": 0.6291079812206574}, "1572642240": {"1": 0.37236533957845436, "2": 0.6276346604215457}, "1572642060": {"1": 0.375886524822695, "2": 0.624113475177305}, "1572641820": {"1": 0.37411764705882355, "2": 0.6258823529411764}, "1572640020": {"1": 0.375886524822695, "2": 0.624113475177305}, "1572639840": {"1": 0.3773584905660377, "2": 0.6226415094339622}, "1572639600": {"1": 0.375886524822695, "2": 0.624113475177305}, "1572639540": {"1": 0.3791469194312796, "2": 0.6208530805687204}, "1572638040": {"1": 0.37411764705882355, "2": 0.6258823529411764}, "1572637380": {"1": 0.37089201877934275, "2": 0.6291079812206574}, "1572636060": {"1": 0.37411764705882355, "2": 0.6258823529411764}, "1572635400": {"1": 0.3726415094339623, "2": 0.6273584905660378}, "1572633300": {"1": 0.37089201877934275, "2": 0.6291079812206574}, "1572632580": {"1": 0.3644859813084112, "2": 0.6355140186915887}, "1572630480": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572627060": {"1": 0.3644859813084112, "2": 0.6355140186915887}, "1572626460": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572625140": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572622680": {"1": 0.36768149882903983, "2": 0.6323185011709602}, "1572622020": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572620760": {"1": 0.36768149882903983, "2": 0.6323185011709602}, "1572620100": {"1": 0.37089201877934275, "2": 0.6291079812206574}, "1572619560": {"1": 0.36768149882903983, "2": 0.6323185011709602}, "1572617640": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572615120": {"1": 0.3579676674364896, "2": 0.6420323325635103}, "1572612960": {"1": 0.3563218390804598, "2": 0.6436781609195402}, "1572609180": {"1": 0.3579676674364896, "2": 0.6420323325635103}, "1572608520": {"1": 0.35962877030162416, "2": 0.6403712296983758}, "1572606060": {"1": 0.36111111111111116, "2": 0.6388888888888888}, "1572605400": {"1": 0.36768149882903983, "2": 0.6323185011709602}, "1572602880": {"1": 0.37089201877934275, "2": 0.6291079812206574}, "1572599100": {"1": 0.3726415094339623, "2": 0.6273584905660378}, "1572597840": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572597240": {"1": 0.36111111111111116, "2": 0.6388888888888888}, "1572595980": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572595320": {"1": 0.3627906976744186, "2": 0.6372093023255814}, "1572594720": {"1": 0.36596736596736595, "2": 0.6340326340326341}, "1572588360": {"1": 0.3644859813084112, "2": 0.6355140186915887}, "1572587100": {"1": 0.36792452830188677, "2": 0.6320754716981132}, "1572586500": {"1": 0.3694117647058824, "2": 0.6305882352941177}, "1572585840": {"1": 0.3696682464454976, "2": 0.6303317535545023}, "1572585240": {"1": 0.35962877030162416, "2": 0.6403712296983758}, "1572582720": {"1": 0.3613053613053613, "2": 0.6386946386946386}, "1572580200": {"1": 0.35962877030162416, "2": 0.6403712296983758}, "1572575220": {"1": 0.3563218390804598, "2": 0.6436781609195402}, "1572574560": {"1": 0.3613053613053613, "2": 0.6386946386946386}, "1572573840": {"1": 0.3598130841121495, "2": 0.6401869158878505}, "1572573180": {"1": 0.3568075117370892, "2": 0.6431924882629109}, "1572572460": {"1": 0.3522458628841607, "2": 0.6477541371158392}, "1572571800": {"1": 0.36790123456790125, "2": 0.6320987654320989}, "1572570300": {"1": 0.3611793611793612, "2": 0.6388206388206389}, "1572569640": {"1": 0.3627450980392157, "2": 0.6372549019607844}, "1572565620": {"1": 0.34761904761904766, "2": 0.6523809523809524}, "1572564600": {"1": 0.34916864608076004, "2": 0.6508313539192399}, "1572560460": {"1": 0.34761904761904766, "2": 0.6523809523809524}, "1572559860": {"1": 0.37859007832898167, "2": 0.6214099216710183}}, "unibet": {"1572647340": {"1": 0.3689320388349514, "2": 0.6310679611650486}, "1572647220": {"1": 0.35714285714285715, "2": 0.6428571428571429}, "1572645780": {"1": 0.3765281173594133, "2": 0.6234718826405868}, "1572641460": {"1": 0.38423645320197053, "2": 0.6157635467980296}, "1572611700": {"1": 0.36626506024096384, "2": 0.633734939759036}, "1572606660": {"1": 0.38423645320197053, "2": 0.6157635467980296}, "1572580200": {"1": 0.36626506024096384, "2": 0.633734939759036}, "1572558060": {"1": 0.34426229508196726, "2": 0.6557377049180328}}, "ladbroke": {"1572645660": {"1": 0.39054726368159204, "2": 0.609452736318408}, "1572591000": {"1": 0.3796526054590571, "2": 0.6203473945409429}, "1572553920": {"1": 0.3640776699029127, "2": 0.6359223300970874}}, "matchbook": {"1572648900": {"1": 0.3714285714285714, "2": 0.6285714285714284}, "1572648180": {"1": 0.3705463182897863, "2": 0.6294536817102138}, "1572647520": {"1": 0.36792452830188677, "2": 0.6320754716981132}, "1572646860": {"1": 0.3687943262411348, "2": 0.6312056737588652}, "1572646140": {"1": 0.37203791469194314, "2": 0.6279620853080569}, "1572645420": {"1": 0.3738095238095238, "2": 0.6261904761904762}, "1572644760": {"1": 0.3702830188679246, "2": 0.6297169811320755}, "1572644040": {"1": 0.371764705882353, "2": 0.6282352941176471}, "1572643380": {"1": 0.3752969121140143, "2": 0.6247030878859857}, "1572641280": {"1": 0.37619047619047624, "2": 0.6238095238095239}, "1572639840": {"1": 0.3770883054892602, "2": 0.6229116945107398}, "1572638460": {"1": 0.3747016706443914, "2": 0.6252983293556087}, "1572633780": {"1": 0.3738095238095238, "2": 0.6261904761904762}, "1572632820": {"1": 0.3619489559164733, "2": 0.6380510440835265}, "1572631680": {"1": 0.36363636363636365, "2": 0.6363636363636364}, "1572628020": {"1": 0.3687943262411348, "2": 0.6312056737588652}, "1572623820": {"1": 0.3726415094339623, "2": 0.6273584905660378}, "1572621660": {"1": 0.3696682464454976, "2": 0.6303317535545023}, "1572615180": {"1": 0.3687943262411348, "2": 0.6312056737588652}, "1572602700": {"1": 0.3714285714285714, "2": 0.6285714285714284}, "1572601200": {"1": 0.37320574162679426, "2": 0.6267942583732058}, "1572599100": {"1": 0.3747016706443914, "2": 0.6252983293556087}, "1572598440": {"1": 0.36496350364963503, "2": 0.635036496350365}, "1572597840": {"1": 0.37559808612440193, "2": 0.6244019138755981}, "1572597240": {"1": 0.3719676549865229, "2": 0.6280323450134772}, "1572595980": {"1": 0.3944444444444444, "2": 0.6055555555555555}, "1572594720": {"1": 0.3893557422969187, "2": 0.6106442577030813}, "1572590940": {"1": 0.41711229946524064, "2": 0.5828877005347594}, "1572587760": {"1": 0.39944903581267216, "2": 0.6005509641873279}}, "marathon": {"1572646560": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572633180": {"1": 0.375, "2": 0.625}, "1572630300": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572629580": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572629100": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572628680": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572628140": {"1": 0.36255924170616116, "2": 0.6374407582938388}, "1572626400": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572621360": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572617880": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572614340": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572609780": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572607320": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572602100": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572595620": {"1": 0.375, "2": 0.625}, "1572594480": {"1": 0.36255924170616116, "2": 0.6374407582938388}, "1572592680": {"1": 0.35849056603773577, "2": 0.6415094339622641}, "1572592620": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572589140": {"1": 0.345707656612529, "2": 0.654292343387471}, "1572574080": {"1": 0.3504672897196262, "2": 0.6495327102803737}, "1572574020": {"1": 0.3544600938967136, "2": 0.6455399061032865}, "1572563400": {"1": 0.3504672897196262, "2": 0.6495327102803737}, "1572556920": {"1": 0.33257403189066065, "2": 0.6674259681093395}, "1572552660": {"1": 0.3280542986425339, "2": 0.6719457013574661}}, "skybet": {"1572562260": {"1": 0.375, "2": 0.625}, "1572562140": {"1": 0.35539215686274506, "2": 0.6446078431372548}, "1572562080": {"1": 0.375, "2": 0.625}, "1572551280": {"1": 0.35539215686274506, "2": 0.6446078431372548}}, "marathonbet": {"1572646860": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572633780": {"1": 0.375, "2": 0.625}, "1572631680": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572628020": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572621660": {"1": 0.36666666666666664, "2": 0.6333333333333333}, "1572608160": {"1": 0.36342042755344417, "2": 0.6365795724465559}, "1572602700": {"1": 0.37081339712918665, "2": 0.6291866028708134}, "1572599460": {"1": 0.375, "2": 0.625}, "1572593460": {"1": 0.35849056603773577, "2": 0.6415094339622641}, "1572590940": {"1": 0.345707656612529, "2": 0.654292343387471}, "1572564600": {"1": 0.3504672897196262, "2": 0.6495327102803737}, "1572556920": {"1": 0.33257403189066065, "2": 0.6674259681093395}, "1572552660": {"1": 0.3280542986425339, "2": 0.6719457013574661}}, "betvictor": {"1572546900": {"1": 0.3452380952380952, "2": 0.6547619047619047}}}}
    print(operator.get_prediction(data, 0.3))
