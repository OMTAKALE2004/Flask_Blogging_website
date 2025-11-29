#this file tells python that it is a package.


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog_website.config import Config






#instance of sql alchemy
db=SQLAlchemy()

bcrypt=Bcrypt()

login_manager=LoginManager()

# this will redirect user to login if user is not logged in and trying to access account page
login_manager.login_view='users.login'
login_manager.login_message_category='info'

mail=Mail()


# here we are creating app for this specific Config only so i this way we can make different Config class each having 
# different credentials for example : a class with differnt secret key or db uri
# by this way we dont need to eveytime physically change the config variable jsu create new and use that class in below
# create_app function

# also we are initializing db,mail,bcrypt, login_manager in this function for this specific app only and we are keeping there
# extension/instance outside of this function.

def create_app(config=Config):
    app=Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # importing blueprints
    from blog_website.users.routes import users
    from blog_website.posts.routes import posts
    from blog_website.main.routes import main
    from blog_website.errors.handlers import errors

    # registering the blueprints in app
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app

# now we dont have a app variable but we hhave used app variable in various places now we have to make changes there.
# because now app variable is in the function create_app and this function return app
# no at places were you have used app just replace it with current_app
#  Note:import current_app from flask