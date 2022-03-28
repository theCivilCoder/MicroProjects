def toSQL(dfInput):
	df = dfInput.copy()
	print("inside of DfToSQL.py")
	print(f"df.shape = {df.shape}")

	#list to hold the text that populates the SQL script
	listSQL = []

	listCols = df.columns.to_list()

	# df[listCols[0]] = [value.title() for value in df[listCols[0]].to_list()]
	df.sort_values([listCols[0]], inplace=True) 


	#use the default index beginning with 0
	df = df.reset_index()
	# print(df.head())


	primaryKey = 1

	firstLine = f"INSERT INTO {listCols[0]} (id, "
	for col in listCols:
		firstLine += f"{col.replace(' ','_')}, "
	firstLine = firstLine[:-2] +")"
	listSQL.append(firstLine)
	listSQL.append("VALUES")


	while (primaryKey <= len(df)):
		singleEntry = f"({primaryKey}, "
		# for idx, col in enumerate(listCols[1:]):
		for col in listCols:
			value = df.loc[primaryKey-1, col]
			# print(f"value = {value}")
			if (type(value) == str):
				value = value.title()
				singleEntry += f"'{value}', "
			else:
				singleEntry += f"{value}, "

		singleEntry = singleEntry[:-2]+"),"
		listSQL.append(singleEntry)

		primaryKey += 1


	#replace last comma in the last line with a semicolon
	listSQL[-1] = listSQL[-1][:-1]+";"


	with open(f"./sql/{listCols[0]} SQL.txt", "w") as f:
		for line in listSQL:
			# print(line)
			f.write(line+"\n")


		