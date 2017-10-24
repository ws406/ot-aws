from win007.entities.game_odds import GameMainBookiesOdds


class decision_maker:
    def __init__(self):
        pass

    # This function takes the input data and makes a decision about whether this game is
    # qualified or not based on our strategy.
    #
    # The input data structure is illustrated in data_example.json file
    # The return is one of the three possibilites:
    # 1. None: nothing is qualified
    # 2. "1": home team is preferred
    # 3. "2": awa team is preferred
    def which_is_qualified(self, odds: GameMainBookiesOdds):

        pass