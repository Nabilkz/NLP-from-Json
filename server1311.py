from flask import Flask, request, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    password_hash = generate_password_hash(password)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
    db.commit()
    return 'User registered'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    row = cursor.fetchone()
    if row and check_password_hash(row[0], password):
        return 'Login successful'
    else:
        return 'Invalid username or password'

@app.route('/send_data', methods=['POST'])
def send_data():
    input_1 = request.form['input']
    user_id = request.form['user_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO data (user_id, input) VALUES (?, ?)', (user_id, input_1))
    db.commit()
    return input_1
@app.route('/get_data', methods=['POST'])
def get_data():
    global input1
    input1 = request.form['output']
    print(input1)
    return input1
@app.route('/get_sent_data', methods=['GET'])
def get_sent_data():
    global input1
    user_id = request.args.get('user_id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT input FROM data WHERE user_id=? ORDER BY id DESC LIMIT 1', (user_id,))
    row = cursor.fetchone()
    if row:
        return input1
    else:
        return ''

if __name__ == '__main__':
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, input TEXT)')
        db.commit()
    app.run()
