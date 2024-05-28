
from datetime import datetime
from email.mime import image
from io import BytesIO

import string
from this import s
from PIL import Image
import io
import MySQLdb
from enum import unique
import mimetypes
import base64
from re import T
from sqlite3 import Cursor
from flask import Flask,render_template,request,session,redirect,url_for,flash, send_file 
import os                                    
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc , asc
from flask_login import UserMixin,login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import datetime

#my database connection
local_server=True 
app = Flask(__name__)
app.secret_key='cricket'


#this is for unique user
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/circket'
db=SQLAlchemy(app)


def convert_data(file_name):
    with open(file_name, 'rb') as file:
        binary_data = file.read()
    return binary_data
#................................................................coach model.......................................................................
#create a db tables
class Coach(db.Model):
    coach_id=db.Column(db.Integer,primary_key=True)                                        
    c_name=db.Column(db.String(100))                                       
    team_name=db.Column(db.String(100))
    role=db.Column(db.String(100))
    img =db.Column(db.String(10000))
    # img=db.Column(db.LargeBinary)

    def __init__(self, coach_id,c_name,team_name,role,img):
        self.coach_id = coach_id
        self.c_name = c_name
        self.team_name = team_name
        self.role=role
        self.img = img
       
         
    def __repr__(self):
        return f"{self.c_name}:{self.coach_id}:{self.team_name}:{self.role}{self.img}"

#display all
@app.route('/data')
def RetrieveDataList():
    
    coach2 = Coach.query.all()
    # data = Cursor.execute("SELECT img FROM Coach WHERE coach_id=22")
    # img = data[0][0]
    
    session['coach'] = True
    return render_template('datalist.html',coach2 = coach2)

#insert new entry
@app.route('/data/insert' , methods = ['GET','POST'])
def create():
    teamnames = db.engine.execute("SELECT team_name FROM team")
    if request.method == 'GET':
        return render_template('insert.html',teamnames=teamnames)
 
    if request.method == 'POST':
        coach_id = request.form['coach_id']
        c_name = request.form['c_name']
        team_name = request.form['team_name']
        role = request.form['role']
        img = request.form['img']
        coach1 = Coach(coach_id=coach_id, c_name=c_name, team_name=team_name,role=role,img=img)
        db.session.add(coach1)
        db.session.commit()
        return redirect('/data')

#display single entry for user
@app.route('/data/<int:id>')
def RetrieveSingleCoach(id):
    coach1 = Coach.query.filter_by(coach_id=id).first()
    if coach1:
        return render_template('data.html', coach1 = coach1)
    return f"coach with id ={id} Doenst exist"

#update 
@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    coach1 = Coach.query.filter_by(coach_id=id).first()
    teamnames = db.engine.execute("SELECT team_name FROM team")
    if request.method == 'POST':
        if coach1:
            db.session.delete(coach1)
            db.session.commit()
 
            name = request.form['c_name']
            team_name = request.form['team_name']
            role =request.form['role']
            img = request.form['img']
            # filename = secure_filename(img.filename)
            # mimetype = img.mimetype
            
            coach1 = Coach(coach_id=id, c_name=name, team_name=team_name,role=role,img=img)
 
            db.session.add(coach1)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"coach with id = {id} Does not exist"
 
    return render_template('update.html', coach1 = coach1, teamnames = teamnames)

#delete
@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    coach1 = Coach.query.filter_by(coach_id=id).first()
    if request.method == 'POST':
        if coach1:
            db.session.delete(coach1)
            db.session.commit()
            return redirect('/data')
    
    return render_template('delete.html')

#...............................................................end of coach ...................................................................


#.................................................................admin page.....................................................................

class Admin(db.Model): 
    id=db.Column(db.Integer,primary_key=True) 
    admin_name=db.Column(db.String(100))                                       
    email=db.Column(db.String(100))                                       
    password=db.Column(db.String(1000))

def __init__(self,id,admin_name,email,password):
        self.id = id
        self.admin_name = admin_name
        self.email = email
        self.password = password
                 

@app.route("/admin")
def admin():
    session['coach'] = False
    session['captain'] = False
    session['match'] = False
    session['team'] = False
    session['player'] = False
    return render_template('admin.html')

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        a = request.form['admin_name']
        p = request.form['password']
        data = Admin.query.filter_by(admin_name=a, password=p).first()
        if data is not None:
            session['logged_in'] = True
            print("login")
            flash('login successful')
            return redirect(url_for('admin'))
        else:
            print("invalid")
            flash('invalid user')
            return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    print("logout sucessful")
    return redirect(url_for('index'))

def __init__(self, admin_name, password):
        self.admin_name = admin_name
        self.password = password

#......................................................................admin page end................................................................
@app.route("/user")
def user():
    match2 = Matches.query.order_by(asc(Matches.match_date_time)).all()
    team1 = Team.query.all()
    flagimg = db.engine.execute('SELECT team_name,team_img FROM team')
    current_time=datetime.datetime.now()
    print(current_time)
    print(match2[0].match_date_time)
    return render_template('schedule.html',flagimg=flagimg,match2=match2,current_time=current_time,team1=team1)

#--------------------------------------------------------------------caption module------------------------------------------------------------
class Captian(db.Model): 
    team_id=db.Column(db.Integer,unique=True) 
    player_id=db.Column(db.String(100),unique=True) 
    team_name=db.Column(db.String(100))                                       
    captian_name=db.Column(db.String(1000))
    _table_args_ = (
        db.PrimaryKeyConstraint(
            team_id,player_id,
        )
    )

    def __init__(self, team_id,player_id,team_name,captian_name):
        self.team_id = team_id
        self.player_id = player_id
        self.team_name = team_name
        self.captian_name = captian_name
        
         
    def __repr__(self):
        return f"{self.team_id}:{self.player_id}:{self.team_name}:{self.captian_name}"

#display all
@app.route('/datacaptain')
def RetrieveDataListofcaptian():
    captian2 = Captian.query.all()
    session['captain'] = True
    return render_template('datalist.html',captian2 = captian2)

# insert new entry
@app.route('/datacaptain/insert' , methods = ['GET','POST'])
def createcaptian():
    teamnames = db.engine.execute("SELECT team_id,team_name FROM team") 
    if request.method == 'GET':
        return render_template('insert.html',teamnames=teamnames)
 
    if request.method == 'POST':
        team_id = request.form['team_id']
        player_id = request.form['player_id']
        team_name = request.form['team_name']
        captian_name = request.form['captian_name']
        captian1 = Captian(team_id=team_id,player_id=player_id, team_name=team_name,captian_name=captian_name)
        db.session.add(captian1)
        db.session.commit()
        return redirect('/datacaptain')

#display single entry for user
@app.route('/datacaptain/<int:id>')
def RetrieveSingleCaptain(id):
    captain1 = Captian.query.filter_by(team_id=id).first()
    if captain1:
        return render_template('data.html', captain1 = captain1)
    return f"coach with id ={id} Doenst exist"

# update 
@app.route('/datacaptain/<int:id>/update',methods = ['GET','POST'])
def updatecaptian(id):
    teamnames = db.engine.execute("SELECT team_name FROM team")
    captian1 = Captian.query.filter_by(team_id=id).first()
    if request.method == 'POST':
        if captian1:
            db.session.delete(captian1)
            db.session.commit()
 
            captian_name = request.form['captian_name']
            team_name =request.form['team_name']
            player_id = request.form['player_id']
            captian1 = Captian(team_id=id,captian_name=captian_name, player_id=player_id,team_name=team_name)
 
            db.session.add(captian1)
            db.session.commit()
            return redirect(f'/datacaptain/{id}')
        return f"captian with id = {id} Does not exist"
 
    return render_template('update.html', captian1 = captian1,teamnames=teamnames)

#delete
@app.route('/datacaptain/<int:id>/delete', methods=['GET','POST'])
def deletecaptian(id):
    captian1 = Captian.query.filter_by(team_id=id).first()
    if request.method == 'POST':
        if captian1:
            db.session.delete(captian1)
            db.session.commit()
            return redirect('/datacaptain')
    
    return render_template('delete.html')

#--------------------------------------------------------end of caption----------------------------------------------------------------------

class Matches(db.Model): 
    match_id=db.Column(db.String(100),primary_key=True)                                       
    t1_name=db.Column(db.String(100))                                       
    t2_name=db.Column(db.String(100))                                       
    stadium=db.Column(db.String(1000))
    match_date_time=db.Column(db.DateTime)
    winner=db.Column(db.String(1000))
    losser=db.Column(db.String(1000))

    def __init__(self, match_id,t1_name,t2_name,stadium,match_date_time,winner,losser):
        self.match_id = match_id
        self.t1_name = t1_name
        self.t2_name = t2_name
        self.stadium = stadium
        self.match_date_time = match_date_time
        self.winner = winner
        self.losser = losser
        
         
    def __repr__(self):
        return f"{self.match_id}:{self.t1_name}:{self.t2_name}:{self.stadium}:{self.match_date_time}:{self.winner}:{self.losser}"

#display all
@app.route('/datamatch')
def RetrieveDataListofmatch():
    session['match'] = True
    match2 = Matches.query.all()
    return render_template('datalist.html',match2 = match2)

# insert new entry
@app.route('/datamatch/insert' , methods = ['GET','POST'])
def creatematch():
    teams = db.engine.execute("SELECT team_name FROM team")
    teamnames = db.engine.execute("SELECT team_name FROM team")
    if request.method == 'GET':
        return render_template('insert.html',teamnames=teamnames,teams=teams)
 
    if request.method == 'POST':
        match_id = request.form['match_id']
        t1_name = request.form['t1_name']
        t2_name = request.form['t2_name']
        stadium = request.form['stadium']
        match_date_time = request.form['match_date_time']
        winner = request.form['winner']
        losser = request.form['losser']
        match1 = Matches(match_id=match_id,t1_name=t1_name, t2_name=t2_name,stadium=stadium,match_date_time=match_date_time,winner=winner,losser=losser)
        db.session.add(match1)
        db.session.commit() 
        return redirect('/datamatch')

#display single entry for user
@app.route('/datamatch/<string:id>')
def RetrieveSinglematch(id):
    match1 = Matches.query.filter_by(match_id=id).first()
    if match1:
        return render_template('data.html', match1 = match1)
    return f"match with id ={id} Doenst exist"

# update 
@app.route('/datamatch/<string:id>/update',methods = ['GET','POST'])
def updatematch(id):
    teams = db.engine.execute("SELECT team_name FROM team")
    teamnames = db.engine.execute("SELECT team_name FROM team")
    for i in teams:
        print(i[0])
    match1 = Matches.query.filter_by(match_id=id).first()
    if request.method == 'POST':
        if match1:
            db.session.delete(match1)
            db.session.commit()
 
            t1_name = request.form['t1_name']
            t2_name =request.form['t2_name']
            stadium = request.form['stadium']
            match_date_time = request.form['match_date_time']
            winner = request.form['winner']
            losser = request.form['losser']
            match1 = Matches(match_id=id,t1_name=t1_name,t2_name=t2_name, stadium=stadium,match_date_time=match_date_time,winner=winner,losser=losser)
 
            db.session.add(match1)
            db.session.commit()
            return redirect(f'/datamatch/{id}')
        return f"match with id = {id} Does not exist"
 
    return render_template('update.html', match1 = match1,teamnames=teamnames,teams=teams)

#delete
@app.route('/datamatch/<string:id>/delete', methods=['GET','POST'])
def deletematch(id):
    match1 = Matches.query.filter_by(match_id=id).first()
    if request.method == 'POST':
        if match1:
            db.session.delete(match1)
            db.session.commit()
            return redirect('/datamatch')
    
    return render_template('delete.html')

#............................................................matchs..............................................................................

class Team(db.Model): 
    team_id=db.Column(db.Integer,primary_key=True)                                       
    team_name=db.Column(db.String(100))                                       
    team_rank=db.Column(db.Integer)                                       
    captian_name=db.Column(db.String(1000))
    no_of_wins=db.Column(db.Integer)
    no_of_losses=db.Column(db.Integer)
    wicket_keeper=db.Column(db.String(1000))
    team_img=db.Column(db.String(10000))
    
    def __init__(self, team_id,team_name,team_rank,captian_name,no_of_wins,no_of_losses,wicket_keeper,team_img):
        self.team_id = team_id
        self.team_name = team_name
        self.team_rank = team_rank
        self.captian_name = captian_name 
        self.no_of_wins = no_of_wins
        self.no_of_losses = no_of_losses 
        self.wicket_keeper = wicket_keeper
        self.team_img = team_img
         
    def __repr__(self):
        return f"{self.team_id}:{self.team_name}:{self.team_rank}:{self.captian_name}:{self.no_of_wins}:{self.no_of_losses}:{self.wicket_keeper}:{self.team_img}"

#display all
@app.route('/datateam')
def RetrieveDataListofteam():
    session['player'] = False
    team2 = Team.query.all()
    session['team'] = True
    return render_template('datalist.html',team2 = team2)

# insert new entry
@app.route('/datateam/insert' , methods = ['GET','POST'])
def createteam():
    
    if request.method == 'GET':
        return render_template('insert.html')
 
    if request.method == 'POST':
        team_id = request.form['team_id']
        team_name = request.form['team_name']
        team_rank = request.form['team_rank']
        captian_name = request.form['captian_name']
        no_of_wins = request.form['no_of_wins'] 
        no_of_losses = request.form['no_of_losses'] 
        wicket_keeper = request.form['wicket_keeper']
        team_img = request.form['team_img']
        team1 = Team(team_id=team_id, team_name=team_name, team_rank=team_rank,captian_name=captian_name,no_of_wins=no_of_wins,no_of_losses=no_of_losses,wicket_keeper=wicket_keeper,team_img=team_img)
        db.session.add(team1)
        db.session.commit()
        db.engine.execute('UPDATE team JOIN (SELECT team_id,@curteam_rank:=@curteam_rank +1 AS team_rank FROM team JOIN (SELECT @curteam_rank:=0)r ORDER BY no_of_wins DESC)team_rank ON (team_rank.team_id=team.team_id) SET team.team_rank=team_rank.team_rank;')
        return redirect('/datateam')

#display single entry for user
@app.route('/datateam/<int:id>')
def RetrieveSingleteam(id):
    team1 = Team.query.filter_by(team_id=id).first()
    if team1:
        return render_template('data.html', team1 = team1)
    return f"team with id ={id} Doenst exist"

# update 
@app.route('/datateam/<int:id>/update',methods = ['GET','POST'])
def updateteam(id):
    team1 = Team.query.filter_by(team_id=id).first()
    if request.method == 'POST':
        if team1:
            db.session.delete(team1)
            db.session.commit()
            team_name = request.form['team_name'] 
            team_rank = request.form['team_rank']
            captian_name = request.form['captian_name']
            no_of_wins =request.form['no_of_wins']
            no_of_losses = request.form['no_of_losses']
            wicket_keeper= request.form['wicket_keeper']
            team_img= request.form['team_img']
            team1 = Team(team_id=id,team_name=team_name,team_rank=team_rank,captian_name=captian_name,no_of_wins=no_of_wins,no_of_losses=no_of_losses,wicket_keeper=wicket_keeper,team_img=team_img)
 
            db.session.add(team1)
            db.session.commit()
            db.engine.execute('UPDATE team JOIN (SELECT team_id,@curteam_rank:=@curteam_rank +1 AS team_rank FROM team JOIN (SELECT @curteam_rank:=0)r ORDER BY no_of_wins DESC)team_rank ON (team_rank.team_id=team.team_id) SET team.team_rank=team_rank.team_rank;')
        
            return redirect(f'/datateam/{id}')
        return f"team with id = {id} Does not exist"
 
    return render_template('update.html', team1 = team1)

#delete
@app.route('/datateam/<int:id>/delete', methods=['GET','POST'])
def deleteteam(id):
    team1 = Team.query.filter_by(team_id=id).first()
    if request.method == 'POST':
        if team1:
            db.session.delete(team1)
            db.session.commit()
            return redirect('/datateam')
    
    return render_template('delete.html')

#.........................................................................team......................................................................


class Players(db.Model): 
    player_id=db.Column(db.String(100),primary_key=True)                                       
    team_name=db.Column(db.String(100))                                       
    player_name=db.Column(db.String(100))                                       
    age=db.Column(db.Integer)
    no_of_t20=db.Column(db.Integer)
    playing_role=db.Column(db.String(1000))
    batting_style=db.Column(db.String(1000))
    avg=db.Column(db.Float)                                       
    total_runs=db.Column(db.Integer)
    sr=db.Column(db.Float)
    fifty_hundrand=db.Column(db.String(1000))
    bowling_type=db.Column(db.String(1000))
    no_of_wicket=db.Column(db.Integer)
    economy=db.Column(db.Float)
    player_img=db.Column(db.String(10000))

    def __init__(self, player_id,team_name,player_name,age,no_of_t20,playing_role,batting_style,avg,total_runs,sr,fifty_hundrand,bowling_type,no_of_wicket,economy,player_img):
        
        self.player_id = player_id
        self.team_name = team_name
        self.player_name = player_name
        self.age = age
        self.no_of_t20 = no_of_t20 
        self.playing_role = playing_role
        self.batting_style = batting_style 
        self.avg = avg   
        self.total_runs = total_runs  
        self.sr = sr
        self.fifty_hundrand = fifty_hundrand 
        self.bowling_type = bowling_type  
        self.no_of_wicket = no_of_wicket
        self.econamy = economy    
        self.player_img =player_img
        
    def __repr__(self):
        return f"{self.player_id}:{self.team_name}:{self.player_name}:{self.age}:{self.no_of_t20}:{self.playing_role}:{self.batting_style}:{self.avg}:{self.total_runs}:{self.sr}:{self.fifty_hundrand}:{self.bowling_type}:{self.no_of_wicket}:{self.economy}:{self.player_img}"

#display all
@app.route('/dataplayer')
def RetrieveDataListofplayer():
    player2 = Players.query.all()
    print(player2)
    session['player'] = True
    return render_template('datalist.html',player2 = player2)

# insert new entry
@app.route('/dataplayer/insert' , methods = ['GET','POST'])
def createplayer():
    if request.method == 'GET':
        teams = db.engine.execute("SELECT team_name FROM team")
        return render_template('insert.html',teams=teams)
 
    if request.method == 'POST':
        player_id = request.form['player_id']
        team_name = request.form['team_name']
        player_name = request.form['player_name']
        age = request.form['age']
        no_of_t20 = request.form['no_of_wicket']
        playing_role = request.form['playing_role']
        batting_style = request.form['batting_style']
        avg = request.form['avg']
        total_runs = request.form['total_runs']  
        sr = request.form['sr']
        fifty_hundrand = request.form['fifty_hundrand']
        bowling_type = request.form['bowling_type']
        no_of_wicket = request.form['no_of_wicket']
        economy = request.form['economy']
        player_img=request.form['player_img']          
        player1 = Players(player_id=player_id, team_name=team_name,player_name=player_name,age=age,no_of_t20=no_of_t20,playing_role=playing_role,batting_style=batting_style,avg=avg,total_runs=total_runs,sr=sr,fifty_hundrand=fifty_hundrand,bowling_type=bowling_type,no_of_wicket=no_of_wicket,economy=economy,player_img=player_img)
        db.session.add(player1)
        db.session.commit()
        return redirect(f'/editplayer/{team_name}')

#display single entry for user
@app.route('/dataplayer/<string:id>')
def RetrieveSingleplayer(id):
    player1 = Players.query.filter_by(player_id=id).first()
    if player1:
        return render_template('data.html', player1 = player1)
    return f"player with id ={id} Doenst exist"

# update 
@app.route('/dataplayer/<string:id>/update',methods = ['GET','POST'])
def updateplayer(id):
    teamnames=db.engine.execute("select team_name from team")
    player1 = Players.query.filter_by(player_id=id).first()
    if request.method == 'POST':
        if player1:
            db.session.delete(player1)
            db.session.commit()
 
            team_name = request.form['team_name']
            player_name = request.form['player_name']
            age = request.form['age']
            no_of_t20 = request.form['no_of_wicket']
            playing_role = request.form['playing_role']
            batting_style = request.form['batting_style']
            avg = request.form['avg']
            total_runs = request.form['total_runs']  
            sr = request.form['sr']
            fifty_hundrand = request.form['fifty_hundrand']
            bowling_type = request.form['bowling_type']
            no_of_wicket = request.form['no_of_wicket']
            economy = request.form['economy'] 
            player_img = request.form['player_img']         
            player1 = Players(player_id=id, team_name=team_name,player_name=player_name,age=age,no_of_t20=no_of_t20,playing_role=playing_role,batting_style=batting_style,avg=avg,total_runs=total_runs,sr=sr,fifty_hundrand=fifty_hundrand,bowling_type=bowling_type,no_of_wicket=no_of_wicket,economy=economy,player_img=player_img)
            
            db.session.add(player1)
            db.session.commit()
            return redirect(f'/dataplayer/{id}')
        return f"player with id = {id} Does not exist"
 
    return render_template('update.html', player1 = player1,teamnames=teamnames)

#delete
@app.route('/dataplayer/<string:id>/delete', methods=['GET','POST'])
def deleteplayer(id):
    player1 = Players.query.filter_by(player_id=id).first()
    teamname = db.engine.execute('SELECT team_name FROM players WHERE player_id=(%s)',id)
    for i in teamname:
        team=i[0]
        print(i[0])
    if request.method == 'POST':
        if player1:
            db.session.delete(player1)
            db.session.commit()
            return redirect(f'/editplayer/{team}')
    
    return render_template('delete.html',player1=player1)

#..................................................players................................................................................

@app.route("/details/<string:id>")
def details(id):
    match1 = Matches.query.filter_by(match_id=id).first()
    team1 = Team.query.all()
    print(match1)
    teamquery2 = db.engine.execute("SELECT team_name,team_img FROM team,matches WHERE (team_name=t1_name OR team_name=t2_name) AND match_id=(%s)",id)
    current_time=datetime.datetime.now()
    teamquery1 = db.engine.execute("SELECT match_date_time FROM matches WHERE match_id=(%s)",id)
    for i in teamquery1 :
        if current_time > i[0] :  
                print("true")
                query1 = db.engine.execute("SELECT player_name,player_id,player_img FROM players,matches WHERE team_name=t1_name AND match_id=(%s) ORDER BY RAND () LIMIT 11",id)
                query2 = db.engine.execute("SELECT player_name,player_id,player_img FROM players,matches WHERE team_name=t2_name AND match_id=(%s) ORDER BY RAND () LIMIT 11",id)
                return render_template('details.html',match1=match1,query1=query1,query2=query2,teamquery2=teamquery2,team1=team1)
    
    query1 = db.engine.execute("SELECT player_name,player_id,player_img FROM players,matches WHERE team_name=t1_name AND match_id=(%s)",id)
    query2 = db.engine.execute("SELECT player_name,player_id,player_img FROM players,matches WHERE team_name=t2_name AND match_id=(%s)",id)
    return render_template('details.html',match1=match1,query1=query1,query2=query2,teamquery2=teamquery2,team1=team1)


@app.route("/team/<string:id>")
def team(id):
    team1 = Team.query.filter_by(team_name=id).first()
    teamquery1 = db.engine.execute("SELECT * FROM coach WHERE team_name=(%s)",id)
    teamplayers =  db.engine.execute("SELECT player_name,player_id,player_img FROM players WHERE team_name=(%s)",id)
    return render_template('team.html',team1=team1,teamquery1=teamquery1,teamplayers = teamplayers)


@app.route("/")
def index():
    session['logged_in'] = False
    return render_template('index.html')
    

@app.route("/test")
def test():
    try:
        Admin.query.all()
        Cursor.execute("SELECT img FROM Coach WHERE Coach_id=22")
        record=Cursor.fetchone()
        data=convert_data(record)
        print(data)
        return 'database connected'
    except:
        return 'database not connected'


@app.route("/home")
def home():
    query=db.engine.execute("DELETE FROM Players WHERE Player_id='ind1'")
    print(query)
    return render_template('home.html',query=query)

@app.route('/coach/<int:id>')
def SingleCoach(id):
    coach1 = Coach.query.filter_by(coach_id=id).first()
    if coach1:
        return render_template('coach.html', coach1 = coach1)
    return f"coach with id ={id} Doenst exist"

@app.route("/points")
def points():
    point = Team.query.order_by(desc(Team.no_of_wins)).all()
    return render_template('points.html',point=point,)


    
@app.route("/player/<string:id>")
def player(id):
    player1 = Players.query.filter_by(player_id = id).first()
    return render_template('player.html',player1=player1)

@app.route('/editplayer/<string:id>')
def RetrieveDataListofplayeredit(id):
    session['player'] = True
    session['team'] = False
    
    player2 = Players.query.filter_by(team_name=id).all()
    return render_template('playertable.html',player2 = player2)

app.run(debug=True)


@app.route("/a")
def test1():
    # a = Coach.query.filter_by(coach_id = 44).first()
    # newimg =  io.BytesIO(a.img)
    # newimg.seek(0) 
    # b = Image.open(newimg)
    # c=b.save('test.png','PNG')
    # b=Image.frombuffer("I;16",(5,10),a.img,"raw","I;12")
    # b.show()
    # print (a.coach_id,a.c_name)
    

    # current_time=datetime.datetime.now()
    # # today_date = datetime.datetime.today()
    # print(current_time)
    # # print(today_date)
    # teamquery1 = db.engine.execute("SELECT match_date_time FROM matches")
    # for i in teamquery1 :
    #     print(i)
    #     if current_time < i[0] :
    #         print("true")
    #     else :
    #         print("false")

    coach1 = Coach.query.filter_by(coach_id=22).first()
    teamnames = db.engine.execute("SELECT team_name FROM team")
    if request.method == 'POST':
        if coach1:
            db.session.delete(coach1)
            db.session.commit()
 
            name = request.form['c_name']
            team_name = request.form['team_name']
            img = request.form['img']
            # filename = secure_filename(img.filename)
            # mimetype = img.mimetype
            
            coach1 = Coach(coach_id=22, c_name=name, team_name=team_name,img=img)
 
            db.session.add(coach1)
            db.session.commit()
            return redirect('b.html')
        return f"coach with id = {22} Does not exist"
 
    return render_template('a.html', coach1 = coach1, teamnames = teamnames)

# @app.route('/filter',methods=['GET'])
# def filter():
#     if request.method=='GET':
#         q=request.args.get('q')
#         teamnames = db.engine.execute("SELECT * FROM players")
#         if not q :
#             q=request.GET['q']
        
#     return render_template('filter.html',teamnames=teamnames,)
    
# point = Team.query.order_by(desc(Team.no_of_wins)).all()
    
   
    # return render_template("a.html",teamquery1=teamquery1)



