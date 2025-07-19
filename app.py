from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import json
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

# Import configurations
from config import DB_CONFIG, FLASK_CONFIG, LOGGING_CONFIG
import logging
import os

# Configure Flask app
app.secret_key = FLASK_CONFIG['SECRET_KEY']
app.config['DEBUG'] = FLASK_CONFIG['DEBUG']

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['LOG_LEVEL']),
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['LOG_FILE']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Database initialization
def init_db():
    try:
        # First, create database if not exists
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database')
        
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.close()
        
        # Now connect to the database
        conn = get_db_connection()
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default admin user if not exists
        cursor.execute('SELECT * FROM users WHERE username = %s', ('arifin123',))
        if not cursor.fetchone():
            password_hash = generate_password_hash('arifin 123')
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', 
                          ('arifin123', password_hash))
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
        
    except Error as e:
        print(f"Error initializing database: {e}")

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database
init_db()

# Data portfolio
portfolio_data = {
    "name": "Arifin",
    "title": "Full Stack Developer",
    "bio": "Passionate developer with expertise in Python, JavaScript, and modern web technologies. I love creating innovative solutions and beautiful user experiences.",
    "skills": [
        {"name": "Python", "level": 90, "icon": "🐍"},
        {"name": "JavaScript", "level": 85, "icon": "⚡"},
        {"name": "React", "level": 80, "icon": "⚛️"},
        {"name": "Flask", "level": 88, "icon": "🌶️"},
        {"name": "Database", "level": 75, "icon": "🗄️"},
        {"name": "UI/UX", "level": 70, "icon": "🎨"}
    ],
    "projects": [
        {
            "title": "E-Commerce Platform",
            "description": "Full-stack e-commerce solution with payment integration",
            "tech": ["Python", "Flask", "PostgreSQL", "Stripe API"],
            "status": "Completed",
            "image": "🛒"
        },
        {
            "title": "Task Management App",
            "description": "Real-time collaborative task management with notifications",
            "tech": ["React", "Node.js", "Socket.io", "MongoDB"],
            "status": "In Progress",
            "image": "📋"
        },
        {
            "title": "Weather Dashboard",
            "description": "Interactive weather dashboard with data visualization",
            "tech": ["Python", "Flask", "Chart.js", "OpenWeather API"],
            "status": "Completed",
            "image": "🌤️"
        }
    ],
    "contact": {
        "email": "mnarifin018@gmail.com",
        "github": "github.com/arifin32602200103",
        "linkedin": "linkedin.com/in/muhammad-nur-arifin-41316a191",
        "location": "Indonesia"
    }
}

@app.route('/')
def home():
    return render_template('index.html', data=portfolio_data)

@app.route('/api/skills')
def get_skills():
    return jsonify(portfolio_data['skills'])

@app.route('/api/projects')
def get_projects():
    return jsonify(portfolio_data['projects'])

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    
    try:
        # Simpan ke database
        conn = get_db_connection()
        if conn is None:
            return jsonify({'status': 'error', 'message': 'Gagal koneksi ke database'}), 500
            
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (name, email, message) 
            VALUES (%s, %s, %s)
        ''', (data.get('name'), data.get('email'), data.get('message')))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Pesan berhasil dikirim ke database!'})
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Gagal menyimpan pesan: {str(e)}'}), 500

@app.route('/api/theme', methods=['POST'])
def toggle_theme():
    # Endpoint untuk toggle dark/light mode
    return jsonify({'status': 'success'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn is None:
            flash('Gagal koneksi ke database!', 'error')
            return render_template('login.html')
            
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    if conn is None:
        flash('Gagal koneksi ke database!', 'error')
        return redirect(url_for('home'))
        
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, email, message, timestamp 
        FROM messages 
        ORDER BY timestamp DESC
    ''')
    messages = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', messages=messages)

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout!', 'info')
    return redirect(url_for('home'))

@app.route('/api/messages')
@login_required
def get_messages():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'status': 'error', 'message': 'Gagal koneksi ke database'}), 500
        
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, email, message, timestamp 
        FROM messages 
        ORDER BY timestamp DESC
    ''')
    messages = cursor.fetchall()
    conn.close()
    
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg[0],
            'name': msg[1],
            'email': msg[2],
            'message': msg[3],
            'timestamp': str(msg[4])  # Convert datetime to string for JSON
        })
    
    return jsonify(messages_list)

@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
@login_required
def delete_message(message_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'status': 'error', 'message': 'Gagal koneksi ke database'}), 500
            
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE id = %s', (message_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Pesan berhasil dihapus!'})
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Gagal menghapus pesan: {str(e)}'}), 500

if __name__ == '__main__':
    logger.info(f"Starting Flask application on {FLASK_CONFIG['HOST']}:{FLASK_CONFIG['PORT']}")
    app.run(
        debug=FLASK_CONFIG['DEBUG'],
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT']
    )