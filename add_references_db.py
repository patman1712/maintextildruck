import sqlite3

widget_code = """<script src="static/assets/lightwidget.js"></script><iframe src="https://cdn.lightwidget.com/widgets/b18794f24f07585e9ba593ac61842bea.html" scrolling="no" allowtransparency="true" class="lightwidget-widget" style="width:100%;border:0;overflow:hidden;"></iframe>"""

data = [
    ('references_subtitle', 'Von der Idee bis zum fertigen Produkt!'),
    ('references_title', 'GUDE REFERENZEN'),
    ('instagram_widget', widget_code)
]

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.executemany('INSERT OR IGNORE INTO sections (id, content) VALUES (?, ?)', data)
conn.commit()
conn.close()
print("Referenzen-Daten hinzugefügt.")
