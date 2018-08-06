from src.strategy_finding.algorithm.interface import AlgorithmInterface
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
        trainData = matrix(featured_data[0:featured_data.shape[0] - 999,:])
        trainRes = array(trainData[:,0])
        trainArr = trainData[:,3:]
        rf = RandomForestClassifier(n_estimators=10000, min_samples_leaf=100, random_state = 0, n_jobs=-1) #, criterion='gini'
        rf.fit(trainArr, trainRes.ravel())
        importances = rf.feature_importances_
        std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
        indices = np.argsort(importances)[::-1]
        print("Feature ranking:")
        for f in range(trainArr.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f] + 1, importances[indices[f]]))

        testData = matrix(featured_data[featured_data.shape[0] - 1000:featured_data.shape[0] - 1,:])
        testRes = array(testData[:,0])
        testArr = testData[:,3:]

        output = rf.predict(testArr)
        a = np.asarray(output)
        probability = rf.predict_proba(testArr)

        benmarkProb1 = 0.56
        index = 0
        right = 0
        wrong = 0
        odds = 0
        predict_result = None
        for prob in probability:
            result_odds = -1
            if prob[1] > benmarkProb1:
                if testData[index, 0] == 1:
                    right = right + 1
                    result_odds = testData[index, 2]
                else:
                    wrong = wrong + 1
                odds = odds + result_odds
                if testData[index, 3] == 1:
                    predict_result = "home win"
                elif testData[index, 3] == 0:
                    predict_result = "away win"
                else:
                    print("fatal error")
                print("id", int(testData[index, 1]), ",predict", predict_result, ",result", testData[index, 0], ",return", result_odds, ",prob", prob)
            index = index + 1

        print("win rate is", right / (right + wrong), ",bet ratio is", (right + wrong) / len(testRes), ",total bet matches", right + wrong, ",pnl is", odds)
        
        return odds
