# Connect to db, fo

import sqlite3
from contextlib import closing

with closing(sqlite3.connect('words.db')) as conn:
    cursor = conn.cursor()
    # Select only interesting rows
    cursor.execute('''
    SELECT DISTINCT CASE WHEN original < reversed THEN original ELSE reversed END AS original,
    CASE WHEN original < reversed THEN reversed ELSE original END AS reversed
    FROM dictionary
    WHERE both_words = 1 AND original != reversed AND LENGTH(original) > 2 AND GLOB('*[a-z]*', original)
    ''')
    rows = cursor.fetchall()
    # Write to a new table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interesting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT NOT NULL,
        reversed TEXT NOT NULL
    )
    ''')

    # First clear the table
    cursor.execute('DELETE FROM interesting')
    # Insert the rows
    cursor.executemany('INSERT INTO interesting (original, reversed) VALUES (?, ?)', rows)
    conn.commit()

