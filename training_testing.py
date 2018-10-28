import db_prepare_features as db
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
"""
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier

results with all of the features:

* The most important feature is the podiumsUntilThisRace feature (with L1)
* Using criterion = "entropy"

using the "score" function from the sklearn.ensemble.RandomForestClassifier
when splitting to 75% train data, and  25% test data


PROPORTION: 0.715445563924. n_estimators = 91
L1: 0.714173921549. n_estimators = 96 
both: 0.745182431771. n_estimators = 84

##########################################################################################3

criterion = "entropy"
structure = "BOTH"

n_estimators = 84
Accuracy: 0.745182431771

"""


def train_and_test_with_all_features(estimators_num, structure):
    # prepare features and labels for train and test
    features, res = db.prepare_features(structure)

    clf = RandomForestClassifier(n_estimators=estimators_num, criterion="entropy")  # use default values
    # splitting into train and test data
    train_len = int(len(features) * 0.75)  # take 75% for train, 25% for test
    #print("The train set contains: " + str(train_len) + " objects")
    features_train = features[:train_len]
    features_test = features[train_len:]
    res_train = res[:train_len]
    res_test = res[train_len:]

    clf.fit(features_train, res_train)
    accuracy = clf.score(features_test, res_test)
    print("Random forest "+structure+" with "+str(estimators_num)+" n_estimators. Accuracy: "+str(accuracy))
    feature_importance = clf.feature_importances_
    #print("Feature importance:")
    #print(clf.feature_importances_)  # Return the feature importances (the higher, the more important the feature)

    return accuracy, feature_importance, clf


"""
structure = 'BOTH'  # {L1, PROPORTION, BOTH}
accuracy, clf = train_and_test_with_all_features(84, structure)

"""

"""
structure = 'PROPORTION'  # {L1, PROPORTION, BOTH}
# hyper-parameters tuning (brute-force)
max_accuracy = 0
n_estimators_max_acc = 0
min_n_estimators = 1
max_n_estimators = 100
graph = []
for n in range(min_n_estimators, max_n_estimators+1):
    accuracy, clf = train_and_test_with_all_features(n, structure)
    graph.append(accuracy)
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        n_estimators_max_acc = n
print("The best hyper parameter n_estimators value: "+str(n_estimators_max_acc)+". Accuracy: "+str(max_accuracy))

plt.plot(range(min_n_estimators, max_n_estimators+1), graph)
plt.ylabel("Accuracy")
plt.xlabel("n_estimators")
plt.show()
"""