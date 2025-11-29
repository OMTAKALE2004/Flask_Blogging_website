from itsdangerous import URLSafeTimedSerializer as serializer
import secrets
from datetime import datetime,timezone
from blog_website import db,login_manager
from flask_login import UserMixin
from flask import current_app
# Flask-Login uses this function to reload the logged-in user from the user ID stored in the session cookie.
# When a user logs in, their ID is saved in a secure cookie.
# On each request, Flask-Login calls this function to get the full User object from the database.

# in leman terms
# so when i login it stores some data in cookie in the browser and then when i visit different pages on the 
# websiteit uses that stored data to ensure that the logged in person is only viewing that page and not the 
# other user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin): #table name is class name in lowercase
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(120),nullable=False,unique=True)
    password=db.Column(db.String(60),nullable=False)
    img_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    posts=db.relationship('Post',backref='author',lazy=True)
# what db.relationship does it creeates a one to amny relationship between users and posts a user can have many posts but
# each post is associated with one user only
# 'Post' → means it’s related to the Post model.

# backref='author' → this automatically adds a new attribute author to each Post object, which refers back to the User who wrote it.

# lazy=True → means posts are loaded from the database only when you access them (saves memory).

    salt=secrets.token_hex(32) #class variable

    def get_reset_token(self):
        s=serializer(secret_key=current_app.config['SECRET_KEY'],salt=User.salt)
        data={'user_id':self.id}
        return s.dumps(data)
    
    @staticmethod
    def verify_token(token):
        s=serializer(secret_key=current_app.config['SECRET_KEY'],salt=User.salt)
        try:
            user_id=s.loads(token,max_age=1800)['user_id']
           
        except:
            return None
        return User.query.get(user_id)
    


    def __repr__(self) -> str:
        return f"User('{self.username}','{self.email}','{self.img_file}')"
    


class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.now(timezone.utc))
    content=db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Note: it is user.id and not User.id even thoug our class name is User because in sql alchemy it convert class name
    # to lower case and it is then used as the table name.

    
    def __repr__(self) -> str:
        return f"Post('{self.title}','{self.date_posted}')"
