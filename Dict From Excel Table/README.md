# Excel table to SQL script

main() function is inside of "TableToSQL.py"
helper functions are included inside this python file which processes are used to identify the unique 
entities for each column. Each column from  the excel table has its own entities table on the SQL database.
One helper function finds the unique entities in each table and generates the primary key for these entities.
Another helper function performs a filtering pattern against all foreign key columns to identify the correct foreign key.

The sql module takes the prepared pandas dataframe with the primary keys and foreign keys then
writes the sql script to a txt file for each entity table. 