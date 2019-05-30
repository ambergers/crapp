"""Flask app for crApp project."""
import json

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, get_bathrooms_by_lat_long,
                   get_bathroom_objs_from_request)


app = Flask(__name__)
# This is only temporary, will change later
app.secret_key = 'SUpeRsecrEt'

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/get_near_me.json')
def get_near_me():
    """Get bathrooms near user location using python."""

    current_lat = 37.788934
    current_long = -122.411241
    
    near_bathrooms_request = get_bathrooms_by_lat_long(current_lat, current_long)
    near_bathrooms_list = near_bathrooms_request.json()
    near_bathrooms_json = json.dumps(near_bathrooms_list)

    return near_bathrooms_json

@app.route('/near_me')
def display_near_me():
    """Show map with bathrooms near user's location."""
    
    current_lat = 37.788934
    current_long = -122.411241
    
    near_bathroom_request = get_bathrooms_by_lat_long(current_lat, current_long)
    near_bathrooms = get_bathroom_objs_from_request(near_bathroom_request)

    return render_template('homepage.html', near_bathrooms=near_bathrooms)

@app.route('/lists')
def user_lists():
    """Show User's lists."""

    #TODO: Make user's list page
    return render_template('user_lists.html')

@app.route('/checkins')
def user_checkins():
    """Show User's checkins."""

    #TODO: Make user's checkins page
    return render_template('user_checkins.html')

@app.route('/ratings')
def user_ratings():
    """Show User's checkins."""

    #TODO: Make user's ratings page
    return render_template('user_ratings.html')

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port="5001")
