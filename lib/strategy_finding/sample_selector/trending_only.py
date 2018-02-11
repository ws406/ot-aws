from lib.strategy_finding.sample_selector.interface import SampleSelectorInterface


class TrendingOnlySelector(SampleSelectorInterface):

    def get_selected_games_data(self, raw_data: dict):
        print("Running game selector - TrendingOnlySelector")
        pass
