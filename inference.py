import csv
import training_testing
import numpy as np
"""
This script is the "main" script in this project.
Given a list of drivers (their features), the output is the race result (finish line order).
(Using the classifier from training_testing.py and the "remove cycles" algorithm)
The input should be:
[driver_id,...driver_features...]
"""


"""
making an object (L1+PROPORTION)
while the first 2 indexes have the drivers id's
"""
def make_object(driver1,driver2):
    driver1_id = driver1[0]
    driver2_id = driver2[0]
    driver1_features = driver1[1:]
    driver2_features = driver2[1:]

    arr_i = np.array(driver1_features, dtype=float)
    arr_j = np.array(driver2_features, dtype=float)
    features_proportion = (np.divide(arr_i, arr_j, out=np.zeros_like(arr_i), where=arr_j != 0))  # handle also divide by zero
    features_proportion = np.round(features_proportion, 2)  # round to 2 digits after the dot
    features_L1 = np.asarray(driver1_features) - np.asarray(driver2_features)

    ids = np.append([driver1_id],[driver2_id])
    features = np.append(features_L1,features_proportion)

    object = np.append(ids,features)
    return object


"""
make the directed, weighted graph G=(V,E)
V contains the drivers id's
E contains the object (specified by two drivers). The direction of e in E is specified by the classification by clf.
The weight of each e in E is specified by the features of each object, ordering down from the most relevant.
"""
def make_graph(objects_list):

"""
The algorithm:
0. input: G=(V,E) directed with weights on edges [in our case: V = drivers_id, E = objects]
1. make directed graph G'=(V,E'), as E' = None
2. for each e in E, in revert order by weight:
    2.1. if e does not close a cycle:
        2.1.1. add e to E'.
3. return G'
"""
def remove_cycles(graph):


"""
given a race (drivers list) with the features of each driver and it's id,
the output is the order in that race (finish line)
"""
def main(drivers_list):
