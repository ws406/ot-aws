from src.strategy_finding.algorithm.interface import AlgorithmInterface
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from src.utils.logger import OtLogger
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


class NBARF1(AlgorithmInterface):

    def __init__(self, logger: OtLogger):
        super().__int__(logger)

    def get_results(self, header, featured_data: dict):

        # Set up three sets:
        # set 1: 15-16 => 16-17
        # set 2: 16-17 => 17-18
        # set 3: 15-16 + 16-17 => 17-18
        # set 4: 17-18 => 18-19
        # set 5: 16-17 + 17-18 => 18-19

        sets = {
            'set 1':
                {
                    'X_train_full_data': featured_data['2015-2016'][:,1:],
                    'y_train': featured_data['2015-2016'][:,0],
                    'X_test_full_data': featured_data['2016-2017'][:,1:],
                    'y_test': featured_data['2016-2017'][:,0],
                },
            'set 2':
                {
                    'X_train_full_data': featured_data ['2016-2017'][:,1:],
                    'y_train': featured_data ['2016-2017'][:,0],
                    'X_test_full_data': featured_data ['2017-2018'][:,1:],
                    'y_test': featured_data ['2017-2018'][:,0],
                },
            # 'set 3':
            #     {
            #         'X_train_full_data': np.concatenate ([featured_data ['2015-2016'] [:, 1:], featured_data ['2015-2016'] [:,1:]]),
            #         'y_train': np.concatenate ([featured_data ['2015-2016'] [:, 0], featured_data ['2015-2016'] [:, 0]]),
            #         'X_test_full_data': featured_data ['2017-2018'] [:, 1:],
            #         'y_test': featured_data ['2017-2018'] [:, 0],
            #     },
            'set 4':
                {
                    'X_train_full_data': featured_data ['2017-2018'] [:,1:],
                    'y_train': featured_data ['2017-2018'] [:, 0],
                    'X_test_full_data': featured_data ['2018-2019'] [:,1:],
                    'y_test': featured_data ['2018-2019'] [:, 0],
                },
            # 'set 5':
            #     {
            #         'X_train_full_data': np.concatenate (
            #             [featured_data ['2016-2017'] [:, 1:], featured_data ['2017-2018'] [:, 1:]]),
            #         'y_train': np.concatenate (
            #             [featured_data ['2016-2017'] [:, 0], featured_data ['2017-2018'] [:, 0]]),
            #         'X_test_full_data': featured_data ['2018-2019'] [:, 1:],
            #         'y_test': featured_data ['2018-2019'] [:, 0],
            #     },
        }

        for key, value in sets.items():
            self.logger.debug("Running algorithm - RandomForest - on " + key)

            X_train = value['X_train_full_data'][:,3:]
            y_train = value['y_train']
            X_test = value ['X_test_full_data'] [:, 3:]
            y_test = value ['y_test']

            self.compare_algs(X_train, y_train, X_test, y_test, value['X_test_full_data'])

            # Define the algorithm
            # self.logger.debug(confusion_matrix (y_test, y_pred))
            # self.logger.debug(classification_report (y_test, y_pred))
            # self.logger.debug(accuracy_score (y_test, y_pred))

            # Rank feature importance
            # importances = alg.feature_importances_
            # indices = np.argsort(importances)[::-1]
            # self.logger.debug("Feature ranking:")
            # for f in range(X_train.shape[1]):
            #     self.logger.debug(str(f + 1) + ' feature ' + str(indices[f] + 1) + ' - ' + str(importances[indices[f]]))

            # self.calculate_results (y_prob, value ['X_test_full_data'], y_test, alg.classes_)

        return ''


    def compare_algs(self, X_train, y_train, X_test, y_test, X_test_full_data):
        from sklearn.metrics import accuracy_score, log_loss
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC, LinearSVC, NuSVC
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
        from sklearn.naive_bayes import GaussianNB
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
        import pandas as pd

        classifiers = [
            # KNeighborsClassifier (3),
            # SVC (kernel = "rbf", C = 0.025, probability = True),
            NuSVC (probability = True),
            # DecisionTreeClassifier (),
            RandomForestClassifier (),
            # AdaBoostClassifier (),
            # GradientBoostingClassifier (),
            # GaussianNB (),
            # LinearDiscriminantAnalysis (),
            # QuadraticDiscriminantAnalysis ()
            ]

        # Logging for Visual Comparison
        log_cols = ["Classifier", "Accuracy", "Log Loss"]
        log = pd.DataFrame (columns = log_cols)

        for clf in classifiers:
            clf.fit (X_train, y_train)
            name = clf.__class__.__name__

            print ("=" * 30)
            print (name)

            print ('****Results****')
            train_predictions = clf.predict (X_test)
            y_prob = clf.predict_proba(X_test)
            acc = accuracy_score (y_test, train_predictions)
            print ("Accuracy: {:.4%}".format (acc))

            train_predictions = clf.predict_proba (X_test)
            ll = log_loss (y_test, train_predictions)
            print ("Log Loss: {}".format (ll))

            log_entry = pd.DataFrame ([[name, acc * 100, ll]], columns = log_cols)
            log = log.append (log_entry)
            self.calculate_results (y_prob, X_test_full_data, y_test, clf.classes_)

        print ("=" * 30)


    def calculate_results(self, y_prob, X_test_full_data, y_test, classes):

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
            # if y_pred == '1':
            #     i = i + 1
            #     continue

            # print(prob)
            # print(y_pred)
            # print(prob[bigger_value_index])
            # print(X_benchmark_prob)
            # if prob[bigger_value_index] <= benmarkProb:
            # if float(prob[bigger_value_index]) <= float(X_benchmark_prob):
                # y_pred = classes [abs(bigger_value_index-1)]
                # i += 1
                # continue

            # print(X_test_full_data[i, :])
            odds = X_test_full_data[i, 1] if y_pred == '1' else X_test_full_data[i, 2]
            odds = float(odds)
            # print(odds)

            if y_test[i] == y_pred:
                right += 1
                pnl = odds - 1
            else:
                wrong += 1
                pnl = -1

            total_pnl += pnl
            # print ("id", int (X_test_full_data[i, 0]), ",predict", y_pred, ",result",y_test[i],  ",return", pnl, ",prob", prob)
            i = i + 1

        self.logger.debug ("win rate is " + str(right / (right + wrong)) + ", bet ratio is " + str((right + wrong) / len (y_test)) +
               ", total bet matches " + str(right + wrong) + ", pnl is " + str(total_pnl))
