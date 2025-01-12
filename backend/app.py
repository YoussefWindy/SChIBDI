"""Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import datetime

from authlib.integrations.flask_client import OAuth # type: ignore
from dotenv import find_dotenv, load_dotenv # type: ignore
from flask import Flask, redirect, render_template, session, url_for, request, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import create_engine # type: ignore
from flask_cors import CORS # type: ignore
import cohere # type: ignore
from psycopg2 import pool # type: ignore


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
CORS(app)

co = cohere.Client(env.get("COHERE_API_KEY"))

DB_PARAMS = {
    'user': 'bradley',
    'password': 'Spine',
    'host': '142.186.153.219',
    'port': '5432'
}

# Create separate pools for each database
daily_pool = pool.SimpleConnectionPool(
    1, 4,
    database='user_daily',
    **DB_PARAMS
)

settings_pool = pool.SimpleConnectionPool(
    1, 4,
    database='user_settings',
    **DB_PARAMS
)
class UserData:
    DAILY_SCHEMA = {
        'date': 'DATE NOT NULL PRIMARY KEY',
        'mealtime': 'VARCHAR(20)',
        'food': 'VARCHAR(50)[]',
        'symptoms': 'VARCHAR(20)[]',
        'medication_taken': 'BOOLEAN[]'
    }
    
    SETTINGS_SCHEMA = {
        'id': 'VARCHAR(120) UNIQUE',
        'name': 'VARCHAR(100)',
        'age' : 'INTEGER',
        'type': 'VARCHAR(100)',
    }
    
    MEDS_SCHEMA = {
        # Medication settings, table has id of the user.
        'medication_name': 'VARCHAR(50)',
        'medication_time': 'BOOLEAN[]',
    }

    def __init__(self, date, mealtime, food, medication_taken=None, symptoms=None):
        self.date = date
        self.mealtime = mealtime
        self.food = food
        self.medication_taken = medication_taken
        self.symptoms = symptoms

def get_daily_data(user_id, query_date):
    conn = daily_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT date, mealtime, food, symptoms 
                FROM {user_id}  
                WHERE date = %s
            """, (query_date,))  # Added missing comma for single-item tuple
            row = cur.fetchone()
            
            if row is None:
                # Return default empty values if no row found
                return (query_date, "", [], [])
            return row
    finally:
        daily_pool.putconn(conn)

def get_user_settings(user_id):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT *
                FROM profiles
                WHERE id = %s
            """, (user_id,)) # Added missing comma for single-item tuple
            row = cur.fetchone()
            
            if row is None:
                return (None, None, None)
            return row
    finally:
        settings_pool.putconn(conn)

def get_meds_info(user_id, num_meds=False):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            if (num_meds):
                cur.execute(f"""
                    SELECT COUNT(*)
                    FROM {user_id}
                """)
                ret = cur.fetchone()
                return ret[0]
            cur.execute(f"""
                SELECT *
                FROM {user_id}
            """)
            ret = cur.fetchall()
            
            if ret is None:
                return [None, None]
            return ret
    finally:
        settings_pool.putconn(conn)

def get_chat_history(user_id):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT *
                FROM chat_history
                WHERE id = %s
            """, (user_id,))
            ret = cur.fetchall()
            
            return ret
    finally:
        settings_pool.putconn(conn)

def create_daily_table(username):
    conn = daily_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {username} (
                    {', '.join([f'{k} {v}' for k, v in UserData.DAILY_SCHEMA.items()])}
                )
            """)
    finally:
        daily_pool.putconn(conn)

def create_user_table(user_id):
    """Dynamically create table for new user"""
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {user_id} (
                    {', '.join([f'{k} {v}' for k, v in UserData.SETTINGS_SCHEMA.items()])}
                )
            """)
    finally:
        settings_pool.putconn(conn)

def update_daily_data(user_id, query_date, mealtime, food, symptoms):
    conn = daily_pool.getconn()
    try:
        with conn.cursor() as cur:
            # Delete existing data for the given date
            cur.execute(f"""
                DELETE FROM {user_id}
                WHERE date = %s
            """, query_date)
            
            # Insert new data
            cur.execute(f"""
                INSERT INTO {user_id} (date, mealtime, food, symptoms)
                VALUES (%s, %s, %s, %s)
            """, query_date, mealtime, food, symptoms)
            conn.commit()
    finally:
        daily_pool.putconn(conn)

def update_meds_info(user_id, med_name, med_times):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            # Delete existing data
            cur.execute(f"""
                DELETE * FROM {user_id}
            """, med_name)
            
            # Insert new data
            cur.execute(f"""
                INSERT INTO {user_id} (med_name, med_times)
                VALUES (%s, %s)
            """, med_name, med_times)
            conn.commit()
    finally:
        settings_pool.putconn(conn)

def update_user_settings(user_id, name, age, type):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO profiles (id, name, age, type)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (user_id, name, age, type))
            conn.commit()
    finally:
        settings_pool.putconn(conn)

# def submit(user_id, query_date):
#     """Handle GET/POST requests for user data by date"""
#     # Set correct table name
#     UserData.__table__.name = user_id
    
#     if request.method == 'GET':
#         row = get_daily_data(user_id, query_date)
#         if not row:
#             new_entry = UserData(date=query_date)

#         return jsonify({
#             'date': row.date,
#             'mealtime': row.mealtime,
#             'food': row.food,
#             'medication_name': row.medication_name,
#             'medication_taken': row.medication_taken,
#             'symptoms': row.symptoms
#         })

#     if request.method == 'POST':
#         data = request.get_json()
        

#         if existing:
#             # Update existing record
#             existing.mealtime = data['mealtime']
#             existing.food = data['food']
#             existing.medication_name = data.get('medication_name')
#             existing.medication_taken = data.get('medication_taken')
#             existing.symptoms = data.get('symptoms')
#         else:
#             # Create new record
#             new_entry = UserData(
#                 date=query_date,
#                 mealtime=data['mealtime'],
#                 food=data['food'],
#                 medication_name=data.get('medication_name'),
#                 medication_taken=data.get('medication_taken'),
#                 symptoms=data.get('symptoms')
#             )
        
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
    try:
        token = oauth.auth0.authorize_access_token()
        if not token:
            return redirect("/login")
        session["user"] = token
        return redirect("/dashboard")
    except Exception as e:
        return redirect("/login")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    #redirect to login if not logged in 
    if "user" not in session:
        return redirect(url_for("login"))
    user_id = session.get("user", {}).get("sub")
    if not user_id:
        session.clear()
        return redirect(url_for("login"))
    if request.args:
        query_date = request.args.get('date')
        return get_daily_data(user_id, query_date)
    if request.method == "GET":
        user_id = session.get("user", {}).get("sub")
        user_data = get_user_settings(user_id)
        meds_info = get_meds_info(user_id)
        daily_data = get_daily_data(user_id, datetime.date.today())
        return render_template("dashboard.html", user_data=user_data, meds_info=meds_info, daily_data=daily_data)
    else:
        pass

if __name__ == '__main__':
    app.run(debug=True)
