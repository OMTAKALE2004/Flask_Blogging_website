#the task of this file is jsut to run our app instance

# app is not a variable now as we are using create_app function to create an app
# from blog_website import app

from blog_website import create_app
app=create_app()
if __name__=="__main__":
    app.run(debug=True)