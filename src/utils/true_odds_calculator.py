class TrueOddsCalculator:
    def __init__(self):
        pass

    def calculate_3_way_margin_prop(self, home, away, draw):
        return_rate = home * draw * away / (home * draw + draw * away + home * away)
        while return_rate < 0.999999:
            home = (3 * home) / (3 - ((1 - return_rate) * home))
            draw = (3 * draw) / (3 - ((1 - return_rate) * draw))
            away = (3 * away) / (3 - ((1 - return_rate) * away))
            return_rate = home * draw * away / (home * draw + draw * away + home * away)
        return home, away, draw

    def calculate_2_way_margin_prop(self, home, away):
        return_rate = 1 / ( 1 / home + 1 / away)
        while returnRate < 0.999999:
            home = (2 * home) / (2 - ((1 - return_rate) * home))
            away = (2 * away) / (2 - ((1 - return_rate) * away))
            return_rate = 1 / ( 1 / home + 1 / away)
        return home, away

if __name__ == "__main__":
    trueOddsCalculator = TrueOddsCalculator()
    print(trueOddsCalculator.calculate_3_way_margin_prop(1.44, 4.42, 6.25))
    print(trueOddsCalculator.calculate_2_way_margin_prop(3.45, 1.38))
