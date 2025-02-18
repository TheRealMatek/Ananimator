import xml.etree.ElementTree as ET
import sqlite3
from contextlib import closing



with closing(sqlite3.connect('words.db')) as conn:
    with closing(conn.cursor()) as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dictionary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original TEXT NOT NULL,
            reversed TEXT NOT NULL,
            both_words INTEGER NOT NULL
        )
        ''')

        word_limit = 1000000000

        # Open the original and output files
        with open('accented_sloleks2.xml', 'rb') as input_file:
            context = ET.iterparse(input_file, events=('start', 'end'))
            _, root = next(context)
            counter = 0

            words_to_insert = []

            for event, elem in context:
                if elem.tag == 'feat' and elem.get('att') == 'zapis_oblike':
                    counter += 1
                    attribute_value = elem.get('val').lower()
                    if attribute_value:
                        words_to_insert.append((attribute_value, attribute_value[::-1]))
                        if counter % 300000 == 0:
                            print(f'Processed {counter} elements')
                            cursor.execute('BEGIN TRANSACTION')
                            cursor.executemany('INSERT INTO dictionary (original, reversed, both_words) VALUES (?, ?, 0)', words_to_insert)
                            # Commit transaction
                            conn.commit()
                            words_to_insert = []
                elem.clear()

        print(f'Processing complete. Total elements processed: {counter}')