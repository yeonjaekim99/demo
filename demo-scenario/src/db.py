import sqlite3

DB_PATH = "app.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            author_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def find_user_by_username(username: str):
    conn = get_connection()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    user = conn.execute(query).fetchone()
    conn.close()
    return dict(user) if user else None


def search_posts(keyword: str):
    conn = get_connection()
    query = f"SELECT * FROM posts WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"
    posts = conn.execute(query).fetchall()
    conn.close()
    return [dict(p) for p in posts]


def create_user(username: str, password: str, email: str):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (username, password, email),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def create_post(title: str, content: str, author_id: int):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
        (title, content, author_id),
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id


def get_all_posts():
    conn = get_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(p) for p in posts]


def get_all_users():
    conn = get_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]


def delete_user(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


init_db()
