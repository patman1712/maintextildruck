
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Insert default values for WhatsApp
cursor.execute("INSERT OR IGNORE INTO sections (id, content) VALUES ('whatsapp_number', '4915735508068')")
cursor.execute("INSERT OR IGNORE INTO sections (id, content) VALUES ('whatsapp_initial_text', 'Hello')")
cursor.execute("INSERT OR IGNORE INTO sections (id, content) VALUES ('whatsapp_label', 'Frage offen? Schreib uns auf WhatsApp!')")

conn.commit()
conn.close()
print("Initialized WhatsApp database entries.")
