# Connect to db, fo

import sqlite3
from contextlib import closing

with closing(sqlite3.connect('words.db')) as conn:
    cursor = conn.cursor()
    # Create table of palindromes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS palindromes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT NOT NULL,
        reversed TEXT NOT NULL
    )
    ''')
    # Select only palindromes
    cursor.execute('''
    SELECT DISTINCT original, reversed
    FROM dictionary
    WHERE both_words = 1 AND original = reversed AND LENGTH(original) > 2 AND GLOB('*[a-z]*', original)
    ''')
    rows = cursor.fetchall()
    # First clear the table
    cursor.execute('DELETE FROM palindromes')
    # Insert the rows
    cursor.executemany('INSERT INTO palindromes (original, reversed) VALUES (?, ?)', rows)
    
    conn.commit()

