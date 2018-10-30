import csv
import db_prepare_countries_races_constructors
import db_prepare_drivers

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


"""
compute the features.
append that number to the end of each row in results (new column)

This code handles the following features:
counterInvolvedProblems
winsUntilThisRace
podiumsUntilThisRace
driverAge
countryRankByChampionships
countryRankByProportion
allTimeStarts
allTimefastestLap
constructorRank
driverTop100
countryTop38
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

    # implement: calculate the age of the driver
    driver_id = int(row[2])
    race_id = int(row[1])
    birth_year = db_prepare_drivers.get_year_of_birth_of_driver(driver_id)
    if birth_year != -1:
        driver_age = db_prepare_countries_races_constructors.get_year_of_race(race_id) - birth_year
    else:
        driver_age = -1
    # print(driver_age)
    row.append(driver_age)

    # implement: country rank (both options)
    # by championships:
    country_rank_by_championships = db_prepare_drivers.get_country_rank_championships_by_driver(driver_id)
    # by proportion drivers to champions:
    country_rank_by_proportion_champs_drivers = db_prepare_drivers.get_country_rank_proportion_by_driver(driver_id)
    row.append(country_rank_by_championships)
    row.append(country_rank_by_proportion_champs_drivers)

    # implement: all-time parameters (starts and fastest lap)
    # starts:
    all_time_starts = db_prepare_drivers.get_starts_num_by_driver(driver_id)
    # fastest lap
    all_time_fastest_laps = db_prepare_drivers.get_fastest_laps_num_by_driver(driver_id)
    row.append(all_time_starts)
    row.append(all_time_fastest_laps)

    # implement: constructor rank
    constructor_id = int(row[3])
    constructor_rank = db_prepare_countries_races_constructors.get_constructor_rank(constructor_id)
    row.append(constructor_rank)

    # implement: driver top100
    driver_top100 = db_prepare_drivers.get_driver_rank_top100(driver_id)
    row.append(driver_top100)

    # implement: country top38
    country_top38 = db_prepare_drivers.get_country_rank_top38(driver_id)
    row.append(country_top38)

(results[0]).append('counterInvolvedProblems')
(results[0]).append('winsUntilThisRace')
(results[0]).append('podiumsUntilThisRace')
(results[0]).append('driverAge')
(results[0]).append('countryRankByChampionships')
(results[0]).append('countryRankByProportion')
(results[0]).append('allTimeStarts')
(results[0]).append('allTimefastestLap')
(results[0]).append('constructorRank')
(results[0]).append('driverTop100')
(results[0]).append('countryTop38')


# write results to csv file
with open('db_prepared_ver2.csv', 'w', newline='') as csvfile:
    db_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(results)):
        result = results[i]
        wanted_result = result[0:2]
        wanted_result.append(result[6])
        wanted_result.extend(result[18:21])
        wanted_result.extend(result[23:])
        db_writer.writerow(wanted_result)

"""
count = 0
for i in range(len(results)):
    result = results[i]
    
    #wanted_result = result[0:2]
    #wanted_result.append(result[6])
    #wanted_result.extend(result[18:])

    print(result)
    count += 1
    if count > 10:
        break
"""