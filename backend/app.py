from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)


# Initialize the SQLite database
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Challenges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                difficulty INTEGER NOT NULL
            )
        ''')
        # User challenges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                challenge_id INTEGER NOT NULL,
                start_date DATE NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(challenge_id) REFERENCES challenges(id)
            )
        ''')
        conn.commit()

# Add a signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        try:
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                          (username, hashed_password))
            conn.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Username already exists'}), 409
        
@app.route('/assign_challenges', methods=['POST'])
def assign_challenges():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user_id = user[0]
        # Assign 21 days of challenges
        start_date = datetime.now().date()
        for day in range(21):
            challenge_date = start_date + timedelta(days=day)
            difficulty = (day // 7) + 1  # Increase difficulty each week
            cursor.execute('SELECT id FROM challenges WHERE difficulty = ?', (difficulty,))
            challenge = cursor.fetchone()
            if challenge:
                challenge_id = challenge[0]
                cursor.execute('''
                    INSERT INTO user_challenges (user_id, challenge_id, start_date)
                    VALUES (?, ?, ?)
                ''', (user_id, challenge_id, challenge_date))
        conn.commit()

    return jsonify({'message': 'Challenges assigned successfully'}), 201

@app.route('/get_challenges', methods=['GET'])
def get_challenges():
    username = request.args.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user_id = user[0]
        # Get challenges for the user
        cursor.execute('''
            SELECT c.description, uc.start_date, uc.completed
            FROM user_challenges uc
            JOIN challenges c ON uc.challenge_id = c.id
            WHERE uc.user_id = ?
            ORDER BY uc.start_date
        ''', (user_id,))
        challenges = cursor.fetchall()

    return jsonify([
        {'description': row[0], 'start_date': row[1], 'completed': bool(row[2])}
        for row in challenges
    ]), 200

@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    username = data.get('username')
    challenge_date = data.get('challenge_date')

    if not username or not challenge_date:
        return jsonify({'message': 'Username and challenge date are required'}), 400

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user_id = user[0]
        # Update challenge progress
        cursor.execute('''
            UPDATE user_challenges
            SET completed = 1
            WHERE user_id = ? AND start_date = ?
        ''', (user_id, challenge_date))
        conn.commit()

    return jsonify({'message': 'Progress updated successfully'}), 200

CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    init_db()
    app.run(debug=True)