# AI_project_F1

The goal of this project is to predict the rank of drivers in a F1 race.

## Databse
The database for this project is under the folder formula_DB
Changes in original DB:
"results_by_date.csv" contatins the data from "results.csv" and is ordered by date.
"drivers_edited.csv" contains the data from "drivers.csv" fixed (to English letters only)
"wiki_drivers_edited.csv" contains the data from "wiki_drivers.csv" fixed (to English letters only)

The data is taken from the following sources:
https://www.f1-fansite.com/f1-results/all-time-f1-team-rankings/
https://www.f1-fansite.com/f1-results/all-time-f1-driver-rankings/
https://www.f1-fansite.com/f1-results/time-f1-list-drivers-country/

## Pre-processing
db_prepare...py :
This series of code files contains the pre-processing.
The file "db_prepare_results.py" is based on all others, except db_prepare_features.py. It's output is a new csv file which contains all the features of a driver by races.
The file "db_prepare_features.py" pre-processes the data in real-time for the classifier, based on the new csv file of features.

## Training
The code file "training_testing.py" contains the training of a classifier (Random Forest), and it's testing.
the training and testing are based on the objects that are derive from "db_prepare_features.py".

## Inference
The main function of this project.
Given a list of drivers with their features in a specific race, the output is their rank.
It uses a classifier that is trained via "training_testing.py", an algorithm for removing cycles and preparing the right rank based on that.
