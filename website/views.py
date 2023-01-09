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
    players = db.session.query(Player).all()
    games = db.session.query(Game).all()
    shot_name_list = []
    
    shot_name_list.append("R2")
    shot_name_list.append("PM2")
    shot_name_list.append("PT2")
    shot_name_list.append("NP2")
    shot_name_list.append("D3")
    shot_name_list.append("SB3")
    shot_name_list.append("NP3")
    shot_name_list.append("PT3")
    # 3 is added to the loop for the three types of shots whose queries do not follow same format
    
    shot_players = []
    shot_sums = []
    sq_points = []
    total_points = []
    sq_per = []
    tp_per = []
    for i in range(len(shot_name_list)+3):
        
        if i<8:
            shot = shot_name_list[i]
        shotlist = []
        shootersum = 0
        totalshooters = 0
        first_run = True
        for player in players:
            getcontext().prec = 6
            
            if i<8:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.shot==shot)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.shot==shot)).count())
                if first_run:
                    first_run = False
                    
                    #SQ POINTS TOTAL
                    sq = db.session.query(Possession.esq).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.shot==shot)).all()
                    totalsq = Decimal(0)
                    for x in sq:
                        totalsq += Decimal(x[0])
                    sq_points.append(totalsq)
                    
                    pts = db.session.query(Possession.points).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.shot==shot)).all()
                    totalpts = Decimal(0)
                    for x in pts:
                        totalpts += Decimal(x[0])
                    total_points.append(totalpts)
            
                
                    
            if i == 8:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.open3==1)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.open3==1)).count())
                if first_run:
                    first_run = False
                    
                    #SQ POINTS TOTAL
                    sq = db.session.query(Possession.esq).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.open3==1)).all()
                    totalsq = Decimal(0)
                    for x in sq:
                        totalsq += Decimal(x[0])
                    sq_points.append(totalsq)
                    
                    pts = db.session.query(Possession.points).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.open3==1)).all()
                    totalpts = Decimal(0)
                    for x in pts:
                        totalpts += Decimal(x[0])
                    total_points.append(totalpts)
            if i == 9:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.csjumper==1)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.csjumper==1)).count())
                if first_run:
                    first_run = False
                    
                    #SQ POINTS TOTAL
                    sq = db.session.query(Possession.esq).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.csjumper==1)).all()
                    totalsq = Decimal(0)
                    for x in sq:
                        totalsq += Decimal(x[0])
                    sq_points.append(totalsq)
                    
                    pts = db.session.query(Possession.points).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.csjumper==1)).all()
                    totalpts = Decimal(0)
                    for x in pts:
                        totalpts += Decimal(x[0])
                    total_points.append(totalpts)
            if i == 10:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.assist==1)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.assist==1)).count())
                if first_run:
                    first_run = False
                    
                    #SQ POINTS TOTAL
                    sq = db.session.query(Possession.esq).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.assist==1)).all()
                    totalsq = Decimal(0)
                    for x in sq:
                        totalsq += Decimal(x[0])
                    sq_points.append(totalsq)
                    
                    pts = db.session.query(Possession.points).filter(and_((or_(Possession.result=="Miss",Possession.result=="Make")),Possession.assist==1)).all()
                    totalpts = Decimal(0)
                    for x in pts:
                        totalpts += Decimal(x[0])
                    total_points.append(totalpts)
                    
                    
            if (make+miss)!=0:
                
                perc = make /(make+miss)*Decimal(100)
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
            shootersum_str = str(shootersum)+"%"
        else:
            shootersum_str = "-"
        
        shot_players.append(shotlist)
        shot_sums.append(shootersum_str)
        
        
        
        
        if shootersum != 0:
            
            getcontext().prec = 6
            print(i)
            print(totalsq)
            print(shootersum)
            sq_per_num = totalsq/shootersum
            getcontext().prec = 2
            sq_per_num_round = sq_per_num + Decimal(0)
            sq_per.append(str(sq_per_num_round)) #ADD OR REMOVE PERCENT?
            
            
            getcontext().prec = 6
            tp_per_num = totalpts/shootersum
            getcontext().prec = 2
            tp_per_num_round = tp_per_num + Decimal(0)
            tp_per.append(str(tp_per_num_round)) #ADD OR REMOVE PERCENT?
            
        else:
            sq_per.append('-')
            tp_per.append('-')
            
            
        
        
    print(shot_sums)
        
    return render_template("shot_types.html", user=current_user, players=players, stats = shot_players, sums = shot_sums, sq = sq_points , tp = total_points, sqper = sq_per,tpper = tp_per)

@views.route('/shot_types_single', methods=['GET','POST'])
@login_required
def shot_types_single():
    
    
    # 3 is added to the loop for the three types of shots whose queries do not follow same format
    
    #stat_list = ['0: poss','1: chances','2: fgm-fga','3: 3fgm','4: ftm-fta','5: assist','6: open 3','7: c&sjumper','8: poss length', '9: tag %','10: trigger time', '11: bolt time' , '12: paint time', '13: Poss with paint time', '14: Post ups', '15: total passes', '16: passes/poss','17: avg touches']
    
    
    playerid = session['player']
    
    player = Player.query.get(playerid)
    
    shot_name_list = []
    
    shot_name_list.append("R2")
    shot_name_list.append("PM2")
    shot_name_list.append("PT2")
    shot_name_list.append("NP2")
    shot_name_list.append("D3")
    shot_name_list.append("SB3")
    shot_name_list.append("NP3")
    shot_name_list.append("PT3")
    
    shot_players = []
    shot_sums = []
    for i in range(len(shot_name_list)+3):
        if i<8:
            shot = shot_name_list[i]
        shotlist = []
        shootersum = 0
        totalshooters = 0
        
        for game in player.games:
            getcontext().prec = 6
            
            if i<8:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.shot==shot,Possession.game_id==game.id)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.shot==shot,Possession.game_id==game.id)).count())
            if i == 8:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.open3==1,Possession.game_id==game.id)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.open3==1,Possession.game_id==game.id)).count())
            if i == 9:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.csjumper==1,Possession.game_id==game.id)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.csjumper==1,Possession.game_id==game.id)).count())
            if i == 10:
                make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.assist==1,Possession.game_id==game.id)).count())
                miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.assist==1,Possession.game_id==game.id)).count())
            if (make+miss)!=0:
                
                perc = make /(make+miss)*Decimal(100)
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
        
        shot_players.append(shotlist)
        
        if shootersum == 0:
            shootersum = '-'
        shot_sums.append(shootersum)
        
        
        
    return render_template("shot_types_single.html", user=current_user, player=player, games = player.games, stats = shot_players, sums = shot_sums)


@views.route('/games', methods=['GET','POST'])
@login_required
def games():
    
    games = db.session.query(Game).all()
    
    all_game_stats = []
    for i in range(len(games)):
        
        game_stats = []
        
        poss = Decimal(db.session.query(Possession).filter(and_(Possession.poss==1,Possession.game_id==games[i].id)).count())
        
        if poss != 0:
            game_stats.append(poss)
        else:
            game_stats.append('-')
        
        
        
        
        
        
        
        poss_zero = Decimal(db.session.query(Possession).filter(and_(Possession.poss==1,Possession.game_id==games[i].id)).count())
        
        if poss_zero+poss != 0:
            game_stats.append(poss_zero+poss)
        else:
            game_stats.append('-')
            
            
            
            
            
            
            
            
        fgm_make = db.session.query(Possession).filter(and_(Possession.result == "Make",Possession.game_id==games[i].id)).count()
        
        fgm_miss = db.session.query(Possession).filter(and_(Possession.result == "Miss",Possession.game_id==games[i].id)).count()
        
        if fgm_make !=0 and fgm_miss != 0:
            game_stats.append(str(fgm_make) + '/' + str(fgm_miss))
        else:
            game_stats.append('-')
            
                    
                 
                 
                 
                    
        
        
        
        fgm3_make = db.session.query(Possession).filter(and_(Possession.result == "Make",Possession.game_id==games[i].id,(or_(Possession.shot=='NP3',Possession.shot=='PT3',Possession.shot=='SB3',Possession.shot=='3')))).count()
        
        fgm3_miss = db.session.query(Possession).filter(and_(Possession.result == "Miss",Possession.game_id==games[i].id,(or_(Possession.shot=='NP3',Possession.shot=='PT3',Possession.shot=='SB3',Possession.shot=='3')))).count()    
        
        if fgm3_make !=0 and fgm3_miss != 0:
            game_stats.append(str(fgm3_make) + '/' + str(fgm3_miss))
        else:
            game_stats.append('-')
        
        
        
        
        
        
        
        
        ftm_sum = 0
        ftm = db.session.query(Possession.ftm).filter(and_(Possession.ftm != None,Possession.game_id==games[i].id)).all()
        fta_sum = 0
        fta = db.session.query(Possession.fta).filter(and_(Possession.fta != None,Possession.game_id==games[i].id)).all()
        
        for j in range(len(fta)):
            ftm_sum += ftm[j][0]
            fta_sum += fta[j][0]
            
        if ftm_sum !=0 and fta_sum != 0:
            game_stats.append(str(ftm_sum) + '/' + str(fta_sum))
        else:
            game_stats.append('-')
            
            
        
        
        
        
        
        assist = db.session.query(Possession).filter(and_(Possession.assist==1,Possession.game_id==games[i].id)).count()
        
        if assist != 0:
            game_stats.append(assist)
        else:
            game_stats.append('-')
        
        
        
        
        
        
        
        
        open3 = db.session.query(Possession).filter(and_(Possession.open3==1,Possession.game_id==games[i].id)).count()
        
        if open3 != 0:
            game_stats.append(open3)
        else:
            game_stats.append('-')
        
        
        
        
        
        
        csjumper = db.session.query(Possession).filter(and_(Possession.csjumper==1,Possession.game_id==games[i].id)).count()
        
        if csjumper != 0:
            game_stats.append(csjumper)
        else:
            game_stats.append('-')
            
        
        
        
        
        
        
        
        
        
        #note WHAT ARE THE NONE VALUES IN SHOTCLOCK ABOUT
        
        poss1_sum = Decimal(0)
        shot_poss1 = db.session.query(Possession.shotclock).filter(and_(Possession.poss==1,Possession.game_id==games[i].id)).all()
        poss0_sum = Decimal(0)
        shot_poss0 = db.session.query(Possession.shotclock).filter(and_(Possession.poss==0,Possession.game_id==games[i].id)).all()
        
        
        for j in range(len(shot_poss1)):
            if shot_poss1[j][0] != None:
                poss1_sum += Decimal(30) - Decimal(shot_poss1[j][0])
            
        for j in range(len(shot_poss0)):
            if shot_poss0[j][0] != None:
                poss0_sum += Decimal(20) - Decimal(shot_poss0[j][0])
            
        getcontext().prec = 6
        #the DIVISOR MAY CONTAIN NONES note
        posslength = (poss1_sum + poss0_sum) / (Decimal(len(shot_poss1)) + Decimal(len(shot_poss0)))
        
        getcontext().prec = 4
        posslength = posslength + Decimal(0)
        
        if posslength != 0:
            game_stats.append(posslength)
        else:
            game_stats.append('-')
            
        
        
        #ASK LOGAN ABOUT THIS note
        tagperc = 0
        
        if tagperc != 0:
            game_stats.append(tagperc)
        else:
            game_stats.append('-')
        
            
        
        #AVERAGE OF (30 - First Trigger (Column AH) for possession = 1);  Do not count Possession = 0 rows
        
        poss1_sum = Decimal(0)
        triggers = db.session.query(Possession.firsttrigger).filter(and_(Possession.poss==1,Possession.game_id==games[i].id)).all()
        
        
        
        for j in range(len(triggers)):
            if triggers[j][0] != None:
                poss1_sum += Decimal(30) - Decimal(triggers[j][0])
            
        
            
        getcontext().prec = 6
        triggertime = (poss1_sum) / Decimal(len(triggers))
        
        getcontext().prec = 4
        triggertime = triggertime + Decimal(0)
        
        if triggertime != 0:
            game_stats.append(triggertime)
        else:
            game_stats.append('-')
            
        
        
        
        
        
        
        
        
        
        #same but with bolt
        
        poss1_sum = Decimal(0)
        bolt = db.session.query(Possession.bolt).filter(and_(Possession.poss==1,Possession.game_id==games[i].id,)).all()
        
        
        
        for j in range(len(bolt)):
            if bolt[j][0] != None:
                poss1_sum += Decimal(30) - Decimal(bolt[j][0])
            
        
            
        getcontext().prec = 6
        bolttime = (poss1_sum) / Decimal(len(bolt))
        
        getcontext().prec = 4
        bolttime = bolttime + Decimal(0)
        
        if bolttime != 0:
            game_stats.append(bolttime)
        else:
            game_stats.append('-')
            
            
            
            
            
            
            
        
        
        #same but for painttouchtime
        
        poss1_sum = Decimal(0)
        painttouch = db.session.query(Possession.painttouchtime).filter(and_(Possession.poss==1,Possession.painttouchtime != None, Possession.game_id==games[i].id)).all()
        
        
        
        for j in range(len(painttouch)):
            if painttouch[j][0] != None:
                poss1_sum += Decimal(30) - Decimal(painttouch[j][0])
            
        
            
        getcontext().prec = 6
        painttouchtime = (poss1_sum) / Decimal(len(painttouch))
        
        getcontext().prec = 4
        painttouchtime = painttouchtime + Decimal(0)
        
        if painttouchtime != 0:
            game_stats.append(painttouchtime)
        else:
            game_stats.append('-')
            
            
        
        
        
        
        
        
        poss_with_paint = db.session.query(Possession.painttouchtime).filter(and_(Possession.painttouchtime != None, Possession.game_id==games[i].id)).count()
        
        
        
        if poss_with_paint != 0:
            game_stats.append(poss_with_paint)
        else:
            game_stats.append('-')
            
            
                
            
            
        posttouches = Decimal(0)
        posttouch = db.session.query(Possession.posttouches).filter(and_(Possession.posttouches != None, Possession.game_id==games[i].id)).all()
        
        
        
        for j in range(len(posttouch)):
            if posttouch[j][0] != None:
                posttouches += Decimal(posttouch[j][0])
            
        
            
        
        if posttouches != 0:
            game_stats.append(posttouches)
        else:
            game_stats.append('-')
            
           
           
        
        
        
        
        
        
        
        passes_sum = Decimal(0)
        passes = db.session.query(Possession.numpasses).filter(and_(Possession.posttouches != None, Possession.game_id==games[i].id)).all()
        
        
        
        for j in range(len(passes)):
            if passes[j][0] != None:
                passes_sum += Decimal(passes[j][0])
            
        
            
        
        if passes_sum != 0:
            game_stats.append(passes_sum)
        else:
            game_stats.append('-')
            
        
        
        
        
        getcontext().prec = 6
        
        pass_poss = passes_sum/poss
        
        getcontext().prec = 2
        
        pass_poss = pass_poss + Decimal(0)
        
        if pass_poss != 0:
            game_stats.append(str(pass_poss)+'%')
        else:
            game_stats.append('-')
        
         
            
        #ASK LOGAN ABOUT THIS note
        #can we add a total touches column to the excel because we would need to hardcode player names into data base.
        #if you do want me to store specifically who touches, we may need to agree on a permanent format for where player touches will be in 
        #the spreadsheet // perhaps per position or player number.
        #perhaps add another
        avgtouches = 0
        
        if avgtouches != 0:
            game_stats.append(tagperc)
        else:
            game_stats.append('-')    
            
            
            
        
            
        all_game_stats.append(game_stats)
        
        
        
        
        
        #print(all_game_stats)
    return render_template("games.html", user=current_user, stats = all_game_stats, games=games)


@views.route('/triggers', methods=['GET','POST'])
@login_required
def triggers():
    
    
    shottriggers = ['1','1 Above','122','2','3','BLOB Special','BLOB1','BLOB2','BLOB3','Chin','DHO','Hands','Just Playing','Loop','Low','Point','Porch','Putback','Thumbs Up','Transition']
    data = []
    
    for trigger in shottriggers:
        trigger_data = []
        trigger_data.append(trigger)
        
        
        
        
        
        
        
        
        
        
        getcontext().prec = 6
        sq_sum = Decimal(0)
        sqpoints = db.session.query(Possession.esq).filter(and_(Possession.shottrigger==trigger, Possession.esq != None)).all()
        
        
        for j in range(len(sqpoints)):
            sq_sum += sqpoints[j][0]
        
        sq_sum_6prec = sq_sum
        getcontext().prec = 4
        sq_sum = sq_sum + Decimal(0)
        
        if sq_sum != 0:
            trigger_data.append(sq_sum)
        else:
            trigger_data.append('-')
            
        
        
        
        
        
        
        
        
        
        
        getcontext().prec = 4
        pt_sum = Decimal(0)
        points = db.session.query(Possession.points).filter(and_(Possession.shottrigger==trigger, Possession.points != None)).all()
        
        
        for j in range(len(points)):
            pt_sum += points[j][0]
        
        
        if pt_sum != 0:
            trigger_data.append(pt_sum)
        else:
            trigger_data.append('-')
            
        
        
        
        getcontext().prec = 6
        
        instances = Decimal(db.session.query(Possession).filter(Possession.shottrigger == trigger).count())
        
        
        
        
        if instances != 0 :
            sq_ratio = sq_sum_6prec / instances
        
        
        getcontext().prec = 4
        sq_ratio = sq_ratio + Decimal(0)
        
        if sq_ratio != 0:
            trigger_data.append(sq_ratio)
        else:
            trigger_data.append('-')
        
        
        
        
        
        
        
        
        
        getcontext().prec = 6
        
        if instances != 0 :
            pt_ratio = pt_sum / instances
        
        getcontext().prec = 4
        pt_ratio = pt_ratio + Decimal(0)
        
        if pt_ratio != 0:
            trigger_data.append(pt_ratio)
        else:
            trigger_data.append('-')
            
        
        
        

        if instances != 0:
            trigger_data.append(instances)
        else:
            trigger_data.append('-')
        
        
        data.append(trigger_data)
        
        
        
        
        
        
    
    
    return render_template("triggers.html",user=current_user,data=data)
    
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
  
    for game in player.games:
       
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
        
        
        
    
    
    return render_template("basic_player_single.html",user=current_user, games = player.games , player=player, fgm = fgm , fga = fga, fgm3 = fgm3 , fga3 =fga3, efg=efg, ftm=ftm, fta=fta, ftperc = ftperc, assist = assist, esq = esq,
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




@views.route('/enter_shot_types_single', methods=["POST"])
def enter_shot_types_single():
    print("hello")
    data = json.loads(request.data)
    playerid = data['playerId']
    print(playerid)
    session['player'] = playerid
    
    return redirect(url_for('views.shot_types_single'))
    






    