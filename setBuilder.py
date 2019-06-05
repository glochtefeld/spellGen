classes = ['bard','cleric','druid','paladin','ranger','sorcerer','warlock','wizard']
path = input("Book [PHB/XGE]: ")

classDictionary = dict()

for cls in classes:
    with open(path + "/" + cls + ".spells","r") as inFile:
        clsSet = set()
        for line in inFile:
            line = line.strip()
            clsSet.add(line)
        print(clsSet)
        classDictionary.update({cls:clsSet})
print(classDictionary)

with open(path + 'Class.spells','w+') as outFile:
    outFile.write(str(classDictionary))
