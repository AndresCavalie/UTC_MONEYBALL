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
    
game_player = db.Table( #ASSOCIATION TABLE
    "game_player",
    db.metadata,
    db.Column("game_id", db.ForeignKey('game.id'), primary_key = True),
    db.Column("player_id", db.ForeignKey('player.id'), primary_key = True)
)

touches = db.Table( #ASSOCIATION TABLE
    "touches",
    db.metadata,
    db.Column("posession_id", db.ForeignKey('possession.id'), primary_key = True),
    db.Column("player_id", db.ForeignKey('player.id'), primary_key = True)
)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    team = db.Column(db.String)
    # date = db.Column(db.DateTime(timezone=True), nullable= True)
    date = db.Column(db.String, nullable= True)
    
    players = db.relationship("Player", secondary = game_player, backref="games")
    possessions = db.relationship('Possession')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    number = db.Column(db.Integer)
    initials = db.Column(db.String(5))
    name = db.Column(db.String(30))
    
class Possession(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    players = db.relationship("Player", secondary = touches, backref="posessions")
    possnum = db.Column(db.Integer)
    tagstart = db.Column(db.String(30), nullable=True)
    poss = db.Column(db.Boolean)
    start = db.Column(db.String(20))
    shottrigger = db.Column(db.String(20), nullable=True)
    secondary = db.Column(db.String(20), nullable=True)
    usr = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    scr = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    psr = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    shot = db.Column(db.String(5), nullable=True)
    result = db.Column(db.String(5))
    assist = db.Column(db.Integer, nullable=True)
    ftm = db.Column(db.Integer, nullable=True)
    fta = db.Column(db.Integer, nullable=True)
    open3 = db.Column(db.Integer, nullable=True)
    
    
    #USR SCR PSR Shooter Passer P1 P2 P3 P4 P5
    
    
    
    shooter = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    passer = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    csjumper = db.Column(db.Integer, nullable=True)
    esq = db.Column(db.Numeric(precision = 3, scale = 2),nullable=True)
    #ESQ GOES HERE??????
    shotclock = db.Column(db.Integer,nullable=True)
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
    
    r2 = db.Column(db.Integer)
    pm2 = db.Column(db.Integer)
    pt2 = db.Column(db.Integer)
    np2 = db.Column(db.Integer)
    pt3 = db.Column(db.Integer)
    np3 = db.Column(db.Integer)
    d3 = db.Column(db.Integer)
    sb3 = db.Column(db.Integer)
    ft = db.Column(db.Integer)
    points = db.Column(db.Integer)

    
    #games = db.relationship('Game')
    