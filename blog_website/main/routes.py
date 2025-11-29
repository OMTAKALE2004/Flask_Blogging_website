'''This routes file will contain any other routes that are not related to users and posts'''


from flask import render_template,request
from blog_website.db_models import Post

from flask import Blueprint
main=Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page=request.args.get('page',1,type=int) #this will search for page keyword in query parameter[url] default is 1 and only integer value is allowed
                                            # beacuse page no are 1,2,3 therefore only nt is aalowed
    # we are querying post which are most recent first
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=2)
    return render_template("home.html",posts=posts)

@main.route("/about")
def about():
    return render_template("about.html")