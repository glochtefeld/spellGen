import csv

def openDict(book):
    # passed a string to open specific file.
    # File contains a dictionary stored as a string.
    path = book + "Class.spells"
    with open(path, 'r') as inFile:
        for line in inFile:
            spells = eval(line.strip())
        return spells #Only one line, but COULD BE MORE!

def classCheck(name, spellDict):
    # checks if spell in spell list.
    classes = list(spellDict.keys())
    classList = list()

    for cls in classes:
        if name in spellDict[cls]:
            classList.append(1)
        else:
            classList.append(0)

    print(classList)
    return classList

def main():
    book = "PHB"
    spellDict = openDict(book) # returns dictionary of class:set(spells)

    autoComplete = {
                    'ab':'Abjuration',
                    'co':'Conjuration',
                    'di':'Divination',
                    'en':'Enchantment',
                    'ev':'Evocation',
                    'il':'Illusion',
                    'ne':'Necromancy',
                    'tr':'Transmutation'}
    try: # Input spells
        while True: # BAD FORM, but excepts KeyboardInterrupt
            name = input("Name (Double check sp.): ")
            spellLevel = int(input("Level: "))
            while spellLevel > 9 or spellLevel < 0:
                print("not a level")
                spellLevel = int(input("Level: "))

            # Probably should make sure that 1/0 is input for most of these.
            # Expect this in v1.1! New feature.

            print(list(autoComplete.keys()),end='')
            print()
            school = input("School: ")
            verbal = int(input("Verbal [1/0]: "))
            somatic = int(input("Somatic [1/0]: "))
            print("0: None | 1: No Cost | 2: Cost | 3: Consumed Cost|4:Consumed Mat., no cost")
            material = int(input("Material [0-4]: "))
            ritual = int(input("Ritual [1/0]: "))
            conc = int(input("Concentration [1/0]: "))
            page = int(input("Page: "))

            # Returns list (interpreted by db code)
            classAssign = classCheck(name, spellDict)

            # Line breaks look better
            row = [spellLevel,name,autoComplete[school],verbal,somatic, material,ritual]
            row += classAssign
            row += [conc,book,page]

            with open('spellsDB.csv','a+') as outFile:
                print('writing to db...')
                nuWriter = csv.writer(outFile, delimiter=',')
                nuWriter.writerow(row)
            print('Written.')

    except KeyboardInterrupt:
        print('\nExiting.')

if __name__ == '__main__':
    main()
