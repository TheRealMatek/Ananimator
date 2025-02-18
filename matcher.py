# Connect to db, fo

import sqlite3
from contextlib import closing

with closing(sqlite3.connect('words.db')) as conn:
    cursor = conn.cursor()
    # Update the both_words column to 1 if reverse_word exists in the word column
    cursor.execute('''
    UPDATE dictionary
    SET both_words = 1
    WHERE reversed IN (SELECT original FROM dictionary)
    ''')
    conn.commit()

