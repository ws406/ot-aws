import sys
from lib.strategy_finding.sample_selector.interface import SampleSelectorInterface
from lib.strategy_finding.feature_builder.interface import FeatureBuilderInterface
from lib.strategy_finding.algorithm.interface import AlgorithmInterface
from lib.strategy_finding.sample_selector.trending_only import TrendingOnlySelector
from lib.strategy_finding.feature_builder.wdl_probabilities import WDLProbabilitiesFeatureBuilder
from lib.strategy_finding.algorithm.random_forest import RandomForestAlgorithm


class StrategyFinding:

    sample_selector = SampleSelectorInterface()
    feature_selector = FeatureBuilderInterface()
    algorithm = AlgorithmInterface()

    def __init__(self):
        pass

    def execute(
        self,
        sample_selector: SampleSelectorInterface,
        feature_builder: FeatureBuilderInterface,
        algorithm: AlgorithmInterface,
        raw_data
    ):
        print("Start...")
        featured_data = feature_builder.get_features(sample_selector.get_selected_games_data(raw_data))
        results = algorithm.get_results(featured_data)
        print(results)

# TODO: write this please.
raw_data = load_data()
StrategyFinding().execute(
    TrendingOnlySelector(),
    WDLProbabilitiesFeatureBuilder(),
    RandomForestAlgorithm(),
    raw_data
)
