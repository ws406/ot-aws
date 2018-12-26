from src.strategy_finding.analyser import Analyser
from src.strategy_finding.sample_selector.select_all import SelectAll
from src.strategy_finding.data_labeler.nba_home_1_away_2 import NBAHome1Away2
from src.strategy_finding.feature_builder.nba_1 import NBA1
from src.strategy_finding.algorithm.nba_rf_1 import NBARF1
from src.utils.logger import OtLogger


path_to_dir = '../data/basketball_all_odds_data/'
# path_to_dir = '../data/basketball_all_odds_data/test/'
logger = OtLogger('ot')

analyser = Analyser(logger)
games_data = analyser.load_data(path_to_dir)
result = analyser.execute(
    sample_selector = SelectAll(logger),
    data_labeler = NBAHome1Away2(logger),
    feature_builder = NBA1(logger),
    algorithm = NBARF1(logger),
    data = games_data
)
