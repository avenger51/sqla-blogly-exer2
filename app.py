
"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session, abort, current_app, url_for
from models import db, connect_db, User, Post #note: this will break everything
#if these don't exist in models.py - Post Tag, PostTag, Post - To be added later...
#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #removed for troubleshooting
app.config['SQLALCHEMY_ECHO'] = True  #removed for troubleshooting
app.config['SECRET_KEY'] = 'typicalbs'
#toolbar = DebugToolbarExtension(app) #THIS NEVER WORKS

connect_db(app)
# 100% REQUIRED TO ADD app.app_context() so that %run app.py creates Post class
with app.app_context():
    db.create_all()
#db.init_app(app) # THIS BREAKS BASIC HOME PAGE FUNCTIONALITY


@app.route("/", methods=['GET', 'POST'])
def add_user():
    
    """Add a new user to the database"""
    if request.method == 'POST':
        # Get user info
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']
        
        # Create User object and add to db
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        #user = User.query.filter_by(first_name=first_name).first()

        # Redirect to the user list page
       # if new_user:
       #     return redirect('/user_listing')
        
       # if user:
       #     return redirect(f'/users/{user.id}/posts/new')
    
    #return render_template("home.html")  # Pass user_id to the template

        return redirect('/user_listing')
    
    return render_template("home.html") 

@app.route ('/user_listing')
def display_users():
      """Get list of users"""
      users = User.query.all()
      return render_template("user_listing.html", users=users) 


@app.route('/user_details/<int:user_id>')
def display_user_details(user_id):
    """Display user details based on user ID"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()

    return render_template("user_details.html", user=user, user_id=user_id, posts=posts) #had to add user_id as well..


@app.route('/add_post_form/<int:user_id>', methods=['GET'])
def add_post_form(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("add_post_form.html", user=user, user_id=user_id)  #needed user_id=user_id

@app.route('/create_post/<int:user_id>', methods=['POST'])
def create_post(user_id):
    post_title = request.form['post_title']
    post_content = request.form['post_content']
    
    # Create a new post
    new_post = Post(post_title=post_title, post_content=post_content, user_id=user_id)

    # Add the new post to the database
    db.session.add(new_post)
    db.session.commit()

    # Redirect to the post_detail page for the newly created post
    return redirect(url_for('post_detail', user_id=user_id, post_id=new_post.post_id))
    
@app.route('/post_detail/<int:user_id>/<int:post_id>', methods=['GET', 'POST'])
def post_detail(user_id, post_id):
     
     post = Post.query.get_or_404(post_id)
     user = User.query.get_or_404(user_id)

     if request.method == 'POST':
        if 'delete_post' in request.form:
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('display_user_details', user_id=user_id,))

     return render_template("post_detail.html", post=post, user=user, user_id=user_id, post_id=post_id)



@app.route('/post_edit/<int:user_id>/<int:post_id>', methods=['GET','POST'])
def post_edit(user_id, post_id):
    
     post = Post.query.get_or_404(post_id)
     user = User.query.get_or_404(user_id)

     if request.method == 'POST':
         new_title = request.form['new_title']
         new_content = request.form['new_content']

         post.post_title = new_title 
         post.post_content = new_content

         db.session.commit()
    
    

         return redirect(url_for('post_detail', user_id=user_id, post_id=post_id))
     

     return render_template("post_edit.html", post=post, user=user, post_id=post_id, user_id=user_id)


#if __name__ == "__main__":SSS
#    # Create the User and Post tables
#    db.create_all()
#    app.run(debug=True)

#@app.route('/show_post_form')
#def show_post_form():
#    if request.method == 'POST':
#        user_id = request.form.get('user_id')
#        user = User.query.get(user_id)
#
#        if user:
#
#            return redirect(f'/users/{user_id}/posts/new')
#        
#    return render_template("new_post_form.html")

#EXER 2 BELOW:

##GET to show form to add a post for the user
#WTF WON'T WORK
#@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
#def show_post_form(user_id):
#
#    first_name = User.query.get_or_404(user_id)
#    return render_template("new_post_form.html", user=first_name)
##POST handle post add form, add post, redirect to user detail page
#@app.route('/users/<int:user_id/new')
#def add_user_post(user_is):
#     
##GET show a post, show buttons to edit/delete post
#@app.route('/posts/<int:post_id>')
#def show_post(post_id)
#     
##GET show form to edit a post and cancel (back to user page)
#@app.route('/posts/<int:post_id>/edit')
#def show_edit_form(post_id):
#     
##POST handle editing of a post.  Redirect back to post view
#@app.route('/posts/<int:post_id>/edit')
#def post_handler(post_id):
#
##POST delete the post
#@app.route('/posts/<int:post_id>/delete')
#def post_delete(post_id):
#     

#TAG EXERCISE 3 BELOW

##LIST ALL TAGS WITH LINKS TO tags_detail page
##GET
#@app.route('/tags')
#def tags_list():
#    tag_test = 'testing'
#    return render_template("tag_list.html", tag_test=tag_test)
#
###SHOW FORM TO ADD A NEW TAG
##GET
#@app.route('/tags/new')
#def tags_new():
#    #new_tag = request.form['new_tag']
#    tags_new_test = 'tagtest'
#
#    return render_template("new_tags_form.html", tags_new_test=tags_new_test)
#
##SHOW DETAILS ABOUT THE TAG (include links to edit and delete)
##GET
#@app.route('/tags/<int:tag_id>')
#def tags_detail(tag_id):



#NOT WORKING
#@app.route("/check_username", methods=['POST'])
#def check_username():
#    """Check the entered username and redirect to a new page if found."""
#    # Get the user's first name from the form
#    first_name = request.form['first_name']
#    
#    # Query the database to check if the user exists
#    user = User.query.filter_by(first_name=first_name)
#    
#    if user:
#        # Redirect to a new page with the user's ID as a parameter
#        return redirect(f'/users/{user.id}/posts/new')
#    else:
#        # Handle the case when the user is not found
#        flash("User not found. Please enter a valid name.")
#        return redirect('/')
#    
#     
#@app.route("/user_lookup", methods=["POST"])
#def user_lookup():
#    """Look up a user by their ID and redirect to the new_post_form route."""
#    user_id = request.form.get("user_id")  # Get the user ID from the form
#    user = User.query.get(user_id)  # Try to find the user by ID in the database
#
#    if user:
#        # Redirect to the new_post_form route with the user's ID as a parameter
#        return redirect(f"/users/{user_id}/posts/new")
#    else:
#        flash("User not found. Please enter a valid user ID.")
#        return redirect("/")
#









#NOTE:  CANNOT GET 'user_id' to function

#@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
#def edit_user_submit(user_id):
#    user = User.query.get_or_404(user_id)
#
#    if request.method == "POST":
#       
#        user.first_name = request.form['first_name']
#        user.last_name = request.form['last_name']
#        user.image_url = request.form['image_url']
#        
#    
#        db.session.commit()
#       
#        return redirect('/user_listing')  # Update this URL as needed
#
#    return render_template('edit_user.html', user=user)
#
##@app.route("/edit_user/<int:user_id>", methods=["GET"])
##def edit_user_form(user_id):
##    user = User.query.get_or_404(user_id)
#    return render_template('edit_user.html', user=user)










#ORIGINAL BROKEN:
#@app.route("/edit_user/<int:user_id>")
#def edit_user(user_id):
#      # NEED TO DISPLAY THE PAGE WITH FORMS/
#      #if request.method == 'POST':
#        user = User.query.get_or_404(user_id)
#       # if user is None:
#        # Handle the case where the user with the specified ID doesn't exist
#            #abort(404)
#        return render_template('edit_user.html', user=user)
#    
#@app.route("/edit_user/<int:user_id>", methods=["POST"])
#def users_edit(user_id):
#    """Show a form to edit an existing user"""
#   
#    
#    user_id.first_name = request.form['first_name']
#    user_id.last_name = request.form['last_name']
#    user_id.image_url = request.form['image_url']
#    
#    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
#    db.session.add(new_user)
#    db.session.commit()
#        
#        # Redirect to the user list page
#    return redirect('/user_listing')
#  
#   @app.route("/user_details/<int:user_id>/edit")

#ORIGINAL AND NOT SURE WHAT I WAS DOING WITH THIS:
#def display_user_details(user_id):
#    #SHOW A FORM TO ENTER A USER ID.
#   
#    user = User.query.get_or_404(user_id)
#    if user is None:
#        # Handle the case where the user with the specified ID doesn't exist
#        abort(404)
#     
#    # Perform some actions with the user data and return a response
#    return render_template("user_details.html", user=user)