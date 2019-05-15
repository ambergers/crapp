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
    created_at = db.Column(db.Datetime, nullable=False)
    is_premium = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provide helpful User representation when printed."""

        return f"<User user_id={self.user_id} name={self.full_name}>"


