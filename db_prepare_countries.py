import csv
import operator

"""
Preparing the db of countries.
Two optional function:
country_by_championships
country_by_proportion_champs_drivers

The order of countries is defined by wiki_countries.csv.
Notice that a name of a country is the same as in wiki_drivers_edited.csv, as we add it to the drivers in db_prepare_wiki.py
"""

def country_by_championship():
    championships = {}
    counter = 0
    with open('formula_DB/wiki_countries.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if counter == 0:  # the first row (titles)
                counter = 1
                continue
            championships[row[0]] = row[3] #the championships in that country
    print(championships)

country_by_championship()