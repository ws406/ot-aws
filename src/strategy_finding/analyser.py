from src.strategy_finding.algorithm.interface import AlgorithmInterface
from src.utils.file_helper import filerHelper
from src.utils.logger import OtLogger
import json
from src.strategy_finding.feature_builder.interface import FeatureBuilderInterface
import numpy as np


class Analyser:

    def __init__(self, logger: OtLogger):
        self.logger = logger

    def load_data(self, path, feature_builder: FeatureBuilderInterface):
        games = False
        for file_name in filerHelper.get_files_from_a_dir(path):
            file_dir_name = path + file_name
            self.logger.debug("Loading games data from " + file_dir_name)
            with open(file_dir_name) as json_file:
                g = feature_builder.get_features(json.load(json_file))
                if games is False:
                    games = g
                else:
                    games = np.concatenate((games, g))
                self.logger.debug("Add " + str(len(g)) + " games from file - " + file_name)
                self.logger.debug(str(len(games)) + " games added", True)

        filerHelper.save_file('../data/analysing/features/features.csv', games)

    def execute(
        self,
        algorithm: AlgorithmInterface,
        analysis_ready_data,
        header
    ):
        self.logger.debug("Starting analysis...")

        return algorithm.get_results(header, analysis_ready_data)
