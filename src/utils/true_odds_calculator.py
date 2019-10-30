class TrueOddsCalculator:
    def __init__(self):
        pass

    def calculate_3_way_margin_prop(self, home, away, draw):
        margin = (1/home + 1/draw + 1/away) - 1

        home_fair = 3*home / (3-home*margin)
        away_fair = 3*away / (3-away*margin)
        draw_fair = 3*draw / (3-draw*margin)

        return home_fair, away_fair, draw_fair

    def calculate_2_way_margin_prop(self, home, away):
        margin = (1/home + 1/away) - 1

        home_fair = 2*home / (2-home*margin)
        away_fair = 2*away / (2-away*margin)

        return home_fair, away_fair

if __name__ == "__main__":
    trueOddsCalculator = TrueOddsCalculator()
    print(trueOddsCalculator.calculate_3_way_margin_prop(1.44, 4.42, 6.25))
    print(trueOddsCalculator.calculate_2_way_margin_prop(3.45, 1.38))
