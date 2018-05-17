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
    return render_template('diceRoller.html')

@app.route('/diceCompute')
def diceCompute():
    dieSize = int(request.args.get("dieSize"))
    numDies = int(request.args.get("numDies"))
    print(dieSize,numDies)
    newRoll = Dice(dieSize, numDies)
    quotes=['Impossible!','Rigged.','Natural [INSERT ROLL HERE]!','Gnarly.',\
    'Tubular.','Lorem Ipsum!','.']

    return render_template('diceRoller.html', roll = newRoll.roll(),\
    rolled=True, quote=choice(quotes))


@app.route('/ogl')
def ogl():
    return render_template('ogl.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
