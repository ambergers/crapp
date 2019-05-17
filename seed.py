"""Utility file to seed bathroom, user, and list data to crapp database"""

from model import (User, Bathroom, NamedList, ListItem, CheckIn, Rating,
                   connect_to_db, db)
from server import app
from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)


def load_users():
    """Generate and load users into crapp database."""

    # Delete all rows in table to avoid duplicate data if run again
    User.query.delete()

    for i in range(30):
        # Generate fake name and email to create fake users
        name = fake.name()
        email = fake.email()
        user = User(full_name=name, email=email)

        # Add user to database session 
        db.session.add(user)

    # Commit new users to the database
    db.session.commit()
    print("Users Loaded")

def load_bathrooms():
    """Load bathroom data from api into crapp database."""
    # TODO: make a get request of all bathroom data
    # Load to or update in database

def load_named_lists():
    """Load initial named lists for all users to access."""
    # TODO: instanciate fave and least fave lists

def load_list_items():
    """Load list items for users' lists."""
    # TODO

def load_checkins():
    """Load checkins for fake users created with load_users."""
    # TODO

def load_ratings():
    """Load ratings for fake users created with load_users."""
    # TODO


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
