from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for,session
from flask_login import login_required, current_user
views = Blueprint('views',__name__)
from .models import Note, Search, Post, Info, Game, Possession
from . import db, rmt ,excel_processor
import json
import pandas as pd
import time
import os
from os.path import join, dirname, realpath
import openpyxl
from pathlib import Path




@views.route('/', methods=['GET','POST'])
@login_required
def home():
    
    if request.method == 'POST':
        sheet = request.files['data']
    
        df = excel_processor.process(sheet)
        print(df)
        for i in range(len(df)):
            if i ==0:
                game = Game(team = df.loc[i,"Opp"] , date = df.loc[i,"Date"])
                poss = Possession(game_id=game.id,
                                    # players,
                                    posessed = df.loc[i,"Poss"],
                                    start = df.loc[i,"Start"],
                                    strigger = df.loc[i,"Shot Trigger"],
                                    secondary = df.loc[i,"Secondary"],
                                    shotlocation = df.loc[i,"Shot"],
                                    result = df.loc[i,"Result"],
                                    assist = df.loc[i,"Assist+"],
                                    ftmade = df.loc[i,"FTM"],
                                    ftattempts = df.loc[i,"FTA"],
                                    open3 = df.loc[i,"Open 3"],
                                    catch_shoot = df.loc[i,"C&S Jumper"],
                                    shotclock = df.loc[i,"Result"],
                                    tag1 = df.loc[i,"Result"],
                                    tag2 = df.loc[i,"Result"],
                                    tag3 = df.loc[i,"Result"],
                                    tag4 = df.loc[i,"Result"],
                                    tag5 = df.loc[i,"Result"],
                                    offreb = df.loc[i,"Result"],
                                    firsttrigger = df.loc[i,"Result"],
                                    bolt = df.loc[i,"Result"],
                                    painttouchtime = df.loc[i,"Result"],
                                    posttouches = df.loc[i,"Result"],
                                    numpasses = df.loc[i,"Result"])
            elif df.loc[i,"Opp"] == game.name:
                poss = poss with game.id
            else:
                game = game
                poss = poss with game.id
                
      
            
        
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
    session.pop('messages', default=None)
    search = Search.query.get(searchid)
    return render_template("searches.html",search=search,user=current_user)


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
        search=Search.query.get(searchid)
        
        return redirect(url_for('views.searches', search=search))







    