import sqlite3
import os

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Check if header_image exists
exists = c.execute("SELECT 1 FROM sections WHERE id = 'header_image'").fetchone()

if not exists:
    print("Adding header_image to database...")
    c.execute("INSERT INTO sections (id, content) VALUES (?, ?)", ('header_image', 'static/assets/cropped-f_frame-scaled-1.jpg'))
    conn.commit()
else:
    print("header_image already exists.")

conn.close()
