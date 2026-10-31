import sqlite3, csv

def export_tables():
    conn = sqlite3.connect('database.db')
    for table in ('contacts','careers'):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        if rows:
            with open(f'{table}.csv','w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([d[0] for d in cursor.description])
                writer.writerows(rows)
            print(f'Wrote {len(rows)} rows to {table}.csv')
        else:
            print(f'No data in {table}')
    conn.close()

if __name__ == '__main__':
    export_tables()
