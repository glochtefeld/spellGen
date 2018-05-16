import math
import records
from random import choice, sample

class Spellcaster:
    def __init__(self, caster, level, modifier=0, otherbooks = None):
        self.caster = caster
        if self.caster == 'Eldritch Knight':
            self.caster = 'eldKnight'
            self.thirdCaster = "Wizard"
        elif self.caster == "Arcane Trickster":
            self.caster = 'arcTrickster'
            self.thirdCaster = "Wizard"

        self.level = level
        self.modifier = modifier
        self.otherbooks = otherbooks

        self.fullCasters = set(['Bard','Cleric','Druid','Sorcerer','Warlock','Wizard'])
        self.halfCasters = set(['Paladin','Ranger'])
        self.thirdCasters = set(['eldKnight','arcTrickster'])
        self.prepared = set(['Cleric','Druid','Paladin','Wizard'])

        db = records.Database("sqlite:///static/databases/classSpells.db")
        sqlCommand = "select * from classSpells where level = "\
        + str(self.level)
        rows = db.query(sqlCommand)
        map = rows.as_dict()

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

        # Picking spells
        spellPath = "sqlite:///static/databases/spellDB.db"
        self.spellDB = records.Database(spellPath)
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
        self.spellRows = self.spellDB.query(spellRequests)
        self.spellMap = self.spellRows.as_dict()
        #print(spellMap)
        #spell = list(choice(spellMap).values())
        #print(spell)


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

    def getMaxSpellLvl(self):
        return self.maxSpellLevel

    def getPrepSpells(self):
        return self.countSpells

    def __str__(self):
        return self.caster + " " + str(self.level)


def main():
    myWiz = Spellcaster('Wizard',5,3, 'XGE')
    print(myWiz)
    print('Highest lvl: ',myWiz.getMaxSpellLvl())
    print('# o Cantraps: ', myWiz.getCantrips())
    print('Prepared Spells: ', myWiz.getPrepSpells())

if __name__ == '__main__':
    main()
