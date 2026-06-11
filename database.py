import sqlite3

def get_db():

    conn = sqlite3.connect(
        "posts.db",
        check_same_thread=False
    )

    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        title TEXT,
        body TEXT,
        hashtags TEXT,
        image_prompt TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()

    return conn
