from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
import mysql.connector
from functools import wraps

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'beauty_recommender'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
                       (username, hashed_password, email))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/products', methods=['GET'])
@login_required
def get_products():
    category = request.args.get('category')
    type = request.args.get('type')
    concern = request.args.get('concern')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM products WHERE category = %s AND type = %s AND concern = %s"
    cursor.execute(query, (category, type, concern))
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(products)

@app.route('/api/review', methods=['POST'])
@login_required
def add_review():
    data = request.json
    user_id = session['user_id']
    rating = data['rating']
    comment = data.get('comment', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO reviews (user_id, rating, comment) VALUES (%s, %s, %s)", 
                       (user_id, rating, comment))
        conn.commit()
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)