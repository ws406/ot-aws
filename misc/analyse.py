from src.strategy_finding.analyser import Analyser
from src.strategy_finding.feature_builder.three_ways_key_bookies import ThreeWaysKeyBookies
from src.utils.logger import OtLogger


# path_to_dir = '../data/basketball_all_odds_data/'
path_to_dir = '../data/analysing/'
logger = OtLogger('ot')

analyser = Analyser(logger)
feature_builder = ThreeWaysKeyBookies(logger)

games_data = analyser.load_data(path_to_dir, feature_builder)
