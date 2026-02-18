import sqlite3

data = [
    ('site_logo', 'static/assets/new_logo.png'),
    ('primary_color', '#bd1026')
]

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.executemany('INSERT OR IGNORE INTO sections (id, content) VALUES (?, ?)', data)
conn.commit()
conn.close()
print("Design-Einstellungen zur Datenbank hinzugefügt.")
