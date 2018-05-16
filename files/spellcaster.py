import math
import records
from random import choice, sample
import operator


class Spellcaster:
    def __init__(self, caster, level, modifier=0, otherbooks = None):
        self.caster = caster
        self.level = level
        self.modifier = modifier
        self.otherbooks = otherbooks

        # Third Caster class resetting
        if self.caster == 'Eldritch Knight':
            self.caster = 'eldKnight'
            self.thirdCaster = "Wizard"
        elif self.caster == "Arcane Trickster":
            self.caster = 'arcTrickster'
            self.thirdCaster = "Wizard"

        # Class Separations
        self.fullCasters = set(['Bard','Cleric','Druid','Sorcerer','Warlock','Wizard'])
        self.halfCasters = set(['Paladin','Ranger'])
        self.thirdCasters = set(['eldKnight','arcTrickster'])
        self.prepared = set(['Cleric','Druid','Paladin','Wizard'])

        # Number of spells / cantrips by level
        db = records.Database("sqlite:///static/databases/classSpells.db")
        sqlCommand = "select * from classSpells where level = "\
        + str(self.level)
        rows = db.query(sqlCommand)
        map = rows.as_dict()

        # SPELL DATABASE
        spellPath = "sqlite:///static/databases/spellDB.db"
        self.spellDB = records.Database(spellPath)

        # Determine highest spell slot
        if self.caster in self.fullCasters: # Full casters
            self.maxSpellLevel = math.ceil(self.level / 2)
        elif self.caster in self.halfCasters: # Half Casters
            if self.level == 1:
                self.maxSpellLevel = -1
            else:
                self.maxSpellLevel = math.ceil(self.level / 4)
        else: # Third casters; don't get spells until lvl 3
            if self.level < 3:
                self.maxSpellLevel = -1
            else:
                self.maxSpellLevel = math.ceil(self.level / 6)
        if self.maxSpellLevel > 9: # Max spell level is 9
            self.maxSpellLevel = 9

        # Determine # of prepared spells
        if self.caster in self.prepared: # Only a few prepared casters
            self.countSpells = self.level + self.modifier
            if self.countSpells < 1:
                self.countSpells = 1
        else: # DB integration. Reads level row; returns # of spells known.
            self.countSpells = map[0][self.caster]


        # Determine Cantrips
        if self.caster in self.halfCasters:
            self.cantrips = -1
        else:
            dbCol = self.caster + "Cantrips"
            self.cantrips = map[0][dbCol]

    def getCantrips(self):
        # Returns a list of lists filled with cantrip info to be for tables
        if self.otherbooks:
            canRequest = "select Name,School,Verbal,Somatic\
            ,Material,Concentration,Source,Page from spellDB where " +\
            self.caster + " = 1 AND SpellLevel = 0"
        else:
            canRequest = "select Name,School,Verbal,Somatic\
            ,Material,Concentration,Source,Page from spellDB where " +\
            self.caster + " = 1 AND SpellLevel = 0 AND Source = 'PHB'"
        spellRows = self.spellDB.query(canRequest)
        spellMap = spellRows.as_dict()
        #print(spellMap)

        try: # Database isn't complete; can request more spells than exist.
            canList = sample(spellMap, self.cantrips)
        except ValueError as v:
            print('Not enough spells in DB.')
            canList = list(spellMap)

        for i in range(len(canList)):
            canList[i] = list(canList[i].values())

            # Changes 0/1 into Y/N (easier than changing db)
            for j in range(2,6):
                if canList[i][j] == 1:
                    canList[i][j] = 'Yes'
                elif canList[i][j] == 0:
                    canList[i][j] = 'No'

        return canList

    def getSpells(self):
        # Picking spells
        if self.otherbooks:
            spellRequests = "select SpellLevel,Name,School,Verbal,Somatic\
            ,Material,Concentration,Source,Page from spellDB where " +\
            self.caster + " = 1 AND SpellLevel <= " + str(self.maxSpellLevel) +\
            " AND SpellLevel > 0"
        else:
            spellRequests = "select SpellLevel,Name,School,Verbal,Somatic\
            ,Material,Concentration,Source,Page from spellDB where " +\
            self.caster + " = 1 AND SpellLevel <= " + str(self.maxSpellLevel) +\
            " AND SpellLevel > 0 AND Source = 'PHB'"
        spellRows = self.spellDB.query(spellRequests)
        spellMap = spellRows.as_dict()

        try: # Database isn't complete; can request more spells than exist.
            spellList = sample(spellMap, self.countSpells)
        except ValueError as v:
            print('Not enough spells in DB.')
            spellList = list(spellMap)

        for i in range(len(spellList)):
            spellList[i] = list(spellList[i].values())

            # Changes 0/1 into Y/N (easier than changing db)
            for j in range(3,7):
                if spellList[i][j] == 1:
                    spellList[i][j] = 'Yes'
                elif spellList[i][j] == 0:
                    spellList[i][j] = 'No'

        spellList = sorted(spellList, key=operator.itemgetter(0))

        return spellList

    def getMaxSpellLvl(self):
        return self.maxSpellLevel

    def getPrepSpells(self):
        return self.countSpells


def main():
    myWiz = Spellcaster('Wizard',5,3, True)
    print(myWiz)
    print('Highest lvl: ',myWiz.getMaxSpellLvl())
    print('Cantraps: ')
    for i in myWiz.getCantrips():
        print(i)
    print('Prepared Spells: ', myWiz.getPrepSpells())
    print("Spells: ")
    for i in myWiz.getSpells():
        print(i)

if __name__ == '__main__':
    main()
