from lib.strategy_finding.algorithm.interface import AlgorithmInterface
from pprint import pprint
import numpy as np

class RandomForestAlgorithm(AlgorithmInterface):

    def get_results(self, header, featured_data: np.array):
        print("Running algorithm - RandomForest")
        print(featured_data.shape)
        pprint(header)
        pass
