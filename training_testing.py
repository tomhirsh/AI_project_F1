import db_prepare_features as db
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

"""
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier
"""


def train_and_test_with_decision_tree(s_split,features_train, features_test, res_train, res_test):
    clf = DecisionTreeClassifier(random_state=0 , criterion="entropy", min_samples_split=s_split)
    clf.fit(features_train, res_train)
    accuracy = clf.score(features_test, res_test)
    print("Decision tree. Accuracy: "+str(accuracy))

    return accuracy


def train_and_test_with_random_forest(estimators_num, s_split, features_train, features_test, res_train, res_test):
    clf = RandomForestClassifier(n_estimators=estimators_num, criterion="entropy", min_samples_split=s_split)  # use default values
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

    return train_and_test_with_random_forest(num_estimators, 15, feat_train, feat_test, r_train, r_test)


def hyper_parameters_tuning_decision_tree_min_samples_split():
    structure = 'BOTH'  # {L1, PROPORTION, BOTH}
    # prepare features and labels for train and test
    # splitting into train and test data
    features, res = db.prepare_features(structure)
    feat_train, feat_test, r_train, r_test = train_test_split(features, res)  # randomly split the examples to train and test set 75%,25%

    graph = []
    # decision tree
    a = [2,5,10,15,20,25]
    for i, val in enumerate(a):
        accuracy = train_and_test_with_decision_tree(val, feat_train, feat_test, r_train, r_test)
        graph.append(accuracy)
    plt.plot([2,5,10,15,20,25], graph)
    plt.ylabel("Accuracy")
    plt.xlabel("min_samples_split")
    plt.grid(True)
    plt.title("Accuracy as a function of min_samples_split with "+str(structure)+" features")
    plt.show()


def hyper_parameters_tuning_random_forest_min_samples_split():
    structure = 'BOTH'  # {L1, PROPORTION, BOTH}
    # prepare features and labels for train and test
    # splitting into train and test data
    features, res = db.prepare_features(structure)
    feat_train, feat_test, r_train, r_test = train_test_split(features, res)  # randomly split the examples to train and test set 75%,25%

    graph = []
    # random forest
    a = [2,5,10,15,20,25]
    for i, val in enumerate(a):
        accuracy, _, _ = train_and_test_with_random_forest(87, val, feat_train, feat_test, r_train, r_test)
        graph.append(accuracy)
    plt.plot([2,5,10,15,20,25], graph)
    plt.ylabel("Accuracy")
    plt.xlabel("min_samples_split")
    plt.grid(True)
    plt.title("Accuracy as a function of min_samples_split with "+str(structure)+" features")
    plt.show()


def hyper_parameters_tuning_random_forest_n_estimators():
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
        accuracy, _, _ = train_and_test_with_random_forest(n, 15, feat_train, feat_test, r_train, r_test)
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
#hyper_parameters_tuning_random_forest_n_estimators()
#hyper_parameters_tuning_decision_tree_min_samples_split()
#hyper_parameters_tuning_random_forest_min_samples_split()
#train_and_test(87)