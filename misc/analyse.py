from src.strategy_finding.analyser import Analyser
from src.strategy_finding.sample_selector.trending_only import TrendingOnlySelector
from src.strategy_finding.sample_selector.trending_odds_select import TrendingOddsSelector
from src.strategy_finding.data_labeler.dnb_win_only import DnbWinOnly
from src.strategy_finding.data_labeler.dnb_win_only2 import DnbWinOnly2
from src.strategy_finding.feature_builder.wdl_probabilities import WDLProbabilitiesFeatureBuilder
from src.strategy_finding.feature_builder.wdl_probabilities2 import WDLProbabilitiesFeatureBuilder2
from src.strategy_finding.algorithm.random_forest import RandomForestAlgorithm

# path_to_dir = './misc/all_odds_data/'
path_to_dir = './data/test/'
analyser = Analyser()
games_data = analyser.load_data(path_to_dir)
result = analyser.execute(
    sample_selector = TrendingOddsSelector(),
    data_labeler = DnbWinOnly2(),
    feature_builder = WDLProbabilitiesFeatureBuilder2(),
    algorithm = RandomForestAlgorithm(),
    data = games_data
)
