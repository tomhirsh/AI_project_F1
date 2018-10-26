import db_prepare_features as db
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

"""
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier.fit
"""

"""
results with all of the features:

* The most important feature is the podiumsUntilThisRace feature (with L1)

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

"""
def train_and_test_with_all_features(estimators_num, structure, cross_validation):
    # prepare features and labels for train and test
    features, res = db.prepare_features(structure)


    clf = RandomForestClassifier(n_estimators=estimators_num)  # use default values
    if not cross_validation:
        # splitting into train and test data
        train_len = int(len(features) * 0.75)  # take 75% for train, 25% for test
        print("The train set contains: " + str(train_len) + " objects")
        features_train = features[:train_len]
        features_test = features[train_len:]
        res_train = res[:train_len]
        res_test = res[train_len:]

        clf.fit(features_train,res_train)
        accuracy = clf.score(features_test,res_test)
        print(accuracy)
        print(clf.feature_importances_)  # Return the feature importances (the higher, the more important the feature)
    else:
        print("using cross validation")
        avg_score = cross_val_score(clf, features, res, cv=4)
        accuracy = sum(avg_score) / len(avg_score)
        print(accuracy)

structure = 'BOTH'  # {L1, PROPORTION, BOTH}
cross_validation = True
train_and_test_with_all_features(100,structure, cross_validation)

"""
def score_1(clf, features_subset, labels):
    res = cross_val_score(clf, features_subset, labels, cv=4)
    return sum(res)/len(res)

def sfs(x, y, k, clf, score):
    
    #:param x: feature set to be trained using clf. list of lists.
    #:param y: labels corresponding to x. list.
    #:param y: labels corresponding to x. list.
    #:param k: number of features to select. int
    #:param clf: classifier to be trained on the feature subset.
    #:param score: utility function for the algorithm, that receives clf, feature subset and labeles, returns a score.
    #:return: list of chosen feature indexes
    
    chosen_features_indexes = []
    chosen_features=[]
    for i in range(len(x)):
        chosen_features.append([])
    num_features = len(x[0])
    features_not_chosen_curr = list(range(num_features))
    for i in range(k):
        max_util = -1
        max_index = -1
        for j in range(len(features_not_chosen_curr)):
            for t in range(len(x)):
                chosen_features[t].append(x[t][features_not_chosen_curr[j]])
            curr_util = score(clf, chosen_features, y)
            if curr_util > max_util:
                max_util = curr_util
                max_index = features_not_chosen_curr[j]
            for t in range(len(x)):
                chosen_features[t].remove(x[t][features_not_chosen_curr[j]])
        features_not_chosen_curr.remove(max_index)
        chosen_features_indexes.append(max_index)
        for t in range(len(x)):
            chosen_features[t].append(x[t][max_index])
    return chosen_features_indexes


def choose_features_with_SFS(estimators_num, structure, num_chosen_features):
    features, res = db.prepare_features(structure)
    train_len = int(len(features) * 0.75)  # take 75% for train, 25% for test
    print("The train set contains: "+str(train_len)+" objects")
    features_train = features[:train_len]
    features_test = features[train_len:]
    res_train = res[:train_len]
    res_test = res[train_len:]

    clf = RandomForestClassifier(n_estimators=estimators_num)  # use default values

    chosen_features = []
    for i in range(len(features)):
        chosen_features.append([])
    chosen_features_indexes = sfs(features_train, res_train, num_chosen_features, RandomForestClassifier(n_estimators=estimators_num), score_1)
    chosen_features_indexes.sort()
    for chosen in chosen_features_indexes:
        for t in range(len(features)):  # to ge all the 422 rows from features
            chosen_features[t].append(features[t][chosen])

    chosen_features_train = chosen_features[:train_len]
    chosen_features_test = chosen_features[train_len:]

    clf.fit(chosen_features_train, res_train)
    accuracy = clf.score(chosen_features_test, res_test)
    print(accuracy)
    print(clf.feature_importances_)  # Return the feature importances (the higher, the more important the feature)


structure = 'BOTH'  # {L1, PROPORTION, BOTH}
choose_features_with_SFS(100, structure, 8)
"""
