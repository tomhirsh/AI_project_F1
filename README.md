# AI_project_F1

## Databse  
The database for this project is under the folder formula_DB  
Changes in original DB:  
"results_by_date.csv" contatins the data from "results.csv" and is ordered by date.  
"drivers_edited.csv" contains the data from "drivers.csv" fixed (to English letters only)  
"wiki_drivers_edited.csv" contains the data from "wiki_drivers.csv" fixed (to English letters only)  

## Code files  
"db_prepare_results.py" - Handling the total number of podiums, wins and status.  
"db_prepare_wiki.py" - Handling the total starts and fastest laps of drivers (combines the data from wiki and the original DB)  
