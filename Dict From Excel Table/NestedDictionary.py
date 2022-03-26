"""
	Couldnt do it, i will take a different approach
"""


def NestedDictionary(dictObj, listKeys, value):
	currentLevelKey = listKeys.pop(0)
	if len(listKeys) > 0:
		print("iteration where len > 0 ---")
		subDictObj = NestedDictionary(dictObj, listKeys, value)
		print(f"latest subDictObj = {subDictObj}")
		dictObj[currentLevelKey] = subDictObj
		# print(f"latest dictObj = {dictObj}")
		return dictObj
	else:
		print("in else")
		print(f"currentLevelKey = {currentLevelKey}, value = {value}")
		dictObj =  newDictionary(currentLevelKey, value)
		print(f"lowest layer, dictObj = {dictObj}")
		return dictObj

def newDictionary(deepestKey, value):
	return {deepestKey:value}

def main():
	dictObj = {}
	listKeys = ["layer1", "layer2"]
	listKeys = ["layer1", "layer2", "layer3"]
	listKeys = ["layer1", "layer2", "layer3", "layer4"]


	NestedDictionary(dictObj, listKeys, "value")
	# dictObj = newDictionary("deepestKey", "value")
	print()
	print("Outside of the recursive function")
	print(dictObj)
	print(dictObj['layer1'])

main()