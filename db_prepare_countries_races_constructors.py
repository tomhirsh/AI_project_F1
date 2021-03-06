import csv

"""
Pre-processing the data for countries, races and constructors.

Countries rank:
    Two optional function:
    country_by_championships
    country_by_proportion_champs_drivers

    The order of countries is defined by wiki_countries.csv.
    Notice that a name of a country is the same as in wiki_drivers_edited.csv, as we add it to the drivers in db_prepare_wiki.py

Races:
    prepare the year of a race, by its id

Constructors rank:
    by wins of the constructor in all-time races (Kaggle db).
"""


def prepare_constructors_rank():
    constructors = {}
    counter = 0
    with open('formula_DB/constructorStandings.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if counter == 0:
                counter += 1
                continue
            constructor_id = int(row[2])
            wins_in_the_race = int(row[6])
            if constructor_id in constructors:
                constructors[constructor_id] += wins_in_the_race
            else:
                constructors[constructor_id] = wins_in_the_race

    list_numbers = []
    for constructor in constructors:
        if constructors[constructor] not in list_numbers:
            list_numbers.append(constructors[constructor])
    list_numbers.sort(reverse=True)

    dict_numbers = {}
    counter = 0
    for num in list_numbers:
        dict_numbers[num] = counter
        counter += 1

    for constructor in constructors:
        constructors[constructor] = dict_numbers[constructors[constructor]]
    return constructors


def prepare_races_by_year():
    race_with_year = {}
    counter = 0
    with open('formula_DB/races.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if counter == 0:
                counter += 1
                continue
            race_with_year[int(row[0])] = int(row[1]) #the championships in that country
    return race_with_year


def get_rank_by_country(dict_countries, country_name):
    return dict_countries[country_name]


def country_by_championships():
    championships = {}
    counter = 0
    with open('formula_DB/wiki_countries.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if counter == 0:
                counter += 1
                continue
            championships[row[0]] = int(row[3]) #the championships in that country

    list_numbers = []
    for country in championships:
        if championships[country] not in list_numbers:
            list_numbers.append(championships[country])
    list_numbers.sort(reverse=True)

    dict_numbers = {}
    counter = 0
    for num in list_numbers:
        dict_numbers[num] = counter
        counter += 1

    for country in championships:
        championships[country] = dict_numbers[championships[country]]
    return championships


def country_by_proportion_champs_drivers():
    champions_proportional_drivers = {}
    counter = 0
    with open('formula_DB/wiki_countries.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if counter == 0:
                counter += 1
                continue
            drivers_num = row[1]
            champs_num = row[2]
            champions_proportional_drivers[row[0]] = (int(champs_num))/(int(drivers_num)) # proportion between champions and drivers in that country

    list_numbers = []
    for country in champions_proportional_drivers:
        if champions_proportional_drivers[country] not in list_numbers:
            list_numbers.append(champions_proportional_drivers[country])
    list_numbers.sort(reverse=True)

    dict_numbers = {}
    counter = 0
    for num in list_numbers:
        dict_numbers[num] = counter
        counter += 1

    for country in champions_proportional_drivers:
        champions_proportional_drivers[country] = dict_numbers[champions_proportional_drivers[country]]
    return champions_proportional_drivers


def get_rank_by_championships(country):
    country_by_championships_ranked = country_by_championships()
    return get_rank_by_country(country_by_championships_ranked,country)


def get_rank_by_proportion_champs_drivers(country):
    country_by_proportion_champs_drivers_ranked = country_by_proportion_champs_drivers()
    return get_rank_by_country(country_by_proportion_champs_drivers_ranked,country)


def get_year_of_race(race_id):
    races_by_year = prepare_races_by_year()
    return int(races_by_year[race_id])


constructors_rank = prepare_constructors_rank()


def get_constructor_rank(constructor_id):
    if constructor_id in constructors_rank:
        return int(constructors_rank[constructor_id])
    else:
        return -1

#print(prepare_constructors_rank())
#print(constructors_rank)
#print(get_constructor_rank(102))
#print(get_year_of_race(1))
#print(get_rank_by_championships('Finland'))
