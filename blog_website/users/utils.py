'''this file has all the supporting functions for routes'''

import os
import secrets
from PIL import Image
from flask_mail import Message
from flask import url_for,current_app
from blog_website import mail

def save_prof_img(prof_img):
    # so here we do not want to save image name as it was entered by user we can change the name of image to random name
    rand_hex=secrets.token_hex(8)
    # now we want to save the image in same extension in db as uploaded so we need to extract extention
    _,fext=os.path.splitext(prof_img.filename)
    img_name=rand_hex+fext
    img_path=os.path.join(current_app.root_path,'static/Profile_picture',img_name) 
    # logic to crop image to square
    output_size=(125,125)
    i=Image.open(prof_img)
    width,height=i.size
    x1=(width-min(width,height))//2
    y1=(height-min(width,height))//2
    x2=x1+min(width,height)
    y2=y1+min(width,height)
    i=i.crop((x1,y1,x2,y2))
    i.thumbnail(output_size)
    i.save(img_path) #our uploaded file will be stored at this location
    return img_name


# function to send email
def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message(subject='Regarding website password reset',sender='om2004takale@gmail.com',recipients=[user.email])
    msg.body=f''' To reset your password please visit the following link:
    {url_for('users.reset_password',token=token,_external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)