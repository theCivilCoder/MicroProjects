import pandas as pd, numpy as np 

"""
TableToSQL()
	@Input = path to Excel holding the data
	@Output = txt file holding executable sql script for inserting data into SQL Tables with foreign key relationships 
				based on relationships defined in the Excel table.

	Assumptions: 
		- Primary key of SQL table begins at 1
		- Right Column is a Many to 1 relationship with the left column (many entries on the right column relate to only one entry on the left column)
"""
def TableToSQL(path):
	dictPrimaryKeys = {}
	df = pd.read_excel(path)
	# print(df.head())

	listCols = df.columns.to_list()
	print("Names of the Columns found in this Excel:")
	print(listCols)
	print("")


	## Get Primary Keys for each of the unique entries in each column
	idxCol = 0
	while (idxCol < len(listCols)):
		currentColName = listCols[idxCol]
		currentCol = list(set(df[currentColName].to_list()))
		currentCol.sort()
		addPKsToDict(dictPrimaryKeys, currentCol, currentColName)

		idxCol += 1
	# print(dictPrimaryKeys)
	print("-"*150)
	print("")


	## Create Excels for each column showing the layout of the equivalent SQL table
	idxCol = 0
	while (idxCol < len(listCols)):
		# print(f"current idxCol = {idxCol}")

		#get part of the dataframe up to the current column currently under consideration
		dfPartial = df[df.columns.to_list()[:idxCol+1]]
		
		#drop the duplicate rows
		# print(f"size: {dfPartial.shape}")
		dfPartial = dfPartial.drop_duplicates()
		# print(f"size: {dfPartial.shape}")

		dfPartial.index.names = ["Primary Key"]

		#call function to process the table and print out excel tables representative of the table saved on SQL software
		printTableWithForeignKeys(idxCol, dfPartial, dictPrimaryKeys)

		# print(dfPartial.head())
		# print()
		idxCol += 1 

	# -------------------------------------------------
	# # THIS IS FOR TESTING SINGLE ITERATION, CAN DELETE LATER 

	# #get part of the dataframe up to the current column currently under consideration
	# idxCol = 1
	# dfPartial = df[df.columns.to_list()[:idxCol+1]]
	
	# #drop the duplicate rows
	# # print(f"size: {dfPartial.shape}")
	# dfPartial = dfPartial.drop_duplicates()
	# # print(f"size: {dfPartial.shape}")

	# #update the index to being at 1
	# dfPartial.index = np.arange(1, len(dfPartial) + 1)
	# dfPartial.index.names = ["Primary Key"]

	# #call function to process the table and print out excel tables representative of the table saved on SQL software
	# printTableWithForeignKeys(idxCol, dfPartial, dictPrimaryKeys)

	# # print(dfPartial.head())
	# # print()





"""
addPKsToDict()
	@Inputs:
		dictPrimaryKyes = dictionary holding dictionaries for each column where the sub-level dictionary holds (key,value) pairs of (unique entry, primary key integer)
		listUniqueNames = list of the unique entries in one column
		columName = name of the column under consideration (column from excel table)
	@Output: None

	Updates the dictionary holding all the dictionaries for each column with a single dictionary for the current column under consideration
"""
def addPKsToDict(dictPrimaryKeys, listUniqueNames, columnName):
	#create the dictionary for this particular columnName with the corresponding primary key for each unique entry
	dictOneColumn = {}

	for (i, name) in enumerate(listUniqueNames):
		dictOneColumn[name] = i+1

	#Update the dictionary with the primary keys for all the columns
	dictPrimaryKeys[columnName] = dictOneColumn

	print(f"Column Name = {columnName}")
	print(dictOneColumn)
	print()



def printTableWithForeignKeys(idxCol, dfPartial, dictPrimaryKeys):
	print(f"current idxCol = {idxCol}")
	currentColName = dfPartial.columns.to_list()[-1].replace(" ","_")

	#reorganize the dfPartial so that the latest column is on the left beside the primary key
	dfPartial = dfPartial[[dfPartial.columns.to_list()[-1]]+dfPartial.columns.to_list()[:-1]]

	#sort the table by the current column under consideration
	dfPartial.sort_values([currentColName.replace("_"," ")], inplace=True) 

	#update the index to being at 1
	dfPartial.index = np.arange(1, len(dfPartial) + 1)


	#add in the corresponding foreign keys for each column right of the latest column 
	listForeignKeyColumns = dfPartial.columns.to_list()[1:]
	# print(listForeignKeyColumns)
	for foreignKeyColumnName in listForeignKeyColumns:
		currentCol = dfPartial[foreignKeyColumnName].to_list()
		dictCurrentCol = dictPrimaryKeys[foreignKeyColumnName]

		#define the list of foreign keys
		listForeignKeys = [dictCurrentCol[foreignEntity] for foreignEntity in currentCol]

		#Add the foreign keys column to the dataframe
		dfPartial[f"{foreignKeyColumnName}_ForeignKey"] = listForeignKeys


	print(dfPartial.head())
	print()



	dfPartial.to_excel(f"Col{idxCol +1} - {currentColName}.xlsx")

def main():
	path = r"D:\Coding\100. Projects\1. MicoProjects\Dict From Excel Table\Data.xlsx"
	TableToSQL(path)

main() 