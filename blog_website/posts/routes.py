''' This routes file will contain all routes related to posts
    as we are using blueprint change all url_for('route_function') to url_for('blueprint_name.route_funtion') in all files including templates
'''

from flask import render_template,redirect,url_for,flash,request,abort
from flask_login import current_user,login_required
from blog_website.db_models import User,Post
from blog_website import db
from blog_website.posts.forms import NewPost

from flask import Blueprint
posts=Blueprint('posts',__name__)

# route to add new post
@posts.route('/post/new/',methods=['GET','POST'])
@login_required
def new_post():
    form=NewPost()
    if form.validate_on_submit():
        flash("Post added succesfully",'success')
        post=Post(title=form.title.data,content=form.content.data,author=current_user) #also you can do user_id=current_user.id
        db.session.add(post)
        db.session.commit()
        # as we are using blueprints now therfore in url_for method we need to specify blueprint.route_function
        return redirect(url_for('main.home'))
    return render_template('new_post.html',title='New Post',form=form,legend="New Post")
           
#route to go a specific post
# you can add variable in route like <int:post_id> example /post/1 ,/post/2 etc
@posts.route('/post/<int:post_id>')
def post(post_id):
    # in home route when the title link is clicked is calls the post function and it gets post.id as argument
    post=Post.query.get_or_404(post_id) #this will give the post with the id if it exists else give a 404 error
    return render_template('post.html',title=post.title,post=post)

#route to update a post
@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.user_id!=current_user.id: # you can also use post.author!=current_user
        abort(403)
    form=NewPost()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        #as we are just updating the data in db no need of session.add
        db.session.commit()
        flash("Post updated successfully",'success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        # to autopopulate update form with existing posst data
        form.title.data=post.title
        form.content.data=post.content
    return render_template('new_post.html',title='Update post',legend='Update Post',form=form)

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.user_id!=current_user.id: # you can also use post.author!=current_user
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!','success')
    return redirect(url_for('main.home'))


@posts.route('/post/user/<string:username>',methods=['GET'])
def user_post(username):
    page=request.args.get('page',1,type=int)
    print(username)
    # posts=Post.query.where(Post.user_id==user_id).order_by(Post.date_posted.desc()).paginate(page=page,per_page=2)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=2)
    return render_template('user_post.html',title="posts",posts=posts,user=user)