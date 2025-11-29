''' this routes file will contain all routes which are related to users
as we are using blueprint change all url_for('route_function') to url_for('blueprint_name.route_funtion') in all files including templates'''


from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,current_user,logout_user,login_required
from blog_website import bcrypt,db
from blog_website.db_models import User,Post
from blog_website.users.forms import RegistraionForm,LoginFOrm,AccountUpdate,RequestResetForm,ResetPassword
from blog_website.users.utils import save_prof_img,send_reset_email

from flask import Blueprint
users=Blueprint('users',__name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated: #this will route the user to home page if it is already logged in 
        return redirect(url_for('main.home'))
    form=RegistraionForm()
    if form.validate_on_submit():
        # hashing the password
        pw_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created.You can now Login','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)

@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        # it ensures that if user has already logged in and try to go to login page is automatically redirected to home page
        return redirect(url_for('main.home'))
    form=LoginFOrm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            # to grab the next page
            # example scenario
            # suppose you are logged out but then also you try to access account page.
            # now as your are logged out it will make you to go to login page and once you have logged in it will
            # redirect you to home page beacause that's how we coded
            # but what this below line will do is store the page we were trying to acces before login and after
            # login it will redirect us to same page
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessfull. Incorrect Email or password",'danger')
    
    return render_template('login.html',title='Login',form=form)


@users.route("/logout")
def logout():
    logout_user() # this method logout the current user.It does not require current user as 
                  # argument as itknows the current user
    return redirect(url_for('main.home'))


@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    img_file=url_for('static',filename=f'Profile_picture/{current_user.img_file}')
    form=AccountUpdate()
    if form.validate_on_submit():
        # below lines will update the username and email of user
        if form.prof_img.data:
            prof_img=save_prof_img(form.prof_img.data)
            current_user.img_file=prof_img #img_file is column name in user table that store profile image
                                            # prof_img is name in form

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Account Info updated successfully",'success')
        return redirect('account') # this redirect helps to avoid that resubmission error given by browser
    
    # if request.method=='POST' and 'remove_pic' in request.form:
    #     print("im here")
    #     current_user.img_file=url_for('static',filename='Profile_picture/default.jpg')
    #     db.session.commit()
    #     flash("Profile image set to default",'info')
    #     return redirect('account')
    
    elif request.method=='GET': # so when we click on account tab when we are login so it is a GET request
                                # so in this condition we are trting to say if it is a GET request to the following things
        form.username.data=current_user.username #it will set the username in update form to current username means when you open account it will automatically show the current username filled in the form
        form.email.data=current_user.email
        

    return render_template('account.html',title='Account',img_file=img_file,form=form)


@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated: #this will route the user to home page if it is already logged in 
        return redirect(url_for('main.home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Password reset email has been send to your respective email id','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',form=form,title="Reset Password")


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated: #this will route the user to home page if it is already logged in 
        return redirect(url_for('main.home'))
    user=User.verify_token(token)
    if user is None:
        flash("The token is invalid or expired",'warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPassword()
    if form.validate_on_submit():
        pw_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=pw_hash
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html',title='Reset Password',form=form)


