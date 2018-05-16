from flask import Flask, render_template, request
from spellcaster import Spellcaster
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/goToForm')
def goToForm():
    classList = ['Bard','Cleric', 'Druid', 'Eldritch Knight', 'Paladin',\
    'Ranger', 'Arcane Trickster', 'Sorcerer', 'Warlock', 'Wizard']
    lvlList = [str(i) for i in range(1,21)]
    modList = [str(i) for i in range(-5,6)]
    return render_template('genForm.html', dropList = classList, lvls = lvlList,\
    mods = modList)

@app.route('/processForm')
def processForm():
    playerClass = request.args.get("classList")
    playerLevel = int(request.args.get("lvl"))
    playerMod = int(request.args.get("mod"))
    otherbooks = request.args.get("otherbooks")

    newChar = Spellcaster(playerClass,playerLevel,playerMod,otherbooks)

    return render_template('results.html', cantraps = newChar.getCantrips())

@app.route('/diceRoller')
def diceRoller():
    return render_template('diceRoller.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
