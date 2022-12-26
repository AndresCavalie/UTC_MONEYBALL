from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    running = db.Column(db.Boolean,default = False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    searches = db.relationship('Search')
    
class Search(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    subreddits = db.Column(db.String(150))
    keywords = db.Column(db.String(150))
    frequency = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('Post')
    lastcheck = db.Column(db.DateTime(timezone=True), default = func.now())
    lastemail = db.Column(db.DateTime(timezone=True), default = func.now())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    search_id = db.Column(db.Integer, db.ForeignKey('search.id'))
    title = db.Column(db.String(150))
    selftext = db.Column(db.String(300))
    date = db.Column(db.String(40))
    realdate = db.Column(db.String(40))
    keyword = db.Column(db.String(150))
    subreddit = db.Column(db.String(150))
    permalink = db.Column(db.String(150))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    posessions = db.relationship('Possession')
    player1 = db.Column(db.Integer, db.ForeignKey('player.id'),default=1)
    player2 = db.Column(db.Integer, db.ForeignKey('player.id'))
    player3 = db.Column(db.Integer, db.ForeignKey('player.id'))
    player4 = db.Column(db.Integer, db.ForeignKey('player.id'))
    player5 = db.Column(db.Integer, db.ForeignKey('player.id'))
    player6 = db.Column(db.Integer, db.ForeignKey('player.id'))
    player7 = db.Column(db.Integer, db.ForeignKey('player.id'))

class Possession(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    id = db.Column(db.Integer, primary_key = True)
    posessed = db.Column(db.Boolean)
    start = db.Column(db.String(20))
    strigger = db.Column(db.String(20), nullable=True)
    secondary = db.Column(db.String(20), nullable=True)
    usr = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    scr = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    psr = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    shotlocation = db.Column(db.String(5), nullable=True)
    result = db.Column(db.String(5))
    p = db.Column(db.Integer, nullable=True)
    ftmade = db.Column(db.Integer, nullable=True)
    ftattempts = db.Column(db.Integer, nullable=True)
    open3 = db.Column(db.Integer, nullable=True)
    shooter = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    passer = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    catch_shoot = db.Column(db.Integer, nullable=True)
    #ESQ GOES HERE??????
    shotclock = db.Column(db.Integer)
    p1 = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    p2 = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    p3 = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    p4 = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    p5 = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    tag1 = db.Column(db.Integer, nullable=True)    
    tag2 = db.Column(db.Integer, nullable=True)
    tag3 = db.Column(db.Integer, nullable=True)
    tag4 = db.Column(db.Integer, nullable=True)
    tag5 = db.Column(db.Integer, nullable=True)
    offreb = db.Column(db.Integer, nullable=True)
    firsttrigger = db.Column(db.Integer, nullable=True)
    bolt = db.Column(db.Integer, nullable=True)
    painttouchtime = db.Column(db.Integer, nullable=True)
    posttouches = db.Column(db.Integer, nullable=True)
    numpasses = db.Column(db.Integer, nullable=True)
    #NEED PLAYER NAMES AND STUFF HERE??????
    
class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer)
    initials = db.Column(db.String(5))
    name = db.Column(db.String(30))
    #games = db.relationship('Game')
    