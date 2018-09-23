import csv


full_names = {}
drivers = []
count = 0
with open('formula_DB/drivers_edited.csv', 'r', encoding="utf8") as f:
    reader = csv.reader(f)
    for row in reader:
        driverId = row[0]
        first_name = row[4]
        last_name = row[5]
        if driverId != 'driverId':
            full_name = first_name+" "+last_name
            full_names[full_name] = driverId
            row.append(full_name)
        else:
            row.append('fullName') # header
        drivers.append(row)
        #count+=1
        #if count>10:
        #    break
#

with open('formula_DB/wiki_drivers_edited.csv','r', encoding="utf8") as f:
    reader = csv.reader(f)
    for row in reader:
        driver_name = row[0]
        starts = row[5]
        if driver_name in full_names:
            driver_row = int(full_names[driver_name])
            drivers[driver_row].append(starts)
            #print(driver_name)
        else:
            print(driver_name)

