import db_prepare_features as db
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

"""
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier
"""


def train_and_test_with_all_features(estimators_num, features_train, features_test, res_train, res_test):

    clf = RandomForestClassifier(n_estimators=estimators_num, criterion="entropy")  # use default values

    clf.fit(features_train, res_train)
    accuracy = clf.score(features_test, res_test)
    print("Random forest with "+str(estimators_num)+" n_estimators. Accuracy: "+str(accuracy))
    feature_importance = clf.feature_importances_
    #print("Feature importance:")
    #print(clf.feature_importances_)  # Return the feature importances (the higher, the more important the feature)

    return accuracy, feature_importance, clf


def train_and_test(num_estimators):
    structure = 'BOTH'  # {L1, PROPORTION, BOTH}
    # prepare features and labels for train and test
    # splitting into train and test data
    features, res = db.prepare_features(structure)
    feat_train, feat_test, r_train, r_test = train_test_split(features, res)  # randomly split the examples to train and test set 75%,25%

    return train_and_test_with_all_features(num_estimators, feat_train, feat_test, r_train, r_test)


def hyper_parameters_tuning():
    structure = 'BOTH'  # {L1, PROPORTION, BOTH}
    # prepare features and labels for train and test
    # splitting into train and test data
    features, res = db.prepare_features(structure)
    feat_train, feat_test, r_train, r_test = train_test_split(features, res)  # randomly splits the examples to train and test set 75%,25%

    # hyper-parameters tuning (brute-force)
    max_accuracy = 0
    n_estimators_max_acc = 0
    min_n_estimators = 1
    max_n_estimators = 100
    graph = []
    for n in range(min_n_estimators, max_n_estimators+1):
        accuracy, _, _ = train_and_test_with_all_features(n, feat_train, feat_test, r_train, r_test)
        graph.append(accuracy)
        if accuracy > max_accuracy:
            max_accuracy = accuracy
            n_estimators_max_acc = n
    print("The best hyper parameter n_estimators value: "+str(n_estimators_max_acc)+". Accuracy: "+str(max_accuracy))

    plt.plot(range(min_n_estimators, max_n_estimators+1), graph)
    plt.ylabel("Accuracy")
    plt.xlabel("n_estimators")
    plt.grid(True)
    plt.title("Accuracy as a function of n_estimators with "+str(structure)+" features")
    plt.show()

# testing - hyper parameters tuning
# hyper_parameters_tuning()