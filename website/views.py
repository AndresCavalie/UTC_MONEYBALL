from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for,session
from flask_login import login_required, current_user
views = Blueprint('views',__name__)
from .models import Note, Search, Post, Info, Game, Possession, Player
from . import db, rmt
import json
import pandas as pd
import time
import os
from os.path import join, dirname, realpath
import openpyxl
from pathlib import Path
from sqlalchemy import and_, or_
from decimal import *




@views.route('/players', methods=['GET','POST'])
@login_required
def players():
    # players = db.session.query(Player).join(Search).filter(Search.user_id == User.id).all()
    players = db.session.query(Player).all()
    print(players)
    fgm = []
    fga = []
    fgm3 = []
    fga3 = []
    efg = []
    ftm = []
    fta = []
    ftperc = []
    assist = []
    esq = []
    for player in players:
            getcontext().prec = 3
            fgm_ = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make")).count())
            fgm3_ = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id, Possession.result=="Make", (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
            fga_ = Decimal(db.session.query(Possession).filter(Possession.shooter==player.id).count())
            if fga_ != 0:
                
                efg_ = ((fgm_ + (Decimal(.5)*fgm3_)) / fga_)* (Decimal(100))
                efg.append(efg_)
            else:
                efg.append(None)
            fgm.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make")).count())
            fga.append(db.session.query(Possession).filter(Possession.shooter==player.id).count())
            fgm3.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, Possession.result=="Make", (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
            fga3.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
            ftm.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.ftm==1, Possession.ftm ==2)))).count())
            ftm_ = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.ftm==1, Possession.ftm ==2)))).count())
            fta.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.fta==1, Possession.fta ==2)))).count())
            fta_ = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.fta==1, Possession.fta ==2)))).count())
            esq_ = db.session.query(Possession.esq).filter(and_(Possession.shooter==player.id,Possession.result=="Make")).all()
            sum = Decimal(0)
            for x in esq_:
                sum += x[0]
            esq_ = sum
            if fga_ != 0:
                
                esq_ = (esq_ / fga_)#* Decimal(100)
                esq.append(esq_)
            else:
                esq.append(None)
            if fta_ != 0:
                
                ftperc_ = (ftm_ / fta_) * (Decimal(100))
                ftperc.append(ftperc_)
            else:
                ftperc.append(None)
                
            assist.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.assist==1)).count())
            
            
            print(fgm)
    print(fgm)
    return render_template("players.html",user=current_user,players=players, fgm = fgm , fga = fga, fgm3 = fgm3 , fga3 =fga3, efg=efg, ftm=ftm, fta=fta, ftperc = ftperc, assist = assist, esq = esq)

@views.route('/games', methods=['GET','POST'])
@login_required
def games():
    return render_template("home.html",user=current_user)

@views.route('/triggers', methods=['GET','POST'])
@login_required
def triggers():
    return render_template("home.html",user=current_user)
    
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        sheet = request.files['data']
        df = pd.read_excel(sheet)
        #from one spreadsheet, create one game, and posessions with players
        playerlist = []
        
        game = Game(team = df.loc[0,"Opp"],date = str(df.loc[0,"Date"]) ) #, date = df.loc[i,"Date"])
        db.session.add(game)
        db.session.commit()
        for i in range(len(df)):
            # if i == 0:
            #     game = Game(team = df.loc[i,"Opp"],date = str(df.loc[i,"Date"]) ) #, date = df.loc[i,"Date"])
            #     db.session.add(game)
            #     db.session.commit()   
            # print(i)
            
            tagstart = (df.loc[i, "Tag Start"])
            if tagstart == tagstart:
                tagstart = str(tagstart)
            
            print("usr")  
            usr = (df.loc[i, "Usr"])
            if usr == usr:
                usr = Player.query.filter_by(initials=usr).first()
                print(usr)
                if usr not in playerlist:
                    playerlist.append(usr)
                usr = usr.id
                
            
            print("scr")       
            scr = (df.loc[i, "Scr"])
            if scr == scr:
                scr = Player.query.filter_by(initials=scr).first()
                print(scr)
                if scr not in playerlist:
                    playerlist.append(scr)
                scr = scr.id
                
            
            print("psr")   
            psr = (df.loc[i, "Psr"])
            if psr == psr:
                psr = Player.query.filter_by(initials=psr).first()
                print(psr)
                if psr not in playerlist:
                    playerlist.append(psr)
                psr = psr.id
                
            print("shooter")  
            shooter = (df.loc[i, "Shooter"])
            if shooter == shooter:
                shooter = Player.query.filter_by(initials=shooter).first()
                print(shooter)
                if shooter not in playerlist:
                    playerlist.append(shooter)
                shooter = shooter.id
                
            print("passer")    
            passer = (df.loc[i, "Passer"])
            if passer == passer:
                passer = Player.query.filter_by(initials=passer).first()
                print(passer)
                if passer not in playerlist:
                    playerlist.append(passer)
                passer = passer.id
                
                
            print("p1")
            p1 = (df.loc[i, "P1"])
            if p1 == p1:
                p1 = Player.query.filter_by(number=p1).first()
                print(p1)
                if p1 not in playerlist:
                    playerlist.append(p1)
                p1 = p1.id
                
            
            print("p2")  
            p2 = (df.loc[i, "P2"])
            if p2 == p2:
                p2 = Player.query.filter_by(number=p2).first()
                print(p2)
                if p2 not in playerlist:
                    playerlist.append(p2)
                p2 = p2.id
                
            
            print("p3")    
            p3 = (df.loc[i, "P3"])
            if p3 == p3:
                p3 = Player.query.filter_by(number=p3).first()
                print(p3)
                if p3 not in playerlist:
                    playerlist.append(p3)
                p3 = p3.id
                
            
            print("p4")    
            p4 = (df.loc[i, "P4"])
            if p4 == p4:
                p4 = Player.query.filter_by(number=p4).first()
                print(p4)
                if p4 not in playerlist:
                    playerlist.append(p4)
                p4 = p4.id
                
            
            print("p5")
            p5 = (df.loc[i, "P5"])
            if p5 == p5:
                p5 = Player.query.filter_by(number=p5).first()
                print(p5)
                if p5 not in playerlist:
                    playerlist.append(p5)
                p5 = p5.id
                
                
            poss = Possession(game_id=game.id,
                                possnum = int(df.loc[i,"Poss #"]),
                                tagstart = tagstart,
                                poss = df.loc[i,"Poss"],
                                start = df.loc[i,"Start"],
                                shottrigger = df.loc[i,"Shot Trigger"],
                                secondary = df.loc[i,"Secondary"],
                                usr = usr,
                                scr = scr,
                                psr = psr,
                                shot = df.loc[i,"Shot"],
                                result = df.loc[i,"Result"],
                                assist = df.loc[i,"Assist+"],
                                ftm = df.loc[i,"FTM"],
                                fta = df.loc[i,"FTA"],
                                open3 = df.loc[i,"Open 3"],
                                shooter = shooter,
                                passer = passer,
                                csjumper = df.loc[i,"C&S Jumper"],
                                esq = df.loc[i,"ESQ"],
                                shotclock = df.loc[i,"ShotClock"],
                                p1 = p1,
                                p2 = p2,
                                p3 = p3,
                                p4 = p4,
                                p5 = p5,
                                tag1 = df.loc[i,"1 Tag"],
                                tag2 = df.loc[i,"2 Tag"],
                                tag3 = df.loc[i,"3 Tag"],
                                tag4 = df.loc[i,"4 Tag"],
                                tag5 = df.loc[i,"5 Tag"],
                                offreb = df.loc[i,"OffReb"],
                                firsttrigger = int(df.loc[i,"First Trigger"]),
                                bolt = df.loc[i,"Bolt"],
                                painttouchtime = df.loc[i,"Paint Touch Time"],
                                posttouches = df.loc[i,"PostTouches"],
                                numpasses = int(df.loc[i,"NumPasses"]),
                                r2 = int(df.loc[i,"R2"]),
                                pm2 = int(df.loc[i,"PM2"]),
                                pt2 = int(df.loc[i,"PT2"]),
                                np2 = int(df.loc[i,"NP2"]),
                                pt3 = int(df.loc[i,"PT3"]),
                                np3 = int(df.loc[i,"NP3"]),
                                d3 = int(df.loc[i,"D3"]),
                                sb3 = int(df.loc[i,"SB3"]),
                                ft = int(df.loc[i,"FT"]),
                                points = int(df.loc[i,"POINTS"]))
                                
            db.session.add(poss)
            db.session.commit()   
        for i in range(len(playerlist)):
            game.players.append(playerlist[i]) 
            db.session.commit()
            db.session.add(playerlist[i])    
            db.session.commit()
        return render_template("home.html",user=current_user)
    # if request.method == 'POST':
    #     searchName = request.form.get('searchNameName')
    #     sub = request.form.get('subNameName')
    #     key = request.form.get('keyWordName')
    #     freq = request.form.get('frequency')
    #     search = Search(name=searchName,subreddits=sub,keywords=key,frequency=freq,user_id=current_user.id)
    #     db.session.add(search)
    #     db.session.commit()
        
        
    #     sub = sub.split(',')
    #     key = key.split(',')
    #     timelength = 604800 #a week ####time = how far the RMT will search
        
      
    #     #GET RMT RUN STATUS
    #     state = False
    #     info = db.session.query(Info).first() 
    #     db.session.refresh(info)
    #     if info.running == True:
    #         state = True       
    #     while(state == True ):
    #         time.sleep(1)
    #         db.session.refresh(info)
    #         print(info.running)
    #         if info.running == False:
    #             state = False
    #         print("WAITING ON SCHEDULER")
        
            
    #     info.running = True
    #     db.session.commit()
    #     print("VIEWS SWITCH TO TRUE")
    #     print("sched should be paused")
    #     #RUN RMT
    #     df=rmt.search(sub,key,timelength)
    #     print("views is done adding 5 seconds of view true")
    #     time.sleep(5)
    #     #RMT NO LONGER RUNNING
    #     info.running = False
    #     db.session.commit()
    #     print("SCHED SHOULD RUN NOW")
    #     time.sleep(3)
        
        
    #     ##########################################
    #     for i in range(len(df)):
    #        title =df.loc[i, "title"]
    #        selftext =df.loc[i, "selftext"]
    #        date =df.loc[i, "date"]
    #        realdate =df.loc[i, "realdate"]
    #        keyword =df.loc[i, "keyword"]
    #        subreddit =df.loc[i, "subreddit"]
    #        permalink =df.loc[i, "permalink"]
    #        newPost = Post(search_id=search.id,title=title,selftext=selftext,date=date,realdate=realdate,keyword=keyword,subreddit=subreddit,permalink=permalink)
    #        db.session.add(newPost)
    #        db.session.commit()
    #     ####################################################3
        
        
    #     session['search'] = search.id
    #     return redirect(url_for('views.searches', search=search))
        
    
    return render_template("home.html",user=current_user)

@views.route('/delete-search', methods=["POST"])
def delete_search():
    search = json.loads(request.data)
    searchId = search['searchId']
    search = Search.query.get(searchId)
    if search:
        print('found')
        if search.user_id == current_user.id:
            for post in search.posts:
                db.session.delete(post)
                db.session.commit()
            db.session.delete(search)
            
            db.session.commit()
    print('NOT')
    return jsonify({})






@views.route('/searches')
def searches(): 
    searchid = session['search']
    # session.pop('search', default=None)
    search = Search.query.get(searchid)
    return render_template("searches.html",search=search,user=current_user)

@views.route('/player')
def player(): 
    print("second")
    print(session.items())
    playerid = session['player']
    # session.pop('player', default=None)
    player = Player.query.get(playerid)

    fgm = []
    fga = []
    fgm3 = []
    fga3 = []
    efg = []
    ftm = []
    fta = []
    ftperc = []
    assist = []
    esq = []
    games = player.games
    print(games)
    for game in games:
        print(game.team)
        getcontext().prec = 3
        fgm_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id,Possession.result=="Make")).count())
        fgm3_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, Possession.result=="Make", (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
        fga_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id)).count())
        if fga_ != 0:
            
            efg_ = ((fgm_ + (Decimal(.5)*fgm3_)) / fga_)* (Decimal(100))
            efg.append(efg_)
        else:
            efg.append(None)
        fgm.append(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id,Possession.result=="Make")).count())
        fga.append(db.session.query(Possession).filter(game.id==Possession.game_id,Possession.shooter==player.id).count())
        fgm3.append(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, Possession.result=="Make", (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
        fga3.append(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
        ftm.append(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, (or_(Possession.ftm==1, Possession.ftm ==2)))).count())
        ftm_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, (or_(Possession.ftm==1, Possession.ftm ==2)))).count())
        fta.append(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, (or_(Possession.fta==1, Possession.fta ==2)))).count())
        fta_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, (or_(Possession.fta==1, Possession.fta ==2)))).count())
        esq_ = db.session.query(Possession.esq).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id,Possession.result=="Make")).all()
        sum = Decimal(0)
        for x in esq_:
            sum += x[0]
        esq_ = sum
        if fga_ != 0:
            
            esq_ = (esq_ / fga_)#* Decimal(100)
            esq.append(esq_)
        else:
            esq.append(None)
        if fta_ != 0:
            
            ftperc_ = (ftm_ / fta_) * (Decimal(100))
            ftperc.append(ftperc_)
        else:
            ftperc.append(None)
            
        assist.append(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id,Possession.assist==1)).count())
        
        
        print(fgm)
    print(fgm)
    
    
    return render_template("players copy.html",user=current_user, games = games , player=player, fgm = fgm , fga = fga, fgm3 = fgm3 , fga3 =fga3, efg=efg, ftm=ftm, fta=fta, ftperc = ftperc, assist = assist, esq = esq)
    return render_template("players copy.html", player = player,user=current_user)



@views.route('/delete-post', methods=["POST"])
def delete_post():
    postId = json.loads(request.data)
    postId = postId['postId']
    post = Post.query.get(postId)
    search=Search.query.get(post.search_id)
    if post:
        print('found')
        if search.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
    print('NOT')
    return jsonify({})


@views.route('/enter-search', methods=["POST"])
def enter_search():
        searchdata = json.loads(request.data)
        searchid = searchdata['searchId']
        session['search'] = searchid
        print(session['search'])
        search=Search.query.get(searchid)
        
        return redirect(url_for('views.searches', search=search))
    
@views.route('/enter-player', methods=["POST"])
def enter_player():
        playerdata = json.loads(request.data)
        playerid = playerdata['playerId']
        session['player'] = playerid
        print("first")
        print(session.items())
        player=Player.query.get(playerid)
        
        return redirect(url_for('views.player'))







    