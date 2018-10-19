import csv
import operator

"""
Preparing the db of countries, giving id to each country by a specific order
Two optional function:
country_by_championships
country_by_proportion_champs_drivers

The order of countries is defined by wiki_countries.csv.
Notice that a name of a country is the same as in wiki_drivers_edited.csv, as we add it to the drivers in db_prepare_wiki.py
"""

def country_by_championships():
    championships = {}
    counter = 0
    with open('wiki_countries.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if counter == 0:  # the first row (titles)
                counter = 1
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
    with open('wiki_countries.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if counter == 0:  # the first row (titles)
                counter = 1
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

#print(country_by_championships())
#print(country_by_proportion_champs_drivers())
