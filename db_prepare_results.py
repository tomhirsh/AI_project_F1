import csv


# change status in results to binary status (driver is involved or not)
dict_status = {}
involved_keys = ['3','4','20','31','43','54','62','68','73','81','82','85','90','97','100','104','107','130']
with open('formula_DB/status.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:  # row contains [0]statusId, [1]status name
        if row[0] in involved_keys:
            dict_status[row[0]] = 1
        else:
            dict_status[row[0]] = 0
"""
# self-check
for d in dict:
    print(d+" : "+str(dict[d]))
print(len(dict))
"""

results = []
#count = 0 # counter for debugging
with open('formula_DB/results_by_date.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        # in results, instead of statusId, put the corresponding statusBinary
        if row[0] != 'resultId':
            row[17] = dict_status[row[17]]  # row[17] contains the statusId. convert to statusBinary
        results.append(row)  # after changes, including the header
        #count+=1
        #if count>50:
        #   break

"""
compute the number of driver-involved-status until the current race
append that number to the end of each row in results (new column "counterInvolvedProblems")
compute the number of wins and podiums(positions 1-3) until the current race
append that numbers to the end of each row in results (new columns "wins","podiums")
"""
prob = {}
wins = {}
podiums = {}
for i in range(len(results)-1, 0, -1):
    row = results[i]
    driver = row[2]
    position = row[6]
    statusId = row[17]

    # implement: driver involved problem counter
    if statusId == 1:  # driver involved (status)
        if driver in prob:
            prob[driver] += 1
        else:
            prob[driver] = 1
    if driver in prob:
        row.append(prob[driver])
    else:
        row.append(0)

    # implement: podiums and wins counters
    if position == '1':  # win
        if driver in wins:
            wins[driver] += 1
            podiums[driver] += 1  # sure in podiums if won before
        else:
            wins[driver] = 1
            if driver in podiums:
                podiums[driver] += 1
            else:
                podiums[driver] = 1
    if position in ['2','3']:  # podiums
        if driver in podiums:
            podiums[driver] += 1
        else:
            podiums[driver] = 1
    if driver in wins:
        row.append(wins[driver])
    else:
        row.append(0)
    if driver in podiums:
        row.append(podiums[driver])
    else:
        row.append(0)

(results[0]).append('counterInvolvedProblems')
(results[0]).append('wins')
(results[0]).append('podiums')

"""
# self-check
for i in range(len(results)):
    print(results[i])
"""