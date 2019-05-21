"""Utility file to seed bathroom, user, and list data to crapp database""" 
import requests

from model import (User, Bathroom, NamedList, ListItem, Checkin, Rating,
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

    # Get request to get Response object with California bathrooms from refuge api
    # Will be used as initial seed data for bathrooms table in crapp database
    r = requests.get('https://www.refugerestrooms.org/api/v1/restrooms/search?page=1&per_page=100&offset=0&query=%22state%22:%22California%22')

    # Get list of dictionaries from request 
    bathrooms = r.json()

    # Delete all rows in table to avoid duplicate data if run again
    Bathroom.query.delete()

    # Make Bathroom object for each bathroom from request
    for bathroom in bathrooms:
        bathroom = Bathroom(name=bathroom['name'], directions=bathroom['directions'], notes=bathroom['comment'], 
                            state=bathroom['state'], city=bathroom['city'], country=bathroom['country'],
                            latitude=bathroom['latitude'], longitude=bathroom['longitude'], 
                            accessible=bathroom['accessible'], unisex=bathroom['unisex'],
                            changing_table=bathroom['changing_table'], approved=bathroom['approved'])
        
        # Add each Bathroom object that has lat/long to the database session
        if bathroom.latitude and bathroom.longitude:
            db.session.add(bathroom)                    
    # Commit added Bathroom objects to the database
    db.session.commit()
    print("Bathrooms Loaded")

def load_named_lists():
    """Load initial named lists for all users to access."""
    
    # Delete all rows in table to avoid duplicate data if run again
    NamedList.query.delete()

    # Create 2 default named lists to the database, favorites and shit list
    list1 = NamedList(list_name='Favorites')
    list2 = NamedList(list_name='Shit List')

    # Add default lists to the database session and commit to database
    db.session.add_all([list1, list2])
    db.session.commit()
    print("Named Lists Loaded")

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

    # Import data from load functions defined above 
    load_users()
    load_bathrooms()
    load_named_lists()
