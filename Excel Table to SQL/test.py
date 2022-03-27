import pandas as pd
import sql.pandasToSQL as toolSQL

df = pd.read_excel(r"D:\Coding\100. Projects\1. MicoProjects\Dict From Excel Table\Data.xlsx")


toolSQL.toSQL(df)