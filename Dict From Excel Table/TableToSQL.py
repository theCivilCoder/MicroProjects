import pandas as pd, numpy as np 
import sql.pandasToSQL as toolSQL

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


	# Get Primary Keys for each of the unique entries in each column
	idxCol = 0
	prevDF = None
	while (idxCol < len(listCols)):
		
		# addPKsToDict(dictPrimaryKeys, currentCol, currentColName, idxCol)
		prevDF = addPKsToDict(dictPrimaryKeys, df, idxCol, prevDF)


		idxCol += 1
	# print(dictPrimaryKeys)
	print("-"*150)
	print("")


"""
addPKsToDict()
	@Inputs:
		dictPrimaryKyes (DEPRACATED) = dictionary holding dictionaries for each column where the sub-level dictionary holds (key,value) pairs of (unique entry, primary key integer)
		listUniqueNames = list of the unique entries in one column
		columName = name of the column under consideration (column from excel table)
	@Output: None

	Updates the dictionary holding all the dictionaries for each column with a single dictionary for the current column under consideration
"""
def addPKsToDict(dictPrimaryKeys, df, idxCol, prevDF):
	listCols = df.columns.to_list()
	currentColName = listCols[idxCol]

	dfPartial = df[df.columns.to_list()[:idxCol+1]]
	dfPartial = dfPartial.drop_duplicates()

	#reorganize the dfPartial so that the latest column is on the left
	dfPartial = dfPartial[[dfPartial.columns.to_list()[-1]]+dfPartial.columns.to_list()[:-1]]
	dfPartial.sort_values([currentColName], inplace=True) 
	dfPartial.index = np.arange(1, len(dfPartial) + 1)
	dfPartial.index.names = ["Primary Key"]
	# print("dfPartial passed into printTableWithForeignKeys()")
	# print(dfPartial.head())


	printTableWithForeignKeys(idxCol, dfPartial, dictPrimaryKeys, prevDF)

	return dfPartial






"""
printTableWithForeignKeys()
	@Input:
		dfPartial = partial dataframe up to the column corresponding to idxCol of the original excel table
					partial dataframe is already reorganized so that the column under consideration is the left most column
					partial dataframe already has duplicates dropped and a primary key index starting at 1 was implemented

	This is set up to get the foreign key from previous columns.
	It is assumed each right most column is dependent on all of the columns left of the right-most column
"""
def printTableWithForeignKeys(idxCol, dfPartial, dictPrimaryKeys, prevDF):
	print(f"current idxCol = {idxCol}")
	listCols = dfPartial.columns.to_list()
	listColsFK = listCols[1:]
	# print(listColsFK)
	currentColName = listCols[0].replace(" ","_")

	#list holds lists of the foreign keys 
	listForeignKeys = []

	## first column will be a SQL table with no foreign keys
	if (idxCol > 0):

		#go one row at a time and identify all necessary foreign keys 
		row = 0
		# print(f"dfPartial.size = {dfPartial.size}")
		# print(f"dfPartial.shape = {dfPartial.shape}")
		while (row < dfPartial.shape[0]):
		# while (row < 5):

			currentEntry = dfPartial.iloc[row, 0]
			upperEntityColName = listColsFK[-1]

			#filter the previous dataframe until a single row corresponding to the appropriate foreign key is found
			filteredDF = prevDF.copy().reset_index()

			#iteratively filter the df with each foreign key column (from one foreign key column)
			for foreignKeyColumnName in listColsFK:
				idxFKCol = dfPartial.columns.to_list().index(foreignKeyColumnName)
				currentFilter = dfPartial.iloc[row, idxFKCol]
				filteredDF = filteredDF[filteredDF[foreignKeyColumnName] == currentFilter]

			#After filtering, only one row should exist
			idxPKCol = filteredDF.columns.to_list().index("Primary Key")
			foreignKey = filteredDF.iloc[0, idxPKCol]
			# print(f"for row= {row}, foreignKey = {foreignKey}")
			listForeignKeys.append(foreignKey)

			row+= 1


		#Add in the foreign keys
		dfPartial[f"{listColsFK[-1]}_ForeignKey"] = listForeignKeys


	dfPartial.to_excel(f"Col{idxCol +1} - {currentColName}.xlsx")

def main():
	path = r"D:\Coding\100. Projects\1. MicoProjects\Dict From Excel Table\Data.xlsx"
	TableToSQL(path)

main() 