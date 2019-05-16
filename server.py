"""Flask app for crApp project."""

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db


app = Flask(__name__)
# This is only temporary, will change later
app.secret_key = 'SUpeRsecrEt'

@app.route('/')
def homepage():
    """Show homepage."""

    # TODO: make homepage.html
    return render_template('homepage.html')

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port="5001")
