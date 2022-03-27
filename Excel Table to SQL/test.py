import pandas as pd
import sql.pandasToSQL as toolSQL

df = pd.read_excel(r"D:\Coding\100. Projects\1. MicoProjects\Excel Table to SQL\Data.xlsx")


# toolSQL.toSQL(df)


col = list(set(df[df.columns.to_list()[-1]].to_list()))
col.sort()
for entry in col:
	print(entry)
