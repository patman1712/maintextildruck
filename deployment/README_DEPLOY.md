
# Deployment bei All-Inkl.com

Es ist **machbar**, aber etwas aufwändiger als bei einer reinen HTML-Seite. Hier ist der grobe Ablauf:

1. **Dateien hochladen:** Lade alle Projektdateien per FTP hoch (z.B. in einen Unterordner `fanshop`).
2. **Datenbank:** Die `database.db` Datei muss hochgeladen werden und der Webserver (User `www-data` oder ähnlich) muss Schreibrechte (`chmod 666` oder `chmod 777`) auf die Datei UND den Ordner haben, in dem sie liegt.
3. **Python:** Stelle sicher, dass Python auf deinem Hosting-Paket verfügbar ist (meistens ja).
4. **Abhängigkeiten:** Da du `pip` oft nicht direkt ausführen kannst, musst du die Python-Pakete (`flask`, `werkzeug` etc.) eventuell lokal herunterladen und mit hochladen.
   - Befehl lokal: `pip install -r requirements.txt -t packages/`
   - Dann den Ordner `packages` hochladen.
5. **Konfiguration:**
   - `.htaccess` Datei im Hauptverzeichnis anlegen (siehe Beispiel in diesem Ordner).
   - `index.cgi` Datei anpassen (Pfad zum Projekt, Pfad zu `packages`).
   - `index.cgi` muss ausführbar sein (`chmod 755`).

**Alternativ (einfacher):**
Wenn All-Inkl.com Docker oder spezielle Python-Hosting-Optionen (WSGI) anbietet (oft ab Managed Server), nutze diese. Bei Standard-Webhosting ist der CGI-Weg oben der gängige.

**Wichtig:**
- **Debug-Modus:** In `app.py` unbedingt `debug=True` auf `False` setzen für den Live-Betrieb!
- **Secret Key:** In `app.py` den `secret_key` ändern.

Viel Erfolg!
