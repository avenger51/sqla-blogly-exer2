from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
   """Connect the database to the Flask app."""
   db.app = app
   db.init_app(app)


class User(db.Model):
    """User table to instantiate."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False, unique=False)
    last_name  = db.Column(db.Text, nullable=False, unique=False)
    image_url = db.Column(db.Text, nullable=False, unique=False)
    
    def __repr__(self):  #huh?
        usr = self
        return f"<User {usr.id} {usr.first_name} {usr.last_name} {usr.image_url}>"
    
#EXERCISE 2 BELOW
class Post(db.Model):
   
   __tablename__ = "posts"

   post_id = db.Column(db.Integer, primary_key=True)
   post_title = db.Column(db.Text, nullable=False, unique=True)
   post_content = db.Column(db.Text, unique=True)
   post_created_at = db.Column(db.Integer, nullable=True, unique=False) #, default=datetime.utcnow)


   user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  #<---- this is going to users to get the id...
   #user = db.relationship("User", backref="posts")
#user_id = db.column(db.Integer, db.ForeignKey('users.id'))  #<---- backup to use for Exer 3





#can't tell if this is needed:
#relationship = db.relationship('User', )
#relationship = db.relationship('User', backref='post')
    
#CLASSES FOR TAG EXERCISE 3
#
#class Post(db.model):
#    """id(pk), title, content, created_at, user_id(FK)"""
#    __tablename__ = "posts"
#
#    post_id = db.column(db.integer, primary_key=True)
#    post_title = db.column(db.Text, nullable=False, unique=True)
#    post_content = db.column(db.text, unique=True)
#    post_created_at = db.column(db.integer, nullable=False, unique=False)
#    user_id = db.column(db.Integer, db.ForeignKey('users.id'))  #<---- this is going to users to get the id...
#    
#    #can't tell if this is needed:
#    relationship = db.relationship('User', )
#    relationship = db.relationship('User', backref='post')
#
#class Tag(db.model):
#    """id(pk), name"""
#    __tablename__ = "tags"
#
#    tag_id = db.column(db.integer, primary_key=True)
#    tag_name = db.column(db.Text, nullable=False, unique=True)
#
#
#class PostTag(db.model):
#    """post_id (PK/FK), tag_id(PK/FK)"""
#    __tablename__ = "post_tags"
#   
#    #post_id = db.column(db.integer, primary_key=True)  <---removed these two to make a PK/PK below
#    #tag_id = db.column(db.integer, primary_key=True)
#    #testing foreign key stuff
#    post_id = db.column(db.integer, db.ForeignKey('posts.post_id'), primary_key=True)  #<----to point to the PostID
#    tag_id = db.columb(db.integer, db.ForeignKey('tags.tag_id'), primary_key=True) #<---to point to TagID
#  
#
#
#


#testing
#    @classmethod
#    def get_users_by_image_url(cls, image_url):
#        return cls.query.filter_by(image_url=image_url).all()



#not sure what to do with this:
#if __name__ == "__main__":
# So that we can use Flask-SQLAlchemy, we'll make a Flask app
#    from app import app
#    connect_db(app)
#removed below to not delete the database..
#
#    db.drop_all()
#    db.create_all()
   