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
                    'X_train_full_data': np.concatenate (
                        (featured_data ['2014-2015'] [:, 1:], featured_data ['2015-2016'] [:, 1:])),
                    'y_train': np.concatenate (
                        (featured_data ['2014-2015'] [:, 0], featured_data ['2015-2016'] [:, 0])),
                    'X_test_full_data': featured_data ['2016-2017'] [:, 1:],
                    'y_test': featured_data ['2016-2017'] [:, 0],
                },
            #'set 2':
                #{
                    #'X_train_full_data': np.concatenate (
                        #(featured_data ['2014-2015'] [:, 1:], featured_data ['2015-2016'] [:, 1:]
                         #, featured_data ['2016-2017'] [:, 1:])),
                    #'y_train': np.concatenate ((featured_data ['2014-2015'] [:, 0], featured_data ['2015-2016'] [:, 0]
                                                #, featured_data ['2016-2017'] [:, 0])),
                    #'X_test_full_data': featured_data ['2017-2018'] [:, 1:],
                    #'y_test': featured_data ['2017-2018'] [:, 0],
                #},
            #'set 3':
                #{
                    #'X_train_full_data': np.concatenate (
                        #(featured_data ['2014-2015'] [:, 1:], featured_data ['2015-2016'] [:, 1:]
                         #, featured_data ['2016-2017'] [:, 1:], featured_data ['2017-2018'] [:, 1:])),
                    #'y_train': np.concatenate ((featured_data ['2014-2015'] [:, 0], featured_data ['2015-2016'] [:, 0]
                                                #, featured_data ['2016-2017'] [:, 0],
                                                #featured_data ['2017-2018'] [:, 0])),
                    #'X_test_full_data': featured_data ['2018-2019'] [:, 1:],
                    #'y_test': featured_data ['2018-2019'] [:, 0],
                #},
            # 'set 3':
            #     {
            #         'X_train_full_data': np.concatenate ([featured_data ['2015-2016'] [:, 1:], featured_data ['2015-2016'] [:,1:]]),
            #         'y_train': np.concatenate ([featured_data ['2015-2016'] [:, 0], featured_data ['2015-2016'] [:, 0]]),
            #         'X_test_full_data': featured_data ['2017-2018'] [:, 1:],
            #         'y_test': featured_data ['2017-2018'] [:, 0],
            #     },
            # 'set 4':
            #     {
            #         'X_train_full_data': featured_data ['2017-2018'] [:,1:],
            #         'y_train': featured_data ['2017-2018'] [:, 0],
            #         'X_test_full_data': featured_data ['2018-2019'] [:,1:],
            #         'y_test': featured_data ['2018-2019'] [:, 0],
            #     },
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
            print("Running algorithm - on " + key)

            X_train = value['X_train_full_data'][:,3:]
            y_train = value['y_train']
            X_test = value ['X_test_full_data'] [:, 3:]
            y_test = value ['y_test']

            self.compare_algs(X_train, y_train, X_test, y_test, value['X_test_full_data'], np.asarray(value ['X_test_full_data'] [:, 3]))

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


    def compare_algs(self, X_train, y_train, X_test, y_test, X_test_full_data, benchmarkProb):
        from sklearn.metrics import accuracy_score, log_loss
        from sklearn.linear_model import LogisticRegression
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC, LinearSVC, NuSVC
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
        from sklearn.naive_bayes import GaussianNB
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
        import pandas as pd

        tree_size=500
        classifiers = [
            #KNeighborsClassifier (n_jobs=-1),
            # SVC (kernel = "rbf", C = 0.025, probability = True),
            # NuSVC (probability = True),
            #DecisionTreeClassifier (max_features=None, random_state = 0),
            RandomForestClassifier (n_estimators=tree_size, max_features=None, min_samples_leaf=10, random_state = 0, n_jobs=-1),
            #AdaBoostClassifier (random_state = 0),
            LogisticRegression (),
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
            X_test = X_test.astype(float)
            X_train = X_train.astype(float)
            test_predictions = clf.predict (X_train)
            #print(X_test.shape)
            train_predictions = clf.predict (X_test)
            y_prob = clf.predict_proba(X_test)
            acc1 = accuracy_score (y_train, test_predictions)
            acc = accuracy_score (y_test, train_predictions)
            print ("Train Accuracy: {:.4%}".format (acc1))
            print ("Accuracy: {:.4%}".format (acc))

            train_predictions = clf.predict_proba (X_test)
            ll = log_loss (y_test, train_predictions)
            print ("Log Loss: {}".format (ll))

            log_entry = pd.DataFrame ([[name, acc * 100, ll]], columns = log_cols)
            log = log.append (log_entry)
            self.calculate_results (y_prob, X_test_full_data, y_test, clf.classes_, benchmarkProb)

        print ("=" * 30)


    def calculate_results(self, y_prob, X_test_full_data, y_test, classes, benchmarkProb):

        minBenmarkProb = 0.501
        maxBenmarkProb = 0.52
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
            if y_pred == '2':
                i = i + 1
                continue

            # print(prob)
            # print(y_pred)
            # print(prob[bigger_value_index])
            # print(X_benchmark_prob)
            #if float(maxBenmarkProb) <= float(prob[bigger_value_index]) <= float(minBenmarkProb):
                # y_pred = classes [abs(bigger_value_index-1)]
            if float(prob[bigger_value_index]) < float(benchmarkProb[i]):
                i += 1
                continue

            # print(X_test_full_data[i, :])
            odds = X_test_full_data[i, 1] if y_pred == '1' else X_test_full_data[i, 2]
            # odds = X_test_full_data[i, 1]
            odds = float(odds)
            # print(odds)

            if y_test[i] == y_pred:
                right += 1
                pnl = odds - 1
            else:
                wrong += 1
                pnl = -1

            total_pnl += pnl
            #print ("id", int (X_test_full_data[i, 0]), ",predict", y_pred, ",result",y_test[i],  ",return", pnl, ",prob", prob, "benchmark", float(benchmarkProb[i]))
            i = i + 1

        print ("win rate is " + str(right / (right + wrong)) + ", bet ratio is " + str((right + wrong) / len (y_test)) +
               ", total bet matches " + str(right + wrong) + ", pnl is " + str(total_pnl))
