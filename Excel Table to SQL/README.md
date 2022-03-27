# Excel table to SQL script
Last Updated: 2022-03-26

main() function is inside of "TableToSQL.py"

Helper functions are included inside this python file which are used to identify the unique entities for each column. Each column from  the excel table has its own entities table on the SQL database.
One helper function finds the unique entities in each column and generates the primary key for these entities.
Another helper function performs a filtering pattern against all foreign key columns to identify the correct foreign key.

The sql module takes the prepared pandas dataframe with the primary keys and foreign keys then
writes the sql script to a txt file for each entity table. 