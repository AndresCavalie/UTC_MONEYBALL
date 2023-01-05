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


@views.route('/basic_player', methods=['GET','POST'])
@login_required
def basic_player():
    # players = db.session.query(Player).join(Search).filter(Search.user_id == User.id).all()
    players = db.session.query(Player).all()
    
    fgms=0
    fgas=0
    fgm3s=0
    fga3s=0
    efgs=0
    ftms=0
    ftas=0
    ftpercs=0
    assists=0
    esqs=0
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
                efgs += efg_
            else:
                efg.append(0)
            fgm.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make")).count())
            fgms += db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make")).count()
            fga.append(db.session.query(Possession).filter(Possession.shooter==player.id).count())
            fgas += db.session.query(Possession).filter(Possession.shooter==player.id).count()
            fgm3.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, Possession.result=="Make", (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
            fgm3s += db.session.query(Possession).filter(and_(Possession.shooter==player.id, Possession.result=="Make", (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count()
            fga3.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
            fga3s += db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count()
            ftm.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.ftm==1, Possession.ftm ==2)))).count())
            ftm_ = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.ftm==1, Possession.ftm ==2)))).count())
            ftms += ftm_
            fta.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.fta==1, Possession.fta ==2)))).count())
            
            fta_ = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id, (or_(Possession.fta==1, Possession.fta ==2)))).count())
            ftas += fta_
            esq_ = db.session.query(Possession.esq).filter(and_(Possession.shooter==player.id,Possession.result=="Make")).all()
            getcontext().prec = 5
            sum = Decimal(0)
            for x in esq_:
                sum = sum + Decimal(x[0])
                
                if player.name == "Demetrius Davis":
                    
                    print(Decimal(x[0]))
            if player.name == "Demetrius Davis":
                
                print(sum)
            esq_ = sum
            
            getcontext().prec = 3
            if fga_ != 0:
                
                esq_ = (esq_ / fga_)#* Decimal(100)
                esq.append(esq_)
                esqs += esq_
                
            else:
                esq.append(0)
            if fta_ != 0:
                
                ftperc_ = (ftm_ / fta_) * (Decimal(100))
                ftperc.append(ftperc_)
                ftpercs += ftperc_
            else:
                ftperc.append(0)
                
            assist.append(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.assist==1)).count())
            assists += db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.assist==1)).count()
            
    
    
    efgs = efgs / Decimal(len(players))
    ftpercs = ftpercs / Decimal(len(players))
    # getcontext().prec = 6
    print("ESQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
    print(esqs)
    esqs = esqs / Decimal(len(players))
    
    sum = {'fgm': fgms,
           'fga': fgas,
           'fgm3': fgm3s,
           'fga3': fga3s,
           'efg': efgs,
           'ftm': ftms,
           'fta': ftas,
           'ftperc': ftpercs,
           'assist': assists,
           'esq': esqs
           }      
    
    return render_template("basic_player.html",user=current_user,players=players, fgm = fgm , fga = fga, fgm3 = fgm3 , fga3 =fga3, efg=efg, ftm=ftm, fta=fta, ftperc = ftperc, assist = assist, esq = esq , sum=sum)

@views.route('/shot_types', methods=['GET','POST'])
@login_required
def shot_types():
    # players = db.session.query(Player).join(Search).filter(Search.user_id == User.id).all()
    players = db.session.query(Player).all()
    
    s_shotlist = 0
    s_shotlist_shooters = 0
    
    s_postmove2 = 0
    s_postmove2_shooters_shooters = 0
    
    s_paint2 = 0
    s_paint2_shooters = 0
    
    s_nonpaint2 = 0
    s_nonpaint2_shooters = 0
    
    s_dribble3 = 0
    s_dribble3_shooters = 0
    
    s_stopbehind3 = 0
    s_stopbehind3_shooters = 0
    
    s_nonpaint3 = 0
    s_nonpaint3_shooters = 0
    
    s_painttouch3 = 0
    s_painttouch3_shooters = 0
    
    s_open3 = 0
    s_open3_shooters = 0
    
    s_csjumper = 0
    s_csjumper_shooters = 0
    
    s_assisted = 0
    s_assisted_shooters = 0
    
    shotlist = []
    postmove2 = []
    paint2 = []
    nonpaint2 = []
    dribble3 = []
    stopbehind3 = []
    nonpaint3 = []
    painttouch3 = []
    open3 = []
    csjumper = []
    assisted = []
    
    shot_type_list = []
    shot_name_list = []
    
    shot_type_list.append(shotlist)
    shot_name_list.append("R2")
    shot_type_list.append(postmove2)
    shot_name_list.append("PM2")
    shot_type_list.append(paint2)
    shot_name_list.append("PT2")
    shot_type_list.append(nonpaint2)
    shot_name_list.append("NP2")
    shot_type_list.append(dribble3)
    shot_name_list.append("D3")
    shot_type_list.append(stopbehind3)
    shot_name_list.append("SB3")
    shot_type_list.append(nonpaint3)
    shot_name_list.append("NP3")
    shot_type_list.append(painttouch3)
    shot_name_list.append("PT3")
    
    data = []
    for i in range(len(shot_type_list)):
        shot = shot_name_list[i]
        shotlist = []
        shootersum = 0
        totalshooters = 0
        for player in players:
            getcontext().prec = 6
            make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.shot==shot)).count())
            miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.shot==shot)).count())
            if (make+miss)!=0:
                
                perc = make/(make+miss)*Decimal(100)
                getcontext().prec = 4
                perc_round = perc+Decimal(0)
                shotlist.append(str(perc_round)+"%")
                shootersum += perc
                totalshooters += 1
            else:
                shotlist.append("-")
                

        getcontext().prec = 4
        if totalshooters != 0:
            shootersum = Decimal(shootersum)/Decimal(totalshooters)
            shootersum = str(shootersum)+"%"
        datainner = []
        datainner.append(shotlist)
        datainner.append(shootersum)
        
        data.append(datainner)  
        
        
    
    
    
    
    return render_template("shot_types.html",
                           user=current_user,
                           players=players,
                           data=data)

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
                
            
          
            p4 = (df.loc[i, "P4"])
            if p4 == p4:
                p4 = Player.query.filter_by(number=p4).first()
              
                if p4 not in playerlist:
                    playerlist.append(p4)
                p4 = p4.id
                
            
           
            p5 = (df.loc[i, "P5"])
            if p5 == p5:
                p5 = Player.query.filter_by(number=p5).first()
                
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
  
        if search.user_id == current_user.id:
            for post in search.posts:
                db.session.delete(post)
                db.session.commit()
            db.session.delete(search)
            
            db.session.commit()
 
    return jsonify({})

@views.route('/searches')
def searches(): 
    searchid = session['search']
    # session.pop('search', default=None)
    search = Search.query.get(searchid)
    return render_template("searches.html",search=search,user=current_user)

@views.route('/basic_player_single')
def basic_player_single(): 
   
    playerid = session['player']
    fgm_s = session['fgm']
    fga_s = session['fga']
    fgm3_s = session['fgm3']
    fga3_s = session['fga3']
    efg_s = session['efg']
    ftm_s = session['ftm']
    fta_s = session['fta']
    ftperc_s = session['ftperc']
    assist_s = session['assist']
    esq_s = session['esq']

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
  
    for game in games:
       
        getcontext().prec = 3
        fgm_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id,Possession.result=="Make")).count())
        fgm3_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id, Possession.result=="Make", (or_(Possession.shot=="SB3", Possession.shot=="D3", Possession.shot =="PT3", Possession.shot == "NP3")))).count())
        fga_ = Decimal(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id)).count())
        if fga_ != 0:
            
            efg_ = ((fgm_ + (Decimal(.5)*fgm3_)) / fga_)* (Decimal(100))
            efg.append(efg_)
        else:
            efg.append(0)
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
            sum += Decimal(x[0])
           
            if player.name == "Demetrius Davis":
                    
                    print(Decimal(x[0]))
        if player.name == "Demetrius Davis":
            
            print(sum)
            
        esq_ = sum
        
        
        
        
        
        
        if fga_ != 0:
            
            esq_ = (esq_ / fga_)#* Decimal(100)
            
            esq.append(esq_)
        else:
            esq.append(0)
            
            
            
        if fta_ != 0:
            
            ftperc_ = (ftm_ / fta_) * (Decimal(100))
            ftperc.append(ftperc_)
        else:
            ftperc.append(0)
            
        assist.append(db.session.query(Possession).filter(and_(game.id==Possession.game_id,Possession.shooter==player.id,Possession.assist==1)).count())
        
        
        
    
    
    return render_template("basic_player_single.html",user=current_user, games = games , player=player, fgm = fgm , fga = fga, fgm3 = fgm3 , fga3 =fga3, efg=efg, ftm=ftm, fta=fta, ftperc = ftperc, assist = assist, esq = esq,
                           fgm_s = fgm_s , fga_s = fga_s, fgm3_s = fgm3_s , fga3_s =fga3_s, efg_s=efg_s, ftm_s=ftm_s, fta_s=fta_s, ftperc_s = ftperc_s, assist_s = assist_s, esq_s = esq_s
                           )

@views.route('/delete-post', methods=["POST"])
def delete_post():
    postId = json.loads(request.data)
    postId = postId['postId']
    post = Post.query.get(postId)
    search=Search.query.get(post.search_id)
    if post:
   
        if search.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
    
    return jsonify({})

@views.route('/enter-search', methods=["POST"])
def enter_search():
        searchdata = json.loads(request.data)
        searchid = searchdata['searchId']
        session['search'] = searchid
       
        search=Search.query.get(searchid)
        
        return redirect(url_for('views.searches', search=search))
    
@views.route('/enter_basic_player_single', methods=["POST"])
def enter_basic_player_single():
        playerdata = json.loads(request.data)
        playerid = playerdata['playerId']
        
        
        fgm = playerdata['fgm']
        print(fgm)
        fga = playerdata['fga']
        fgm3 = playerdata['fgm3']
        fga3 = playerdata['fga3']
        efg = playerdata['efg']
        ftm = playerdata['ftm']
        fta = playerdata['fta']
        ftperc = playerdata['ftperc']
        assist = playerdata['assist']
        esq = playerdata['esq']
        session['fgm'] = fgm
        session['fga'] = fga
        session['fgm3'] = fgm3
        session['fga3'] = fga3
        session['efg'] = efg
        session['ftm'] = ftm
        session['fta'] = fta
        session['ftperc'] = ftperc
        session['assist'] = assist
        session['esq'] = esq
        
        
        session['player'] = playerid
        print("first")
        print(session.items())
        player=Player.query.get(playerid)
        
        return redirect(url_for('views.basic_player_single'))







    