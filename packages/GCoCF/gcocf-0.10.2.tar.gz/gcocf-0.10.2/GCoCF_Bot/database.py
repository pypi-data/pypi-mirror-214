import sqlite3
from typing import Optional, Tuple


DB_NAME = "service_bot.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            player_token TEXT NOT NULL,
            player_tag TEXT NOT NULL,
            webhook_url TEXT NOT NULL,
            clan_tag TEXT NOT NULL,
            instance_count INTEGER NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS whitelist (
            user_id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()

async def is_user_whitelisted(user_id: int) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM whitelist WHERE user_id=?", (user_id,))
        return cursor.fetchone() is not None
    
async def add_user_to_whitelist(target_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO whitelist (user_id) VALUES (?)", (target_id,))
        conn.commit()

async def store_user_data(user_id: int, player_token: str, player_tag: str, webhook_url: str, clan_tag: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            player_token TEXT NOT NULL,
            player_tag TEXT NOT NULL,
            webhook_url TEXT NOT NULL,
            clan_tag TEXT NOT NULL,
            instance_count INTEGER NOT NULL
        )
    """)

    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_data = c.fetchone()
    if user_data is None:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, 0)", (user_id, player_token, player_tag, webhook_url, clan_tag))
    else:
        c.execute("UPDATE users SET player_token=?, player_tag=?, webhook_url=?, clan_tag=? WHERE user_id=?", (player_token, player_tag, webhook_url, clan_tag, user_id))

    conn.commit()
    conn.close()

async def get_user_data(user_id: int) -> Optional[Tuple[int, str, str, str, str, int]]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT user_id, player_token, player_tag, webhook_url, clan_tag, instance_count FROM users WHERE user_id=?", (user_id,))
    user_data = c.fetchone()

    conn.close()

    return user_data

async def update_instance_count(user_id: int, count: int):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("UPDATE users SET instance_count=? WHERE user_id=?", (count, user_id))

    conn.commit()
    conn.close()