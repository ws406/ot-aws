from src.strategy_finding.algorithm.interface import AlgorithmInterface
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.utils.logger import OtLogger
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


class NBARF1(AlgorithmInterface):

    def __init__(self, logger: OtLogger):
        super().__int__(logger)

    def get_results(self, header, featured_data: np.array):
        self.logger.debug("Running algorithm - RandomForest")
        self.logger.debug(featured_data.shape)

        X = featured_data[:,1:7]
        y = featured_data[:,0]
        X_train_full_data, X_test_full_data, y_train, y_test = train_test_split (X, y, test_size = 0.05, random_state = 0)

        X_train = X_train_full_data[:,3:]
        X_test = X_test_full_data[:,3:]

        # Define the algorithm
        alg = RandomForestClassifier()
        alg.fit(X_train, y_train)

        y_pred = alg.predict (X_test)
        y_prob = alg.predict_proba(X_test)
        self.logger.debug(y_pred)
        self.logger.debug(y_prob)

        self.logger.debug(confusion_matrix (y_test, y_pred))
        self.logger.debug(classification_report (y_test, y_pred))
        self.logger.debug(accuracy_score (y_test, y_pred))

        # Rank feature importance
        importances = alg.feature_importances_
        std = np.std([tree.feature_importances_ for tree in alg.estimators_],
             axis=0)
        indices = np.argsort(importances)[::-1]
        self.logger.debug("Feature ranking:")
        for f in range(X_train.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f] + 1, importances[indices[f]]))

        self.calculate_results(y_prob, X_test_full_data, y_test, alg.classes_)

        return ''

    def calculate_results(self, y_prob, X_test_full_data, y_test, classes):
        self.logger.debug(classes)

        benmarkProb = 0.52
        i = 0
        right = 0
        wrong = 0
        skipped = 0
        total_pnl = 0

        for prob in y_prob:
            bigger_value_index = 0
            X_benchmark_prob = X_test_full_data[i,3]
            if prob[1] > prob[0]:
                bigger_value_index = 1
                X_benchmark_prob = X_test_full_data[i,4]

            y_pred = classes [bigger_value_index]

            # print(prob)
            # print(y_pred)
            # print(prob[bigger_value_index])
            # print(X_benchmark_prob)
            if prob[bigger_value_index] <= benmarkProb:
                if float(prob[bigger_value_index]) <= float(X_benchmark_prob):
                    skipped += 1
                    continue


            odds = X_test_full_data[i, 1] if y_pred == '1' else X_test_full_data[i, 2]
            if y_test[i] == y_pred:
                right += 1
                pnl = float(odds) - 1
            else:
                wrong += 1
                pnl = -1

            total_pnl += pnl
            # print ("id", int (X_test_full_data[i, 0]), ",predict", predict_result, ",result", ",return", pnl, ",prob", prob)
            i = i + 1

        print ("win rate is", right / (right + wrong), ",bet ratio is", (right + wrong) / len (y_test),
               ",total bet matches", right + wrong, ",pnl is", total_pnl)
