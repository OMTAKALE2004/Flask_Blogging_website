''' This file will contain all forms related to users'''
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from flask_wtf.file import FileField,FileAllowed
from blog_website.db_models import User
from flask_login import current_user

class RegistraionForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    conf_pass=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    # the wtfforms automatically call this function when validating that field
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first() # Note filter_by only takes keyword arguments.
        if user:
            raise ValidationError("Username already exists.Try anaother one!")
        

    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already exists.Try anaother one!")


class LoginFOrm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    login=SubmitField('LogIn')



class AccountUpdate(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    prof_img=FileField('Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    # the wtfforms automatically call this function when validating that field
    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first() # Note filter_by only takes keyword arguments.
            if user:
                raise ValidationError("Username already exists.Try anaother one!")
        

    def validate_email(self,email):
        if email.data!=current_user.email:
            email=User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists.Try anaother one!")
            

class RequestResetForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request token')

    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError("No account found associated with this email.Register first!")
        
class ResetPassword(FlaskForm):
    password=PasswordField('password',validators=[DataRequired()])
    conf_pass=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Reset Password')
