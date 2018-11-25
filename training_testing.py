import db_prepare_features as db
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

"""
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier
"""


def train_and_test_with_decision_tree(s_split,features_train, features_test, res_train, res_test, crit="entropy"):
    clf = DecisionTreeClassifier(random_state=0 , criterion=crit, min_samples_split=s_split)
    clf.fit(features_train, res_train)
    accuracy = clf.score(features_test, res_test)
    print("Decision tree. Accuracy: "+str(accuracy))

    return accuracy


def train_and_test_with_random_forest(estimators_num, s_split, features_train, features_test, res_train, res_test, crit="entropy"):
    clf = RandomForestClassifier(n_estimators=estimators_num, criterion=crit, min_samples_split=s_split)  # use default values
    clf.fit(features_train, res_train)
    accuracy = clf.score(features_test, res_test)
    print("Random forest with "+str(estimators_num)+" n_estimators. Accuracy: "+str(accuracy))
    feature_importance = clf.feature_importances_
    print("Feature importance:")
    print(clf.feature_importances_)  # Return the feature importances (the higher, the more important the feature)

    return accuracy, feature_importance, clf


def train_and_test():
    structure = 'BOTH'  # {L1, PROPORTION, BOTH}
    # prepare features and labels for train and test
    # splitting into train and test data
    features, res = db.prepare_features(structure)
    feat_train, feat_test, r_train, r_test = train_test_split(features, res)  # randomly split the examples to train and test set 75%,25%

    return train_and_test_with_random_forest(60, 25, feat_train, feat_test, r_train, r_test)

def train_and_test_check_criterion():
    structure = 'BOTH'  # {L1, PROPORTION, BOTH}
    # prepare features and labels for train and test
    # splitting into train and test data
    features, res = db.prepare_features(structure)
    feat_train, feat_test, r_train, r_test = train_test_split(features, res)  # randomly split the examples to train and test set 75%,25%

    criterion_set = ["gini", "entropy"]
    for criterion in criterion_set:
        print(criterion)
        acc_tree = train_and_test_with_decision_tree(2, feat_train, feat_test, r_train, r_test, criterion)
        acc_r_forest, _, _ = train_and_test_with_random_forest(10, 2, feat_train, feat_test, r_train, r_test, criterion)
        print("accuracy for decision tree: "+str(acc_tree))
        print("accuracy for random forest: " + str(acc_r_forest))


def hyper_parameters_tuning_min_samples_split():
    structure = 'BOTH'  # {L1, PROPORTION, BOTH}
    # prepare features and labels for train and test
    # splitting into train and test data
    features, res = db.prepare_features(structure)
    feat_train, feat_test, r_train, r_test = train_test_split(features, res)  # randomly split the examples to train and test set 75%,25%

    graph_tree = []
    graph_r_forest = []
    # decision tree
    a = [2,5,10,15,20,25]
    for i, val in enumerate(a):
        accuracy_tree = train_and_test_with_decision_tree(val, feat_train, feat_test, r_train, r_test)
        accuracy_r_forest, _, _ = train_and_test_with_random_forest(10, val, feat_train, feat_test, r_train, r_test)
        graph_tree.append(accuracy_tree)
        graph_r_forest.append(accuracy_r_forest)

    plt.plot([2,5,10,15,20,25], graph_tree, color="green", label="Decision Tree")
    plt.plot([2,5,10,15,20,25], graph_r_forest, color="blue", label="Random Forest")
    plt.ylabel("Accuracy")
    plt.xlabel("min_samples_split")
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.title("Accuracy as a function of min_samples_split")
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
        accuracy, _, _ = train_and_test_with_random_forest(n, 25, feat_train, feat_test, r_train, r_test)
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
#train_and_test_check_criterion()
#hyper_parameters_tuning_min_samples_split()
#hyper_parameters_tuning_random_forest_n_estimators()

train_and_test()