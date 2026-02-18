
# Deployment bei Railway.app

**Ja, absolut empfehlenswert!** Railway ist deutlich moderner, einfacher zu bedienen und performanter als klassisches Shared Hosting.

Allerdings gibt es einen **wichtigen Punkt** zu beachten:

### Das Problem: Flüchtige Daten
Railway löscht standardmäßig alle Daten im Container bei jedem Neustart oder Deployment. Das heißt: Deine `database.db` und hochgeladene Bilder in `static/uploads` würden verschwinden!

### Die Lösung: Railway Volumes
Du musst bei Railway ein **Volume** (Festplatte) anlegen und einbinden.

1. **Projekt erstellen:** Verbinde Railway mit deinem GitHub-Repository.
2. **Volume hinzufügen:**
   - Gehe in dein Railway-Projekt -> Klicke auf den Service.
   - Gehe zu "Volumes".
   - Erstelle ein Volume und mounte es (binde es ein) auf den Pfad `/app/data` (oder ähnlich).
3. **App anpassen:**
   - Du musst in `app.py` sicherstellen, dass die Datenbank und Uploads in diesem Pfad liegen.
   - Beispiel:
     ```python
     # In app.py
     import os
     
     # Wenn wir auf Railway sind (Erkennung über Environment Variable), nutze das Volume
     if os.environ.get('RAILWAY_ENVIRONMENT'):
         BASE_DIR = '/app/data'
     else:
         BASE_DIR = os.path.dirname(os.path.abspath(__file__))
         
     DB_NAME = os.path.join(BASE_DIR, 'database.db')
     UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
     ```

### Schritte für Railway:
1. Ich habe dir bereits ein `Procfile` erstellt (wichtig für Railway).
2. `gunicorn` wurde zu `requirements.txt` hinzugefügt (wird als Webserver benötigt).
3. Lade den Code auf GitHub hoch.
4. Verbinde GitHub mit Railway.
5. Konfiguriere das Volume wie oben beschrieben.

**Vorteile Railway:**
- Automatisches Deployment bei jedem `git push`.
- SSL (https) Zertifikat automatisch dabei.
- Viel schneller.
- Keine veraltete CGI-Technik.

**Nachteil:**
- Kostet nach der Trial-Phase ca. $5/Monat (je nach Nutzung), während All-Inkl oft schon bezahlt ist.
