import sqlite3

# Default content based on the screenshot
intro_text = """
<h2 style="color: #bd1026; font-weight: bold; text-transform: uppercase;">SO EINFACH GEHT’S</h2>
<h3>Der Bestellablauf in wenigen Schritten:</h3>
<p><strong>Bei uns das gewünschte Produkt in wenigen Schritten.</strong> Wir legen großen Wert auf individuelle und professionelle Beratung. Jeder Kunde bekommt einen festen Ansprechpartner, der Ihm mit Rat & Tag zur Seite steht. Ihre Bestellung erfolgt in diesen Schritten</p>
"""

step1_content = """
<div style="text-align: center;">
    <h1 style="color: #bd1026; font-size: 3rem; font-weight: bold;">1.</h1>
    <h3 style="color: #bd1026; font-weight: bold;">Anfragen</h3>
</div>
<p><strong>Was benötigen wir:</strong></p>
<ul style="list-style: none; padding-left: 0;">
    <li><i class="bi bi-check-circle"></i> Stückzahl</li>
    <li><i class="bi bi-check-circle"></i> Textilwunsch (T-Shirt, Hoodie, ...)</li>
    <li><i class="bi bi-check-circle"></i> Das Motiv als PDF, jpg oder tif</li>
</ul>
<p style="color: #bd1026; margin-top: 20px;">spätestens am nächsten Werktag erhalten Sie ein Angebot per Mail</p>
"""

step2_content = """
<div style="text-align: center;">
    <h1 style="color: #bd1026; font-size: 3rem; font-weight: bold;">2.</h1>
    <h3 style="color: #bd1026; font-weight: bold;">Bestätigen</h3>
</div>
<p><strong>Sie erhalten von uns:</strong></p>
<ul style="list-style: none; padding-left: 0;">
    <li><i class="bi bi-check-circle"></i> Druckvorschau / Preview</li>
    <li><i class="bi bi-check-circle"></i> Auftragsbestätigung</li>
    <li><i class="bi bi-check-circle"></i> Vorkassenrechnung</li>
</ul>
<p style="color: #bd1026; margin-top: 20px;">Ein Ansprechpartner wird sich von A-Z um Ihren Auftrag kümmern, ohne lange Wartezeiten.</p>
"""

step3_content = """
<div style="text-align: center;">
    <h1 style="color: #bd1026; font-size: 3rem; font-weight: bold;">3.</h1>
    <h3 style="color: #bd1026; font-weight: bold;">Fertig</h3>
</div>
<p><strong>Fertigstellung:</strong></p>
<ul style="list-style: none; padding-left: 0;">
    <li><i class="bi bi-check-circle"></i> Versand</li>
    <li><i class="bi bi-check-circle"></i> Abholung hier vor Ort</li>
</ul>
<p style="color: #bd1026; margin-top: 20px;">Durchschnittliche Produktionszeit, je nach Auftragsvolumen, beträgt 7-12 Werktage.</p>
"""

data = [
    ('service_intro_image', 'static/assets/kunden_ofc.jpg'), # Placeholder image existing in assets
    ('service_intro_text', intro_text),
    ('service_step_1', step1_content),
    ('service_step_2', step2_content),
    ('service_step_3', step3_content)
]

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.executemany('INSERT OR IGNORE INTO sections (id, content) VALUES (?, ?)', data)
conn.commit()
conn.close()
print("Service-Steps zur Datenbank hinzugefügt.")
