import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                message TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS careers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                position TEXT
            )''')

conn.commit()
conn.close()
print("Database setup completed successfully!")