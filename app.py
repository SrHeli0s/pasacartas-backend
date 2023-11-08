import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import random
import string
import json
import csv
import random
import copy
import time
from config import config 
from models import Game, db

def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

enviroment = config["development"]
app = create_app(enviroment)
CORS(app)

commonCards = []
uncommonCards = []
rareCards = []
epicCards = []
legendaryCards = []

mods = {}
probs = {}
minProbAfterMod = 0

nCards = 0
nPacks = 0

engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

def generateSobre(id):
    global mods
    global probs
    global commonCards
    global uncommonCards
    global rareCards
    global epicCards
    global legendaryCards
    output = []
    for x in range(nPacks):
        localCommonCards = copy.deepcopy(commonCards)
        localUncommonCards = copy.deepcopy(uncommonCards)
        localRareCards = copy.deepcopy(rareCards)
        localEpicCards = copy.deepcopy(epicCards)
        localLegendaryCards = copy.deepcopy(legendaryCards)
        localprobability = copy.deepcopy(probs)

        if nCards>0:
            n = nCards
        else:
            if (id==0): 
                n = 1
            else:
                game = Game.query.filter_by(id=id).first()
                if game is None:
                    return jsonify({'message': 'Game does not exists'}), 404
                n = game.players+1
        
          

        for i in range(n):
            rng = random.random()
            if rng < localprobability["common"]: #Common card
                #Generate card
                new = random.choice(localCommonCards)
                localCommonCards.remove(new)
                new.append('common')
                output.append(new)
                #Apply modifications to probability
                localprobability["common"] = localprobability["common"] + mods['commonpick']['commonmod']
                localprobability["uncommon"] = localprobability["uncommon"] + mods['commonpick']['uncommonmod']
                localprobability["rare"] = localprobability["rare"] + mods['commonpick']['raremod']
                localprobability["epic"] = localprobability["epic"] + mods['commonpick']['epicmod']
                localprobability["legendary"] = localprobability["legendary"] + mods['commonpick']['legendarymod']
                #Fix if any modifications crossed the limit
                for i in localprobability:
                    if localprobability[i] < minProbAfterMod: localprobability[i] = minProbAfterMod 
                

            elif rng < localprobability["common"] + localprobability["uncommon"]: #Uncommon card
                #Generate card
                new = random.choice(localUncommonCards)
                localUncommonCards.remove(new)
                new.append('uncommon')
                output.append(new)
                #Apply modifications to probability
                localprobability["common"] = localprobability["common"] + mods['uncommonpick']['commonmod']
                localprobability["uncommon"] = localprobability["uncommon"] + mods['uncommonpick']['uncommonmod']
                localprobability["rare"] = localprobability["rare"] + mods['uncommonpick']['raremod']
                localprobability["epic"] = localprobability["epic"] + mods['uncommonpick']['epicmod']
                localprobability["legendary"] = localprobability["legendary"] + mods['uncommonpick']['legendarymod']
                #Fix if any modifications crossed the limit
                for i in localprobability:
                    if localprobability[i] < minProbAfterMod: localprobability[i] = minProbAfterMod 

            elif rng < localprobability["common"] + localprobability["uncommon"] + localprobability["rare"]: #Rare card
                #Generate card
                new = random.choice(localRareCards)
                localRareCards.remove(new)
                new.append('rare')
                output.append(new)
                #Apply modifications to probability
                localprobability["common"] = localprobability["common"] + mods['rarepick']['commonmod']
                localprobability["uncommon"] = localprobability["uncommon"] + mods['rarepick']['uncommonmod']
                localprobability["rare"] = localprobability["rare"] + mods['rarepick']['raremod']
                localprobability["epic"] = localprobability["epic"] + mods['rarepick']['epicmod']
                localprobability["legendary"] = localprobability["legendary"] + mods['rarepick']['legendarymod']
                #Fix if any modifications crossed the limit
                for i in localprobability:
                    if localprobability[i] < minProbAfterMod: localprobability[i] = minProbAfterMod 

            elif rng < localprobability["common"] + localprobability["uncommon"] + localprobability["rare"] + localprobability["epic"]: #Epic card
                #Generate card
                new = random.choice(localEpicCards)
                localEpicCards.remove(new)
                new.append('epic')
                output.append(new)
                #Apply modifications to probability
                localprobability["common"] = localprobability["common"] + mods['epicpick']['commonmod']
                localprobability["uncommon"] = localprobability["uncommon"] + mods['epicpick']['uncommonmod']
                localprobability["rare"] = localprobability["rare"] + mods['epicpick']['raremod']
                localprobability["epic"] = localprobability["epic"] + mods['epicpick']['epicmod']
                localprobability["legendary"] = localprobability["legendary"] + mods['epicpick']['legendarymod']
                #Fix if any modifications crossed the limit
                for i in localprobability:
                    if localprobability[i] < minProbAfterMod: localprobability[i] = minProbAfterMod 

            else: #Legendary card
                #Generate card
                new = random.choice(localLegendaryCards)
                localLegendaryCards.remove(new)
                new.append('legendary')
                output.append(new)
                #Apply modifications to probability
                localprobability["common"] = localprobability["common"] + mods['legendarypick']['commonmod']
                localprobability["uncommon"] = localprobability["uncommon"] + mods['legendarypick']['uncommonmod']
                localprobability["rare"] = localprobability["rare"] + mods['legendarypick']['raremod']
                localprobability["epic"] = localprobability["epic"] + mods['legendarypick']['epicmod']
                localprobability["legendary"] = localprobability["legendary"] + mods['legendarypick']['legendarymod']
                #Fix if any modifications crossed the limit
                for i in localprobability:
                    if localprobability[i] < minProbAfterMod: localprobability[i] = minProbAfterMod 
        
    return output



#Creates a new game
@app.route("/new", methods=['GET'])
def newGame():
    db.session.begin()
    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    game = Game.create(id)

    db.session.commit()

    print("Created game "+id)
    return { 'code':id,'playerid':0 }

#Joins a new game and gets the correspondant playerID
@app.route("/join/<id>", methods=['GET'])
def joinGame(id):
    db.session.begin()
    
    game = Game.query.filter_by(id=id).with_for_update().one()

    if game is None:
        return jsonify({'message': 'Game does not exists'}), 404

    print("JOIN ANTES", game.json())
    game.players += 1

    packs = game.getPacks()
    packs.append({})
    game.setPacks(packs)

    game.update()
    print("JOIN DESPUES", game.json())
    db.session.commit()

    return { 'code':id,'playerid':game.players }

#Starts a game and gets the first pack. Only executed by host
@app.route("/start/<id>", methods=['POST'])
def startGame(id):
    db.session.begin()
    game = Game.query.filter_by(id=id).with_for_update().one()
    if game is None:
        return jsonify({'message': 'Game does not exists'}), 404
    
    data = json.loads(request.data.decode('utf-8'))
    playerid = data['playerid']

    if playerid!=0: return

    print("START ANTES:",game.json())
    packs = game.getPacks()
    for i in range(game.players+1):
        packs[i] = copy.deepcopy(generateSobre(id))
    game.setPacks(packs)

    game.flag = 1

    game.update()

    print("START DESPUES:",game.json())
    db.session.commit()

    return {"pack":packs[playerid]}

#Check if game is ready to start
@app.route("/gamestarted/<id>", methods=['POST'])
def isReadyGame(id):
    game = Game.query.filter_by(id=id).first()
    if game is None:
        return jsonify({'message': 'Game does not exists'}), 404
    
    data = json.loads(request.data.decode('utf-8'))
    playerid = data['playerid']

    if game.flag == 1:
        return {"state":1,"pack":game.getPacks()[playerid]}
    else:
        return {"state":0}

@app.route("/generatePack", methods=['GET'])
def generate_pack():
    return {'pack': generateSobre(0)}

@app.route("/getAll", methods=['GET'])
def get_all():
    global commonCards
    global uncommonCards
    global rareCards
    global epicCards
    global legendaryCards
    return {'common': commonCards, 'uncommon':uncommonCards, 'rare':rareCards, 'epic':epicCards, 'legendary':legendaryCards}

#Picks the card n from the pack of the player
@app.route("/pick/<id>/<n>", methods=['POST'])
def pick_card(id,n):
    db.session.begin()
    game = Game.query.filter_by(id=id).with_for_update().one()
    if game is None:
        return jsonify({'message': 'Game does not exists'}), 404

    data = json.loads(request.data.decode('utf-8'))
    playerid = data['playerid']

    packs = game.getPacks()
    packs[playerid].pop(int(n))
    game.setPacks(packs)

    print("[P",playerid,"] Pick card ",int(n),". State of packs:",game.getPacks()[playerid])


    #Check if is the last player to pick
    lastPlayer = True
    for i in range(len(packs)):
        if i != playerid and len(packs[i]) != len(packs[playerid]): lastPlayer = False
    
    if lastPlayer: 
        packs.append(packs.pop(0))
        game.setPacks(packs)

    game.update()
    db.session.commit()

    return {}

#Checks if all players picked. If so the next pack is sent
@app.route("/isready/<id>", methods=['POST'])
def isReadyNextRound(id):
    game = Game.query.filter_by(id=id).first()
    if game is None:
        return jsonify({'message': 'Game does not exists'}), 404

    data = json.loads(request.data.decode('utf-8'))
    playerid = data['playerid']
    packs = game.getPacks()
    
    isReady = True
    for i in range(len(packs)):
        print("Check:",playerid,"(",len(packs[playerid]),")",i,"(",len(packs[i]),")")
        if i != playerid and len(packs[i]) != len(packs[playerid]): isReady = False

    if isReady:
        return {"state":1,"pack":packs[playerid]}
    else:
        return {"state":0}

#Gets the configuration
@app.route("/conf", methods=['GET'])
def get_conf():
    global conf

    return {"data":conf}

#Loads a configuration
@app.route("/conf", methods=['POST'])
def load_conf():
    data = json.loads(request.data.decode('utf-8'))
    load_settings(data['data'])

    return {}



#Load the data from the app
data_dir = "static/"
def load_data():
    #Load cards
    with open(data_dir+'1common.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            commonCards.append(row)
    with open(data_dir+'2uncommon.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            uncommonCards.append(row)
    with open(data_dir+'3rare.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            rareCards.append(row)
    with open(data_dir+'4epic.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            epicCards.append(row)
    with open(data_dir+'5legendary.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            legendaryCards.append(row)
    
    load_settings(None)

#Load settings
def load_settings(data):
    if data==None:
        with open(data_dir+'settings.json','r') as f:
            data = json.load(f)
    
    global conf
    conf = data
    global mods 
    mods = data["modifications"]
    global probs
    probs = data["probabilities"]
    global minProbAfterMod
    minProbAfterMod = data["minProbAfterMod"]
    global nCards
    nCards = data["nCardsInPack"]
    global nPacks    
    nPacks = data["nPacks"]

with app.app_context():
    load_data()
    print("Data loaded successfully!")