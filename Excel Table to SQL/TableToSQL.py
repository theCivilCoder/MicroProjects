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
	# For each column after the first column, add the respective foreign keys
	idxCol = 0
	prevDF = None
	while (idxCol < len(listCols)):
		prevDF = prepDF(df, idxCol, prevDF)
		idxCol += 1
		print("-"*150)
	print("")


"""
prepDF()
	@Inputs:
		df = entire dataframe
		idxCol = index of the column from the excel table which is currently under consideration
		prevDF = the partial dataframe from the previous iteration (this is the corresponding table which the current column will have a foreign key to)
	@Output: 
		dfPartial = the partial dataframe for the current column column under consideration (this will become the prevDF for the next column)

	Updates the dictionary holding all the dictionaries for each column with a single dictionary for the current column under consideration
"""
def prepDF(df, idxCol, prevDF):
	listCols = df.columns.to_list()
	currentColName = listCols[idxCol]
	# print()
	# print(f"idxCol = {idxCol}, currentColName = {currentColName} **Jimmy**")

	#create the partial dataframe holding the dataframe corresponding to the current column under consideration
	dfPartial = df[df.columns.to_list()[:idxCol+1]]

	#drop the duplicate rows
	dfPartial = dfPartial.drop_duplicates()

	#reorganize the dfPartial so that the latest column is on the left
	dfPartial = dfPartial[[dfPartial.columns.to_list()[-1]]+dfPartial.columns.to_list()[:-1]]
	
	#sort all rows by the current column under consideration
	dfPartial.sort_values([currentColName], inplace=True) 

	dfPartial.index = np.arange(1, len(dfPartial) + 1)
	dfPartial.index.names = ["Primary Key"]

	#Add the Foreign Keys
	printTableWithForeignKeys(idxCol, dfPartial, prevDF)

	return dfPartial



"""
printTableWithForeignKeys()
	@Input:
		idxCol = index of the column from the excel table which is currently under consideration
		prevDF = the partial dataframe from the previous iteration (this is the corresponding table which the current column will have a foreign key to)
		dfPartial = partial dataframe up to the column corresponding to idxCol of the original excel table
					partial dataframe is already reorganized so that the column under consideration is the left most column
					partial dataframe already has duplicates dropped and a primary key index starting at 1 was implemented

	This is set up to get the foreign key from previous columns.
	It is assumed each right most column is dependent on all of the columns left of the right-most column
"""
def printTableWithForeignKeys(idxCol, dfPartial, prevDF):
	listCols = dfPartial.columns.to_list()
	listColsFK = listCols[1:]
	# print(listColsFK)
	currentColName = listCols[0].replace(" ","_")
	print(f"current idxCol = {idxCol}, current column name = {currentColName}")


	#list holds lists of the foreign keys 
	listForeignKeys = []

	## first column will be a SQL table with no foreign keys
	if (idxCol > 0):

		#go one row at a time and identify all necessary foreign keys 
		row = 0
		# print(f"dfPartial.size = {dfPartial.size}")
		# print(f"dfPartial.shape = {dfPartial.shape}")
		while (row < dfPartial.shape[0]):

			currentEntry = dfPartial.iloc[row, 0]
			upperEntityColName = listColsFK[-1]

			#filter the previous dataframe until a single row corresponding to the appropriate foreign key is found
			filteredDF = prevDF.copy().reset_index()
			# print("filteredDF before filtering")
			# print(filteredDF.shape)
			# print(filteredDF.head())

			#iteratively filter the df with each foreign key column (from one foreign key column)
			for foreignKeyColumnName in listColsFK:
				idxFKCol = dfPartial.columns.to_list().index(foreignKeyColumnName)
				currentFilter = dfPartial.iloc[row, idxFKCol]
				# print(f"currentFilter = {currentFilter}")
				filteredDF = filteredDF[filteredDF[foreignKeyColumnName] == currentFilter]

			# print("filteredDF after filtering")
			# print(filteredDF.shape)
			# print(filteredDF.head())

			#After filtering, only one row should exist
			idxPKCol = filteredDF.columns.to_list().index("Primary Key")
			foreignKey = filteredDF.iloc[0, idxPKCol]
			# print(f"for row= {row}, foreignKey = {foreignKey}")
			listForeignKeys.append(foreignKey)

			row+= 1


		#Add in the foreign keys
		dfPartial[f"{listColsFK[-1]}_ForeignKey"] = listForeignKeys


		#Remove the original foreign key column(s)
		listCols = dfPartial.columns.to_list()
		numColsFK = len(listColsFK)
		# print(f"numColsFK = {numColsFK}")
		# print("listCols before removal: ")
		# print(listCols)
		colsToKeep = [listCols[0]] + [listCols[numColsFK+1]]
		# print("listCols after removal: ")
		# print(colsToKeep)

		dfPartial = dfPartial[colsToKeep]

	dfPartial.to_excel(f"Col{idxCol +1} - {currentColName}.xlsx")

	# generate the sql script for inserting the data to a sql table
	print()
	toolSQL.toSQL(dfPartial)



def main():
	path = r"D:\Coding\100. Projects\1. MicoProjects\Excel Table to SQL\Data.xlsx"
	TableToSQL(path)

main() 