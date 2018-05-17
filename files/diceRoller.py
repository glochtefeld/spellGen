from random import choice

class Dice:
    def __init__(self, dieSize, diceNumber):
        self.size = dieSize
        self.number = diceNumber
        self.dieRange = [i for i in range(1,self.size+1)]

    # EXPLOSIONS
    def explosion(self, roll_list):
        for i in roll_list:
            if i == self.size:
                newRoll = choice(self.dieRange)
                roll_list.append(newRoll)
        return roll_list

    # GREAT WEAPON FIGHTER
    def gwf(self, roll_list):
        new_list = list()
        for i in roll_list:
            if i < 3:
                new_list.append(choice(self.dieRange))
            else:
                new_list.append(i)

        print(roll_list)
        print(new_list)
        return new_list

    # Really the only class function you need to call
    def roll(self):
        rollList = [choice(self.dieRange) for i in range(self.number)]

        # Explode
        explode1 = self.explosion(rollList)
        # GWF
        gwf1 = self.gwf(explode1)
        # Explode Again
        explode2 = self.explosion(gwf1)
        # Final GWF
        totalRoll = self.gwf(explode2)

        return sum(totalRoll)


def main():
    # You can change these to roll specific dice combinations.
    # Formula is:
    #   variable = Dice( Die Size, Number of Dice )
    #   print( variable.roll() )

    roll = Dice(12,10)
    roll1 = Dice(10,5)
    roll2 = Dice(10,5)
    print(roll.roll())
    print(roll1.roll())
    print(roll2.roll())

if __name__ == '__main__':
    main()
