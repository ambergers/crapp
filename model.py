"""Models and database functions for crApp."""

from flask_sqlalchemy import SQLAlchemy

# Establish connection to the PostgreSQL database
db = SQLAlchemy()


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
    created_at = db.Column(db.Date, nullable=False)
    is_premium = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provide helpful User representation when printed."""

        return f"<User id={self.user_id} name={self.full_name}>"

    # Define relationships
    lists = db.relationship("NamedList")
    checkins = db.relationship("CheckIn")
    ratings = db.relationship("Rating", backref=db.backref("ratings"))

class Bathroom(db.Model):
    """Bathroom on crApp website."""

    __tablename__ = "bathrooms"

    bathroom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    latitude = db.Column(db.Float('10,6'), nullable=False)
    longitude = db.Column(db.Float('10,6'), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    is_premium = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provide helpful Bathroom representation with printed."""

        return f"<Bathroom id={self.bathroom_id} lat_long={self.latitude},{self.longitude}>"

    # Define relationships
    checkins = db.relationship("CheckIn")
    ratings = db.relationship("Rating")

class NamedList(db.Model):
    """Named lists for users to add bathrooms to (fave, least fave, etc)."""

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    def __repr__(self):
        """Provide helpful NamedList representation when printed."""

        return f"<List id={self.list_id} name={self.list_name}>"

    # Define relationship
    list_items = db.relationship("NamedList", backref=db.backref("named_list"))

class ListItem(db.Model):
    """ListItems - bathrooms, user, named list they've been put on."""

    __tablename__ = "list_items"

    list_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathrooms.bathroom_id'), nullable=False)
    date_faved = db.Column(db.Date, nullable=False)

    def __repr__(self):
        """Provide helpful ListItem representation when printed."""

        return f"<ListItem list_id={self.list_id} user={self.user_id} bathroom={self.bathroom_id}>"

class CheckIn(db.Model):
    """Checkins when a user visits a bathroom."""

    __tablename__ = "checkins"

    checkin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathrooms.bathroom_id'), nullable=False)
    checkin_date= db.Column(db.Date, nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.rating_id'), nullable=True)

    def __repr__(self):
        """Provide helpful CheckIn representation when printed."""
        
        return f"<Checkin id={self.checkin_id} user={self.user_id} bathroom={self.bathroom_id} date={self.checkin_date}>"

class Rating(db.Model):
    """User ratings, must have checked in to make a rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathrooms.bathroom_id'), nullable=False)
    checkin_id = db.Column(db.Integer, db.ForeignKey('checkins.checkin_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful rating representation when printed."""

        return f"<Rating id={self.rating_id} user={self.user_id} bathroom={self.bathroom_id} checkin={self.checkin_id} score={self.score}>"

#################################################################
# Helper functions

def connect_to_db(app):
    """Connect database to flask app."""

    # Configure to use PostgreSQL db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If run interactively, will be in state to work with db directly

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
