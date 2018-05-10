from lib.strategy_finding.algorithm.interface import AlgorithmInterface
from pprint import pprint
from numpy import matrix
from numpy import array
import numpy as np
from sklearn.datasets import load_digits
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

class RandomForestAlgorithm(AlgorithmInterface):

    def get_results(self, header, featured_data: np.array):
        print("Running algorithm - RandomForest")
        print(featured_data.shape)
        trainData = matrix(featured_data)
        trainRes = array(trainData[:,0])
        trainArr = trainData[:,2:]
        rf = RandomForestClassifier(n_estimators=10000, min_samples_leaf=100, random_state = 0, n_jobs=-1) #, criterion='gini'
        rf.fit(trainArr, trainRes.ravel())
        importances = rf.feature_importances_
        std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
        indices = np.argsort(importances)[::-1]
        print("Feature ranking:")
        for f in range(trainArr.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f] + 1, importances[indices[f]]))
        #pprint(header)
        pass
