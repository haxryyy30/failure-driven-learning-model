import sqlite3

def connect_db():

    conn = sqlite3.connect("failures.db")

    return conn

def create_table():

    conn = connect_db()

    cursor = conn.cursor()

    # USERS TABLE

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT

    )

    """)

    # FAILURES TABLE

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS failures (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        error_message TEXT,

        module_name TEXT,

        severity TEXT,

        predicted_cause TEXT,

        solution TEXT,
                   
        confidence INTEGER,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()