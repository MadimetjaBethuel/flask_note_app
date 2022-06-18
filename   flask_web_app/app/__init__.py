from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    Create and initialize the app
    args: None
    returns: app
    """

    #initializimg flask 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'youwillneverguessthestring'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # location of the database
    db.init_app(app) # initialize the app

    
    from .views import views
    from .auth import auth

    # Register Blueprints and routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    #import modules 
    from .models import User, Note


    #create the database
    create_database(app)
    

    #flask login LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
  
    return app


def create_database(app):

    """
    check if the database exists and the create if it doesn't have
    args: app
    returns: None
    """
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')