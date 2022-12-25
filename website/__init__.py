from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_apscheduler import APScheduler



db = SQLAlchemy()
DB_NAME = "database.db"


scheduler = APScheduler()
    
def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'sdlkasdjfslkjl'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .models import User, Note
    
    with app.app_context():
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
   
    scheduler.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    with app.app_context():
        
        
        scheduler.start()
        from . import Scheduler
    
        return app