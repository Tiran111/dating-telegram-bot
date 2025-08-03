import sqlite3
from contextlib import closing
from datetime import datetime

# Ініціалізація бази даних
def init_db():
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        
        # Таблиця користувачів
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            gender TEXT CHECK(gender IN ('чоловік', 'жінка', 'інше')),
            city TEXT,
            bio TEXT,
            photo_id TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_banned BOOLEAN DEFAULT FALSE
        )
        ''')
        
        # Таблиця оголошень
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ad_text TEXT NOT NULL,
            ad_photo TEXT,
            is_approved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        # Таблиця лайків
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            user_id INTEGER,
            liked_user_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, liked_user_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (liked_user_id) REFERENCES users(user_id)
        )
        ''')
        conn.commit()

# Користувачі
def add_user(user_id, username, first_name, last_name):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        conn.commit()

def update_profile(user_id, age, gender, city, bio, photo_id):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users 
        SET age = ?, gender = ?, city = ?, bio = ?, photo_id = ?
        WHERE user_id = ?
        ''', (age, gender, city, bio, photo_id, user_id))
        conn.commit()

def get_user(user_id):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

# Оголошення
def add_ad(user_id, ad_text, ad_photo=None):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO ads (user_id, ad_text, ad_photo)
        VALUES (?, ?, ?)
        ''', (user_id, ad_text, ad_photo))
        conn.commit()
        return cursor.lastrowid

def get_ads(approved_only=True):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        if approved_only:
            cursor.execute('SELECT * FROM ads WHERE is_approved = TRUE ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM ads ORDER BY created_at DESC')
        return cursor.fetchall()

def approve_ad(ad_id):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE ads SET is_approved = TRUE WHERE id = ?', (ad_id,))
        conn.commit()

# Пошук
def search_users(gender=None, city=None, age_min=18, age_max=100):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM users WHERE is_banned = FALSE'
        params = []
        
        if gender:
            query += ' AND gender = ?'
            params.append(gender)
        if city:
            query += ' AND city = ?'
            params.append(city)
        
        query += ' AND age BETWEEN ? AND ?'
        params.extend([age_min, age_max])
   database.py

        cursor.execute(query, params)
        return cursor.fetchall()

# Адмін-функції
def ban_user(user_id):
    with closing(sqlite3.connect('dating.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_banned = TRUE WHERE user_id = ?', (user_id,))
        conn.commit()

# Ініціалізуємо БД при імпорті
init_db()
