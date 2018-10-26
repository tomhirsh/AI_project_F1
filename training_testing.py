import db_prepare_features as db
from sklearn.ensemble import RandomForestClassifier

"""
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier.fit
"""

"""
results with all of the features:

Training with 10 n_estimators:
PROPORTION: 0.683556685904
L1: 0.684339235058
both: 0.704294238482

Training with 100 n_estimatores:
PROPORTION: 0.702435684241
L1: 0.708696077472
both: 0.733248557175


"""
def train_and_test_with_all_features(estimators_num, structure):
    # prepare features and labels for train and test
    features, res = db.prepare_features(structure)
    train_len = int(len(features) * 0.75)  # take 75% for train, 25% for test
    print("The train set contains: "+str(train_len)+" objects")
    features_train = features[:train_len]
    features_test = features[train_len:]
    res_train = res[:train_len]
    res_test = res[train_len:]

    clf = RandomForestClassifier(n_estimators=estimators_num)  # use default values
    clf.fit(features_train,res_train)
    accuracy = clf.score(features_test,res_test)
    print(accuracy)

#structure = 'L1'  # {L1, PROPORTION, BOTH}
#train_and_test_with_all_features(100,structure)




