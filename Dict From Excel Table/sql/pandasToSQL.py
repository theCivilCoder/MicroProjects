def toSQL(df):
	print("inside of DfToSQL.py")

	#list to hold the text that populates the SQL script
	listSQL = []

	# df = df.iloc[:10, :]
	print(df.head())

	listCols = df.columns.to_list()

	primaryKey = 1

	firstLine = f"INSERT INTO {listCols[0]} (id, "
	for col in listCols[1:]:
		firstLine += f"{col.replace(' ','_')}, "
	firstLine = firstLine[:-2] +")"
	listSQL.append(firstLine)
	listSQL.append("VALUES")


	while (primaryKey <= len(df)):
		singleEntry = f"('{primaryKey}', "
		# for idx, col in enumerate(listCols[1:]):
		for col in listCols:
			# value = df.iloc[primaryKey-1, idx+1]
			value = df.loc[primaryKey-1, col]
			singleEntry += f"'{value.title()}', "

		singleEntry = singleEntry[:-2]+"),"
		listSQL.append(singleEntry)

		primaryKey += 1


	#replace last comma in the last line with a semicolon
	listSQL[-1] = listSQL[-1][:-1]+";"

	for line in listSQL:
		print(line)

		