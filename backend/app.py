"""Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth # type: ignore
from dotenv import find_dotenv, load_dotenv # type: ignore
from flask import Flask, redirect, render_template, session, url_for, request, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy, MetaData, create_engine
from flask_cors import CORS # type: ignore
import cohere # type: ignore 

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
CORS(app)

co = cohere.Client(env.get("COHERE_API_KEY"))

app.config['SQLALCHEMY_DATABASE_URI']=='postgresql://food_g4ev_user:jsoLdTxhpbdK2SeTvJhExhXi9cwwbWjC@dpg-cu1c2kt2ng1s73ead920-a/food_g4ev'

db=SQLAlchemy(app)

class UserData(db.Model):
    date = db.Column(db.Integer, primary_key=True)
    mealtime = db.Column(db.String(20))
    food = db.Column(db.ARRAY(db.String(50)))
    medication_name = db.Column(db.ARRAY(db.String), nullable=True)
    medication_taken = db.Column(db.ARRAY(db.Bool), nullable=True)
    symptoms = db.Column(db.ARRAY(db.String(20)), nullable=True)

    def __init__(self, date, mealtime, food, medication_name=None, 
                 medication_taken=None, symptoms=None):
        self.date = date
        self.mealtime = mealtime
        self.food = food
        self.medication_name = medication_name
        self.medication_taken = medication_taken
        self.symptoms = symptoms

def create_user_table(user_id):
    """Dynamically create table for new user"""
    # Set table name for the user
    UserData.__table__.name = user_id
    
    # Check if table exists
    if not db.engine.dialect.has_table(db.engine, user_id):
        # Create table if it doesn't exist
        UserData.__table__.create(db.engine)
    
    return UserData

def submit(user_id, query_date):
    """Handle GET/POST requests for user data by date"""
    # Set correct table name
    UserData.__table__.name = user_id
    
    if request.method == 'GET':
        row = UserData.query.filter_by(date=query_date).first()
        if not row:
            new_entry = UserData(
                date=query_date,
            )
            
        return jsonify({
            'date': row.date,
            'mealtime': row.mealtime,
            'food': row.food,
            'medication_name': row.medication_name,
            'medication_taken': row.medication_taken,
            'symptoms': row.symptoms
        })

    if request.method == 'POST':
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('mealtime', 'food')):
            return jsonify({'error': 'Missing required fields'}), 400

        existing = UserData.query.filter_by(date=query_date).first()
        if existing:
            # Update existing record
            existing.mealtime = data['mealtime']
            existing.food = data['food']
            existing.medication_name = data.get('medication_name')
            existing.medication_taken = data.get('medication_taken')
            existing.symptoms = data.get('symptoms')
        else:
            # Create new record
            new_entry = UserData(
                date=query_date,
                mealtime=data['mealtime'],
                food=data['food'],
                medication_name=data.get('medication_name'),
                medication_taken=data.get('medication_taken'),
                symptoms=data.get('symptoms')
            )
            db.session.add(new_entry)

        try:
            db.session.commit()
            return jsonify({'message': 'Data saved successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        
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

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == "GET":
        return render_template('chat.html')
    user_message = request.json.get('message')
    
    # Call Cohere API to get a response
    response = co.generate(
        model='xlarge',
        prompt=user_message,
        max_tokens=50,
        temperature=0.6
    )
    
    bot_message = response.generations[0].text.strip()
    return jsonify({'response': bot_message})

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
      return render_template("dashboard.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
