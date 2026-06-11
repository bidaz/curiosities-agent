import sqlite3

def get_db():
    conn = sqlite3.connect("posts.db", check_same_thread=False)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        title TEXT,
        body TEXT,
        hashtags TEXT,
        image_prompt TEXT,
        image_url TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    # Falls Tabelle schon existiert, image_url nachträglich hinzufügen
    try:
        conn.execute("ALTER TABLE posts ADD COLUMN image_url TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    return conn
