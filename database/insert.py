from database.db import get_connection

def insert_games(games):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS games (
        date TEXT,
        home TEXT,
        away TEXT,
        score TEXT
    )
    """)

    for g in games:
        cur.execute("INSERT INTO games VALUES (?, ?, ?, ?)",
                    (g["date"], g["home"], g["away"], g["score"]))

    conn.commit()
    conn.close()