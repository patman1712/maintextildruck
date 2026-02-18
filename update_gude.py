import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Content from the frontend
gude_content = """<h1 class="site-title"><a href="#about" target="_self">Ai [gu:&#039;dǝ] wie!</a></h1>
<p class="site-description">Direkt an der Kultstätte Bieberer Berg in Offenbach sind wir dein Ansprechpartner für hochwertigen Textildruck und kreatives Merchandise.
Ob Brand, Firma, Musiker oder Verein – wir gestalten, veredeln und produzieren genau das, was zu dir passt...</p>"""

# Update 'gude' content
print("Updating 'gude' content...")
c.execute("UPDATE sections SET content = ? WHERE id = 'gude'", (gude_content,))

# Add gude button fields if they don't exist
new_sections = [
    ('gude_button_text', 'Wir setzen DICH richtig in Szene!'),
    ('gude_button_link', '#about')
]

for section_id, content in new_sections:
    exists = c.execute("SELECT 1 FROM sections WHERE id = ?", (section_id,)).fetchone()
    if not exists:
        print(f"Adding {section_id} to database...")
        c.execute("INSERT INTO sections (id, content) VALUES (?, ?)", (section_id, content))
    else:
        print(f"Updating {section_id}...")
        c.execute("UPDATE sections SET content = ? WHERE id = ?", (content, section_id))

conn.commit()
conn.close()
