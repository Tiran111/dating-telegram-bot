mkdir dating_bot
cd dating_bot
# Створення файлів:
echo 'BOT_TOKEN = "8255438813:AAESXzuHdtuHbO18hpapcuat-e9fPPcD564"
ADMIN_IDS = [8330660486]' > config.py

echo 'import sqlite3
from contextlib import closing

def init_db():
    with closing(sqlite3.connect("dating.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            gender TEXT,
            city TEXT,
            bio TEXT,
            photo_id TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ad_text TEXT,
            ad_photo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )"")
        conn.commit()' > database.py

# Інші файли (bot.py, requirements.txt) скопіюйте аналогічно

# Архівація:
zip -r dating_bot.zip *
