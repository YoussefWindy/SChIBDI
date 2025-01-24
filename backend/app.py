import json, datetime, atexit
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth # type: ignore
from dotenv import find_dotenv, load_dotenv # type: ignore
from flask import Flask, redirect, render_template, session, url_for, request, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import create_engine # type: ignore
from flask_cors import CORS # type: ignore
from psycopg2 import pool, sql # type: ignore


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
CORS(app, supports_credentials=True)

oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

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
            cur.execute(
                sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(sql.Identifier(str(user_id)), sql.SQL(', ').join(
                        sql.SQL("{} {}").format(sql.Identifier(k), sql.SQL(v)) for k, v in UserData.DAILY_SCHEMA.items())))
            cur.execute(sql.SQL("SELECT * FROM {} WHERE date = {}").format(sql.Identifier(str(user_id)), sql.Literal(query_date)))
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
            cur.execute("""
                INSERT INTO profiles (id, name, age, type)
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
            """, (str(user_id), "", 0, ""))
            cur.execute("SELECT * FROM profiles WHERE id = %s", [str(user_id)])
            row = cur.fetchone()
            if row is None:
                return (None, None, None) # if this is reached then something went wrong
            return row
    finally:
        settings_pool.putconn(conn)

def get_meds_info(user_id, num_meds=False):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            if num_meds:
                cur.execute(sql.SQL("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)"), [str(user_id)])
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    return None
                cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(str(user_id))))
                ret = cur.fetchone()
                return ret[0]
            cur.execute(
                sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(sql.Identifier(str(user_id)), sql.SQL(', ').join(
                    sql.SQL("{} {}").format(sql.Identifier(k), sql.SQL(v)) for k, v in UserData.MEDS_SCHEMA.items())))
            cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(str(user_id))))
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
            cur.execute("SELECT * FROM chat_history WHERE id = %s", [str(user_id)])
            return cur.fetchall()
    finally:
        settings_pool.putconn(conn)

# Make this function more efficient, let's not delete everything every time?
def update_daily_data(user_id, query_date, mealtime, food, meds_taken, symptoms):
    conn = daily_pool.getconn()
    try:
        with conn.cursor() as cur:
            # Delete existing data for the given date
            cur.execute(sql.SQL("DELETE FROM {} WHERE date = %s").format(sql.Identifier(str(user_id))), [query_date])            
            # Insert new data
            cur.execute(sql.SQL("""
                INSERT INTO {} (date, mealtime, food, meds_taken, symptoms) VALUES (%s, %s, %s, %s, %s)"""
            ).format(sql.Identifier(str(user_id))), (query_date, mealtime, food, meds_taken, symptoms))
            conn.commit()
    finally:
        daily_pool.putconn(conn)

# Make this function more efficient, let's not delete everything every time?
def update_meds_info(user_id, med_name, med_times):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
                    sql.Identifier(str(str(user_id))),
                    sql.SQL(', ').join(
                        sql.SQL("{} {}").format(sql.Identifier(k), sql.SQL(v)) for k, v in UserData.MEDS_SCHEMA.items()
                    )
                )
            )
            # Delete existing data
            cur.execute("DELETE FROM {} WHERE med_name = %s".format(sql.Identifier(str(user_id))), (med_name,))
            # Insert new data
            cur.execute(sql.SQL("INSERT INTO {} (med_name, med_times) VALUES (%s, %s)").format(
                sql.Identifier(str(user_id))), (med_name, med_times))
            conn.commit()
    finally:
        settings_pool.putconn(conn)

def update_user_settings(user_id, name, age, type):
    conn = settings_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO profiles (id, name, age, type)
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE
                SET name = EXCLUDED.name, age = EXCLUDED.age, type = EXCLUDED.type
            """, (str(user_id), name, age, type))
            conn.commit()
    finally:
        settings_pool.putconn(conn)

@app.route('/')
def home():
    return redirect(url_for('main_home'))


@app.route('/home')
def main_home():
    return render_template('index.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == "GET":
        return render_template('chat.html')
    user_message = request.json.get('message')

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
        token = auth0.authorize_access_token()
        # app.logger.info(token)
        # app.logger.info("HELLOHELLO THIS HAS BEEN REACHED")
        session['user_info'] = token
        # app.logger.info("WOWOWOWOWOWW")
        # app.logger.info(user_id)
        if not token:
            return redirect("/login")
        return redirect("/dashboard")
    except Exception:
        return redirect("/login")

@app.route("/profile")
def profile():
    if session.__sizeof__ == 0 or session['user_info'] is None:
        return redirect("/login")
    user_id = parse(session['user_info']['userinfo']['sub'])
    if request.method == "GET":
        user_data = get_user_settings(user_id)
        return render_template("profile.html", user_data=user_data)
    elif request.method == "POST":
        data = request.json
        name = data["name"]
        age = data["age"]
        type = data["type"]
        update_user_settings(user_id, name, age, type)
    
def parse(user_info):
    return int(user_info.split('|')[1], 16)

known_users = open("known_users.txt").read().split("\n")

@app.get("/dashboard")
def dashboard():
    if session.__sizeof__ == 0 or session['user_info'] is None:
        return redirect("/login")
    user_id = parse(session['user_info']['userinfo']['sub'])
    if user_id not in known_users:
        known_users.append(user_id)
        update_user_settings(user_id, session['user_info']['userinfo']['nickname'], 0, "")
    # if request.args: # why is this here?
    #     pass
    if request.method == "GET":
        meds_info = get_meds_info(user_id)
        daily_data = get_daily_data(user_id, datetime.date.today())
        food_data = daily_data[2]
        breakkies = []
        lunchies = []
        dinnies = []
        snackies = []
        for i in range(len(food_data)):
            match daily_data[1]:
                case "breakfast":
                    breakkies.append(food_data[i])
                case "lunch":
                    lunchies.append(food_data[i])
                case "dinner":
                    dinnies.append(food_data[i])
                case "snack":
                    snackies.append(food_data[i])
        
        meds_array = [[] for _ in range(len(meds_info))]

        #name if time
        for i in range(len(meds_info)):
            for j in range(4):
                if (meds_info[1][j] == True):
                    meds_array[0].append(meds_info[i][0])
                    meds_array[i][2] = j
                    if (daily_data[3] == True):
                        meds_array[i][3] = True
                    else:
                        meds_array[i][3] = False

        syms = daily_data[4]
        
        return render_template("dashboard.html", breakkies=breakkies, lunchies=lunchies, dinnies=dinnies, snackies=snackies, meds=meds_array, syms=syms)
    else:
        pass
    data = request.json
    if data["medication"]:
        meds_array = data["meds"]
        # Insert DB integration here
        med_names = []
        med_times = []
        for i in range(len(meds_array[0])):
            for j in range(4):
                if (meds_array[1][j] == True):
                    med_names.append(meds_array[i][0])
                    med_times.append(meds_array[i][2])
        update_meds_info(parse(session['user_info']['userinfo']['sub']), med_names, med_times)
    else:
        breakfast = data["meals"]["breakfast"]
        lunch = data["meals"]["lunch"]
        dinner = data["meals"]["dinner"]
        snacks = data["meals"]["snack"]
        meds_info = data["meds"]
        symptoms = data["symptoms"]
        food_data = []
        food_times = []
        for i in range(len(breakfast)):
            food_data.append(breakfast[i])
            food_times.append([True, False, False, False])
        for i in range(len(lunch)):
            food_data.append(lunch[i])
            food_times.append([False, True, False, False])
        for i in range(len(dinner)):
            food_data.append(dinner[i])
            food_times.append([False, False, True, False])
        for i in range(len(snacks)):
            food_data.append(snacks[i])
            food_times.append([False, False, False, True])
        
        update_daily_data(parse(session['user_info']['userinfo']['sub']), 
                          datetime.date.today(), 
                          data["mealtime"], 
                          meds_info[1], 
                          food_data, 
                          symptoms)

        # Insert DB integration here

# I don't know why these two below ones were made, remove them when sure they are not needed

# @app.route('/add_medication', methods=['POST'])
# def add_medication():
#     data = request.json
#     medication = data.get('medication')
    
#     try:
#         # Add your database logic here
#         # For example: db.add_medication(medication)
#         return jsonify({'success': True, 'message': 'Medication added successfully'})
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# @app.route('/remove_medication', methods=['POST'])
# def remove_medication():
#     data = request.json
#     medication = data.get('medication')
    
#     try:
#         # Add your database logic here
#         # For example: db.remove_medication(medication)
#         return jsonify({'success': True, 'message': 'Medication removed successfully'})
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/about-us')
def about():
    return render_template('about-us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def cleanup():
    daily_pool.closeall()
    settings_pool.closeall()
    f = open("known_users.txt", "w")
    f.write("\n".join(known_users))

atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug=True)