import db_prepare_features as db
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
"""
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier

results with all of the features:

* The most important feature is the podiumsUntilThisRace feature (with L1)
* Using criterion = "gini"

using the "score" function from the sklearn.ensemble.RandomForestClassifier
when splitting to 75% train data, and  25% test data

* Training with 10 n_estimators:
PROPORTION: 0.683556685904
L1: 0.684339235058
both: 0.704294238482

Training with 100 n_estimatores:
PROPORTION: 0.702435684241
L1: 0.708696077472
both: 0.733248557175



* Using 4-folds cross validation:

Training with 10 n_estimators:
PROPORTION: 0.704541435823
L1: 0.713713086835
both: 0.719704806547

Training with 100 n_estimatores:
PROPORTION: 0.723567404704
L1: 0.733107360335
both: 0.74389153922

* Using criterion = "entropy"
Training with 100 n_estimatores:
both: 0.746948697242

##########################################################################################3

criterion = "entropy"
structure = "BOTH"
cross_validation = True
n_estimators = 89
Accuracy: 0.750373451526

"""


def train_and_test_with_all_features(estimators_num, structure, cross_validation):
    # prepare features and labels for train and test
    features, res = db.prepare_features(structure)

    clf = RandomForestClassifier(n_estimators=estimators_num, criterion="entropy")  # use default values
    if not cross_validation:
        # splitting into train and test data
        train_len = int(len(features) * 0.75)  # take 75% for train, 25% for test
        print("The train set contains: " + str(train_len) + " objects")
        features_train = features[:train_len]
        features_test = features[train_len:]
        res_train = res[:train_len]
        res_test = res[train_len:]

        clf.fit(features_train, res_train)
        accuracy = clf.score(features_test, res_test)
        print("Random forest with "+str(estimators_num)+" n_estimators. Accuracy: "+str(accuracy))
        print("Feature importance:")
        print(clf.feature_importances_)  # Return the feature importances (the higher, the more important the feature)
    else:
        #print("using cross validation")
        avg_score = cross_val_score(clf, features, res, cv=4)
        accuracy = sum(avg_score) / len(avg_score)
        print("Random forest with "+str(estimators_num)+" n_estimators. Accuracy: "+str(accuracy))
    return accuracy


structure = 'BOTH'  # {L1, PROPORTION, BOTH}
cross_validation = True

#train_and_test_with_all_features(89, structure, cross_validation)


# hyper-parameters tuning (brute-force)
max_accuracy = 0
n_estimators_max_acc = 0
min_n_estimators = 10
max_n_estimators = 100
graph = []
for n in range(min_n_estimators, max_n_estimators+1):
    accuracy = train_and_test_with_all_features(n, structure, cross_validation)
    graph.append(accuracy)
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        n_estimators_max_acc = n
print("The best hyper parameter n_estimators value: "+str(n_estimators_max_acc)+". Accuracy: "+str(max_accuracy))

plt.plot(range(min_n_estimators, max_n_estimators+1), graph)
plt.ylabel("Accuracy")
plt.xlabel("n_estimators")
plt.show()
