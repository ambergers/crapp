"""Flask app for crApp project."""
import json
import requests

from flask import (Flask, render_template, redirect, jsonify, request, flash, 
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, get_bathrooms_by_lat_long,
                   get_bathroom_objs_from_request, User, Bathroom)


app = Flask(__name__)
# This is only temporary, will change later
app.secret_key = 'SUpeRsecrEt'

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/register', methods=["GET"])
def display_reg_page():
    """Send to reg page """

    return render_template('reg-form.html')

@app.route('/register', methods=["POST"])
def process_reg():
    """Process registration and redirect to homepage."""

    # Retrieve variables from form and set to variables
    user_full_name = request.form.get("full_name")
    user_email = request.form.get("email")
    user_pswd = request.form.get("password")

    # Try to get user from db, create user if not in db
    try:
        user_obj = User.query.filter_by(email=user_email, 
                                        password=user_pswd).one()
        flash("You're already registered. Go ahead and log in!")
    except:
        user_obj = User(full_name=user_full_name, email=user_email, password=user_pswd)
        db.session.add(user_obj)
        db.session.commit()
        flash("You're now registered! Go ahead an log in.")

    # Redirect to homepage
    return redirect("/")

@app.route("/login")
def display_login():
    return render_template('login-page.html')

@app.route("/login-process", methods=["POST"])
def process_login():
    #retrieve email and password from login-form
    user_email = request.form.get("email")
    password = request.form.get("password")

    try:
        #check to see if user in db by email 
        #if password matches, query database, retrieve user id and add to session
        user_obj = User.query.filter_by(email=user_email, password=password).one()
        session['user_id'] = user_obj.user_id
        flash("Good job! You're logged in!!!")
        url = "/users/" + str(session['user_id'])
        return redirect(url)
        
    except:
        flash("Uh oh! Password/email address is incorrect. It's okay...you can try again")
        return redirect("/login")

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user_id', None)
   flash("You're logged out. Cool.")
   return redirect("/")

@app.route('/get_near_me.json')
def get_near_me():
    """Get bathrooms near user location using python."""

    current_lat = request.args.get("lat")
    current_long = request.args.get("lng")
    
    near_bathrooms_request = get_bathrooms_by_lat_long(current_lat, current_long)
    near_bathrooms_list = near_bathrooms_request.json()

    return jsonify(near_bathrooms_list)

@app.route('/users/<user_id>')
def user_info(user_id):
    """Show user info"""

    #Get/query user object with user id
    user = User.query.get(user_id)

    #Send particular attributes to template
    return render_template('user_hub.html', user=user)

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
