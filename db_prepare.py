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

# in results, instead of statusId, put the corresponding statusBinary
results = []
count = 0
with open('formula_DB/results.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'resultId':
            row[17] = dict_status[row[17]]  # row[17] contains the statusId. convert to statusBinary
        results.append(row)  # after changes, including the header
        count+=1
        if count>10:
           break

prob = {}
for i in range(len(results)-1, 1, -1):
    row = results[i]
    if row[17]==1: # driver involved (status)
        driver = row[2] #row[2] is driverId
        if driver in prob:
            prob[driver] += 1
        else:
            prob[driver] = 1
        row.append(prob[driver])
    else:
        row.append(0)
(results[0]).append('counterInvolved')
# print(results)