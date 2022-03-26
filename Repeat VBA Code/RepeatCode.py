##2021-09-16
## Quickly repeats prints out new code which can be copied over to VBA

# f = open(r"D:\Coding\100. Projects\1. MicoProjects\Repeat VBA Code\Original.txt","r")
# for line in f:
# 	print(line)

numRepetitions = 5
toReplace1 = "ShowWeek1"
toReplace2 = "E:L"
toReplace3 = "E3"




newCode = []
dictReplacements = {
	"Replacement1":[],
	"Replacement2":[],
	"Replacement3":[]
}


## autofill list of replacements #1
listRep1 = []
for repNum in range(2,numRepetitions+1):
	# print(repNum)
	listRep1.append(toReplace1[:-1]+str(repNum))
# print(listRep1)
dictReplacements['Replacement1'] = listRep1

## manually type in list of replacements #2
listRep2 = "M:T U:AB AC:AJ AK:AR".split(" ")
dictReplacements['Replacement2'] = listRep2

## manually type in list of replacements #2
listRep3 = "M3 U3 AC3 AK3".split(" ")
dictReplacements['Replacement3'] = listRep3



for idx, repNum in enumerate(range(2,numRepetitions+1)):
	f = open(r"D:\Coding\100. Projects\1. MicoProjects\Repeat VBA Code\Original.txt","r")
	# print(f" -------------------------------- {idx}")
	rep_i1 = dictReplacements["Replacement1"][idx]
	rep_i2 = dictReplacements["Replacement2"][idx]
	rep_i3 = dictReplacements["Replacement3"][idx]

	for line in f:
		# print(line.replace(toReplace1, rep_i1).replace(toReplace3, rep_i3).replace("\n",""))
		print(line.replace(toReplace1, rep_i1).replace(toReplace2, rep_i2).replace(toReplace3, rep_i3).replace("\n",""))
		# print(line)