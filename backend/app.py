"""Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth # type: ignore
from dotenv import find_dotenv, load_dotenv # type: ignore
from flask import Flask, redirect, render_template, session, url_for, request # type: ignore

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

@app.route('/')
def home():
    return redirect(url_for('main_home'))

@app.route('/home')
def main_home():
    return render_template('index.html')

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/dashboard")

@app.get("/dashboard")
def dashboard():
	if request.args:
		pass
	else:
		pass
	return render_template("dashboard.html", breakkies=["Cereal", "Burrito", "Pasta"], syms=["Nausea"])

# Add these routes to your Flask application
from flask import jsonify, request

@app.route('/add_medication', methods=['POST'])
def add_medication():
    data = request.json
    medication = data.get('medication')
    
    try:
        # Add your database logic here
        # For example: db.add_medication(medication)
        return jsonify({'success': True, 'message': 'Medication added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/remove_medication', methods=['POST'])
def remove_medication():
    data = request.json
    medication = data.get('medication')
    
    try:
        # Add your database logic here
        # For example: db.remove_medication(medication)
        return jsonify({'success': True, 'message': 'Medication removed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/about-us')
def about():
    return render_template('about-us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)