from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.String(), primary_key=True)
    flag = db.Column(db.Integer(), nullable=False)
    players = db.Column(db.Integer(), nullable=False)
    packs = db.Column(db.String(), nullable=False)


    def getPacks(self):
        return json.loads(self.packs)

    def setPacks(self,packs):
        self.packs = json.dumps(packs)

    @classmethod
    def create(cls,id):
        game = Game(id=id,flag=0,packs=json.dumps([{}]),players=0)
        return game.save()

    def save(self):
        try:
            db.session.add(self)
            return self
        except:
            return False

    def update(self):
        self.save()
    
    def delete(self):
        try:
            db.session.delete(self)
            return True
        except:
            return False

    def json(self):
        return {
            'id': self.id,
            'flag': self.flag,
            'packs': self.packs,
            'players': self.players
        }
