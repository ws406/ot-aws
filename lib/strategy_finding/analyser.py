from lib.strategy_finding.sample_selector.interface import SampleSelectorInterface
from lib.strategy_finding.data_labeler.interface import DataLabelerInterface
from lib.strategy_finding.feature_builder.interface import FeatureBuilderInterface
from lib.strategy_finding.algorithm.interface import AlgorithmInterface
from lib.utils.file_helper import filerHelper
from lib.utils.logger import OtLogger
import json


class Analyser:

    def __init__(self):
        self.logger = OtLogger()
        pass

    def load_data(self, path):
        games = []
        self.logger.debug("Loading games dat from " + path)
        for file_name in filerHelper.get_files_from_a_dir(path):
            file_dir_name = path + file_name
            with open(file_dir_name) as json_file:
                g = json.load(json_file)
                self.logger.debug("\tAdd " + str(len(g)) + " games from file - " + file_name)
                games += g

                self.logger.debug(str(len(games)) + " games added", True)
        return games

    def execute(
        self,
        sample_selector: SampleSelectorInterface,
        data_labeler: DataLabelerInterface,
        feature_builder: FeatureBuilderInterface,
        algorithm: AlgorithmInterface,
        data
    ):
        self.logger.debug("Starting analysis...")

        selected_matches = sample_selector.get_selected_games_data(data)
        labelled_matches = data_labeler.label_data(selected_matches)
        header, analysis_ready_matches = feature_builder.get_features(labelled_matches)

        return algorithm.get_results(header, analysis_ready_matches)
