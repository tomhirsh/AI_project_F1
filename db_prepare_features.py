import csv
import numpy as np
import random
"""
IN ORDER TO USE THIS SCRIPT:
call to prepare_features(structure)
structure = 'L1' for the L1 distance function
structure = 'PROPORTION' for the proportion distance function

Use db_prepared.cv and extract relevant features to compare two drivers.
The features will describe an OBJECT

1. L1 (distance)
2. proportion

Each time handle a specific race data, and make couples from that race alone.
Do this for each and every race.
"""


def randomize(i,j):
    if random.randint(0,2) == 1:
        return i,j
    else:
        return j,i

def create_features(drivers, labels, structure):
    drivers_features = []
    binary_labels = []
    for i in range(len(drivers)-1,0, -1):
        for j in range(i):
            new_i,new_j = randomize(i,j)  # don't always choose the first to win !
            # print(str(new_i)+' and '+str(new_j))
            if int(labels[new_i]) < int(labels[new_j]):
                binary_labels += [0]
            else:
                binary_labels += [1]
            if structure == 'L1':
                drivers_features.append(np.asarray(drivers[new_i])-np.asarray(drivers[new_j]))
            elif structure == 'PROPORTION':
                arr_i = np.array(drivers[new_i], dtype=float)
                arr_j = np.array(drivers[new_j], dtype=float)
                featurs_proportion = (np.divide(arr_i, arr_j, out=np.zeros_like(arr_i), where=arr_j != 0))  # handle also divide by zero
                featurs_proportion = np.round(featurs_proportion,2)  # round to 2 digits after the dot
                drivers_features.append(featurs_proportion)
            elif structure == 'BOTH':  # both L1 and proportion
                arr_i = np.array(drivers[new_i], dtype=float)
                arr_j = np.array(drivers[new_j], dtype=float)
                featurs_proportion = (np.divide(arr_i, arr_j, out=np.zeros_like(arr_i), where=arr_j != 0))  # handle also divide by zero
                featurs_proportion = np.round(featurs_proportion,2)  # round to 2 digits after the dot
                features_L1 = np.asarray(drivers[new_i])-np.asarray(drivers[new_j])
                features = np.append(features_L1,featurs_proportion)
                drivers_features.append(features)
    return drivers_features, binary_labels



def prepare_features(structure):
    features = []
    res = []  # The label. 0 if the first driver won, 1 if the second won
    race_id = -1  # To separate the races and figure out the relevant couples
    counter = 0
    with open('db_prepared.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        curr_race_drivers = []
        curr_race_labels = []
        for row in reader:

            if counter == 0:
                counter += 1
                continue
            # fix position (bug in DB)
            if row[2] == '':
                row[2] = '20'
            if int(row[2]) > 10:  # We want only the first 10
                continue
            if row[1] != race_id:
                if race_id != -1:
                    #print(curr_race_drivers)
                    #print(curr_race_labels)
                    if len(curr_race_labels) >= 5:  # semi to full results
                        new_race_features, new_race_labels = create_features(curr_race_drivers, curr_race_labels, structure)
                        features.extend(new_race_features)
                        res.extend(new_race_labels)
                        #break #for check
                curr_race_drivers = []
                curr_race_labels = []
                race_id = row[1]
            int_row = [int(num) for num in row]  # convert the row to int
            wanted_features = int_row[3:]
            #wanted_features.append(int_row[len(int_row)-1])
            curr_race_drivers.append(wanted_features)
            curr_race_labels += [int_row[2]]
            #print(row)
    """
    #  self-check
    for i in range(len(features)):
        print(features[i])
        print(res[i])
    """
    return features, res

#choose structure: L1 or PROPORTION or BOTH
#structure = 'PROPORTION'
#structure = 'L1'
#structure = 'BOTH'
#features, res = prepare_features(structure)
#print(features[0])
