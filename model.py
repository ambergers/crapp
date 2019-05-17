"""Models and database functions for crApp."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from faker import Faker
from faker.providers import misc

# Establish connection to the PostgreSQL database
db = SQLAlchemy()

# Set up Faker object to generate fake initial passwords for users
fake = Faker()
fake.add_provider(misc)

##################################################################
# Model definitions

class User(db.Model):
    """User of crApp website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(30), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    is_premium = db.Column(db.Boolean, default=False, nullable=False)

    # Define relationships
    lists = db.relationship("NamedList")
    checkins = db.relationship("CheckIn")
    ratings = db.relationship("Rating", backref=db.backref("user"))
    
    def __init__(self, full_name, email, password=None):
        """Initialize a User object."""

        self.full_name = full_name
        self.email = email
        self.created_at = datetime.now()
        
        if password:
            self.password = password
        else:
            self.password = fake.password(length=10, special_chars=True, digits=True, 
                                          upper_case=True, lower_case=True) 

    def __repr__(self):
        """Provide helpful User representation when printed."""

        return f"<User id={self.user_id} name={self.full_name}>"

class Bathroom(db.Model):
    """Bathroom on crApp website."""

    __tablename__ = "bathrooms"

    bathroom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    latitude = db.Column(db.Float(10,6), nullable=False)
    longitude = db.Column(db.Float(10,6), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    is_premium = db.Column(db.Boolean, default=False, nullable=False)

    # Define relationships
    checkins = db.relationship("CheckIn")
    ratings = db.relationship("Rating")
   
    def __init__(self, latitude, longitude, address=None):
        self.latitude = latitude
        self.longitude = longitude
        if address:
            self.address = address

    def __repr__(self):
        """Provide helpful Bathroom representation with printed."""

        return f"<Bathroom id={self.bathroom_id} lat_long={self.latitude},{self.longitude}>"

class NamedList(db.Model):
    """Named lists for users to add bathrooms to (fave, least fave, etc)."""

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    # Define relationship
    list_items = db.relationship("ListItem", backref=db.backref("named_list"))
   
    def __init__(self, list_name, user_id):
        self.list_name = list_name
        self.user_id = user_id

    def __repr__(self):
        """Provide helpful NamedList representation when printed."""

        return f"<List id={self.list_id} name={self.list_name}>"

class ListItem(db.Model):
    """ListItems - bathrooms, user, named list they've been put on."""

    __tablename__ = "list_items"

    list_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathrooms.bathroom_id'), nullable=False)
    datetime_added = db.Column(db.DateTime, nullable=False)

    def __init__(self, list_id, user_id, bathroom_id):
        self.list_id = list_id
        self.user_id = user_id
        self.bathroom_id = bathroom_id
        self.datetime_added = datetime.now()

    def __repr__(self):
        """Provide helpful ListItem representation when printed."""

        return f"<ListItem list_id={self.list_id} user={self.user_id} bathroom={self.bathroom_id}>"

class CheckIn(db.Model):
    """Checkins when a user visits a bathroom."""

    __tablename__ = "checkins"

    checkin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathrooms.bathroom_id'), nullable=False)
    checkin_datetime= db.Column(db.DateTime, nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.rating_id'), nullable=True)

    def __init__(self, user_id, bathroom_id, checkin_datetime=None, rating_id=None):
        self.user_id = user_id
        self.bathroom_id = bathroom_id
        
        if checkin_datetime:
            self.checkin_datetime = checkin_datetime
        else:
            self.checkin_datetime = datetime.now()

        if rating_id:
            self.rating_id = rating_id
        

    def __repr__(self):
        """Provide helpful CheckIn representation when printed."""
        
        return f"<Checkin id={self.checkin_id} user={self.user_id} bathroom={self.bathroom_id} date={self.checkin_datetime}>"

class Rating(db.Model):
    """User ratings, must have checked in to make a rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathrooms.bathroom_id'), nullable=False)
    checkin_id = db.Column(db.Integer, db.ForeignKey('checkins.checkin_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.String(200), nullable=True)

    def __init__(self, user_id, bathroom_id, checkin_id, score, review_text=None):
        self.user_id = user_id
        self.bathroom_id = bathroom_id
        self.checkin_id = checkin_id
        self.score = score
        if review_text:
            self.review_text = review_text

    def __repr__(self):
        """Provide helpful rating representation when printed."""

        return f"<Rating id={self.rating_id} user={self.user_id} bathroom={self.bathroom_id} checkin={self.checkin_id} score={self.score}>"

#################################################################
# Helper functions

def connect_to_db(app):
    """Connect database to flask app."""

    # Configure to use PostgreSQL db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///crapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # If run interactively, will be in state to work with db directly

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
