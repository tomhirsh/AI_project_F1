import csv
import db_prepare_countries_races_constructors


def prepare_drivers():
    full_names = {}
    drivers = []
    #count = 0
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

    wiki_starts = {}
    wiki_fastest_laps = {}
    wiki_countries = {}
    with open('formula_DB/wiki_drivers_edited.csv','r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            driver_name = row[0]
            starts = row[5]
            fastest_laps = row[9]
            country = row[1]
            wiki_starts[driver_name] = starts
            wiki_fastest_laps[driver_name] = fastest_laps
            wiki_countries[driver_name] = country

    counter = 0
    for row in drivers:
        if counter == 0:
            row.append("starts_num")
            row.append("fastest_laps_num")
            row.append("country")
            counter += 1
            continue
        driver_name = row[9]
        if driver_name in wiki_starts:
            row.append(int(wiki_starts[driver_name]))
            row.append(int(wiki_fastest_laps[driver_name]))
            row.append(wiki_countries[driver_name])
        else:
            row.append(-1)
            row.append(-1)
            row.append(-1)

    """
    use db_prepare_countries to get the rank of a driver's country and append it to the driver
    """
    counter = 0
    for row in drivers:
        if counter == 0:
            row.append("country_rank_by_championships")
            row.append("country_rank_by_proportion_drivers")
            counter += 1
            continue
        country_name = row[12]
        if country_name != -1:
            row.append(db_prepare_countries_races_constructors.get_rank_by_championships(country_name))
            row.append(db_prepare_countries_races_constructors.get_rank_by_proportion_champs_drivers(country_name))
        else:
            row.append(-1)
            row.append(-1)

    """
    handling the age of a driver - in order to add it to the race's db (age in a race)
    """
    counter = 0
    for row in drivers:
        if counter == 0:
            row.append("year_of_birth")
            counter += 1
            continue
        dob = row[6]
        _,_,yob = dob.split("/")
        row.append(yob)
        if len(row)<16:
            print(row)

    """
    handling the top100 drivers
    """
    driver_rank = {}
    with open('formula_DB/Top_100_driver_ranking.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count == 0:
                count += 1
                continue
            driver_rank[row[1]] = int(row[0])

    counter = 0
    for row in drivers:
        if counter == 0:
            row.append("drivers_top_100")
            counter += 1
            continue
        full_name = row[9]
        if full_name in driver_rank:
            driver_top_100 = driver_rank[full_name]
        else:
            driver_top_100 = 101
        row.append(driver_top_100)

    """
    handling the top38 countries  
    """
    country_rank = {}
    with open('formula_DB/Top_38_country_ranking.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count == 0:
                count += 1
                continue
            country_rank[row[1]] = int(row[0])

    counter = 0
    for row in drivers:
        if counter == 0:
            row.append("countries_top_38")
            counter += 1
            continue
        country_name = row[12]
        if country_name in country_rank:
            countries_top_38 = country_rank[country_name]
        else:
            countries_top_38 = 39
        row.append(countries_top_38)

    #print(drivers[0])
    #print(drivers[1])
    return drivers


drivers = prepare_drivers()
#print(drivers)

# convert drivers to dictionary by driver_id
drivers_dict = {}
for driver in drivers[1:]:
    drivers_dict[int(driver[0])] = driver[1:]


def get_starts_num_by_driver(driver_id):
    if driver_id in drivers_dict:
        driver = drivers_dict[driver_id]
        return int(driver[9]) #9
    else:
        return -1


def get_fastest_laps_num_by_driver(driver_id):
    if driver_id in drivers_dict:
        driver = drivers_dict[driver_id]
        return int(driver[10]) #10
    else:
        return -1


def get_country_rank_championships_by_driver(driver_id):
    if driver_id in drivers_dict:
        driver = drivers_dict[driver_id]
        return int(driver[12]) #12
    else:
        return -1


def get_country_rank_proportion_by_driver(driver_id):
    if driver_id in drivers_dict:
        driver = drivers_dict[driver_id]
        return int(driver[13]) #13
    else:
        return -1


def get_year_of_birth_of_driver(driver_id):
    if driver_id in drivers_dict:
        driver = drivers_dict[driver_id]
        return int(driver[14])
    else:
        return -1


def get_driver_rank_top100(driver_id):
    if driver_id in drivers_dict:
        driver = drivers_dict[driver_id]
        return int(driver[15])
    else:
        return 101


def get_country_rank_top38(driver_id):
    if driver_id in drivers_dict:
        driver = drivers_dict[driver_id]
        return int(driver[16])
    else:
        return 39

"""
for driver in drivers:
        print(driver)
"""

#print(get_starts_num_by_driver(841))

#print(get_country_rank_championships_by_driver(1))
#print(get_country_rank_proportion_by_driver(1))
