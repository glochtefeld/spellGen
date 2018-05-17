from flask import Flask, render_template, request
from spellcaster import Spellcaster
from diceRoller import Dice
from random import choice
app = Flask(__name__)

# Home Directory
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Form')
def goToForm():
    classList = ['Bard','Cleric', 'Druid', 'Paladin','Ranger', 'Sorcerer',\
    'Warlock', 'Wizard']
    lvlList = [str(i) for i in range(1,21)]
    modList = [str(i) for i in range(-5,6)]
    return render_template('genForm.html', dropList = classList,\
    lvls = lvlList, mods = modList)

@app.route('/processForm')
def processForm():
    playerClass = request.args.get("classList")
    playerLevel = int(request.args.get("lvl"))
    playerMod = int(request.args.get("mod"))
    otherbooks = request.args.get("otherbooks")

    newChar = Spellcaster(playerClass,playerLevel,playerMod,otherbooks)

    return render_template('results.html',cantraps = newChar.getCantrips(),\
    spells = newChar.getSpells())

@app.route('/diceRoller')
def diceRoller():
    edgeList = ["A THOUSAND YEARS OF DARKNESS", 'KNIVES', 'DEATH', 'VAGUE HORROR ETC', 'POWER WORD: KILL']
    return render_template('diceRoller.html', evanList = choice(edgeList))

@app.route('/diceCompute')
def diceCompute():
    dieSize = int(request.args.get("dieSize"))
    numDies = int(request.args.get("numDies"))
    print(dieSize,numDies)
    newRoll = Dice(dieSize, numDies)
    quotes=['Impossible!','Rigged.','Natural [INSERT ROLL HERE]!','Gnarly.',\
    'Tubular.','Lorem Ipsum!','.']
    edgeList = ["A THOUSAND YEARS OF DARKNESS", 'KNIVES', 'DEATH', 'VAGUE HORROR ETC', 'POWER WORD: KILL']

    return render_template('diceRoller.html', roll = newRoll.roll(),\
    rolled=True, quote=choice(quotes), evanList = choice(edgeList))

@app.route('/evanRoll')
def evanRoll():
    roll1 = Dice(6,5)
    roll2 = Dice(10,12)
    roll3 = Dice(12,5)

    r1 = roll1.roll()
    r2 = roll2.roll()
    r3 = roll3.roll()

    quotes=['Impossible!','Rigged.','Natural [INSERT ROLL HERE]!','Gnarly.',\
    'Tubular.','Lorem Ipsum!','.']
    edgeList = ["A THOUSAND YEARS OF DARKNESS", 'KNIVES', 'DEATH', 'VAGUE HORROR ETC', 'POWER WORD: KILL']
    returnString = str(r1) + " + " + str(r2) + " + " + str(r3)
    evanPhrase = choice(edgeList)

    return render_template('diceRoller.html', evanList = evanPhrase, roll = r1+r2+r3,\
    rolled=True, quote=choice(quotes), retStr = returnString)

@app.route('/ogl')
def ogl():
    return render_template('ogl.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
