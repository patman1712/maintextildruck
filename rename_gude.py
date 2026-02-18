import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Rename 'gude' to 'home_text' and update related IDs
print("Renaming 'gude' to 'home_text'...")
c.execute("UPDATE sections SET id = 'home_text' WHERE id = 'gude'")
c.execute("UPDATE sections SET id = 'home_button_text' WHERE id = 'gude_button_text'")
c.execute("UPDATE sections SET id = 'home_button_link' WHERE id = 'gude_button_link'")

conn.commit()
conn.close()
