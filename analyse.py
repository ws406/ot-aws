from lib.strategy_finding.analyser import Analyser
from lib.strategy_finding.sample_selector.trending_only import TrendingOnlySelector
from lib.strategy_finding.data_labeler.dnb_win_only import DnbWinOnly
from lib.strategy_finding.feature_builder.wdl_probabilities import WDLProbabilitiesFeatureBuilder
from lib.strategy_finding.algorithm.random_forest import RandomForestAlgorithm

path_to_dir = 'data/test/'
analyser = Analyser()
games_data = analyser.load_data(path_to_dir)
print(analyser.execute(
    TrendingOnlySelector(),
    DnbWinOnly(),
    WDLProbabilitiesFeatureBuilder(),
    RandomForestAlgorithm(),
    games_data
))
