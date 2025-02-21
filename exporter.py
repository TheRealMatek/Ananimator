# Export sql lite table to csv

import sqlite3

def export_table_to_csv(table_name, csv_file):
    with sqlite3.connect('words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM {} ORDER BY original'.format(table_name))
        with open(csv_file, 'w') as f:
            f.write(','.join([description[0] for description in cursor.description]) + '\n')
            for row in cursor.fetchall():
                f.write(','.join(map(str, row)) + '\n')


export_table_to_csv('interesting', 'zanimive_besede.csv')
export_table_to_csv('palindromes', 'palindromi.csv')