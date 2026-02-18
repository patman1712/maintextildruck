
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Pfad zu Ihrem Python-Projekt anpassen
import sys
import os

# Pfad zum Projektordner (relative zur Datei oder absolut)
# Beispiel: '/www/htdocs/w123456/flask_app/'
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Abhängigkeiten hinzufügen, falls sie lokal installiert sind (z.B. in 'packages')
# sys.path.insert(0, os.path.join(project_dir, 'packages'))

from wsgiref.handlers import CGIHandler
from app import app

# Datenbank-Initialisierung sicherstellen (optional, besser manuell ausführen)
# from app import init_db
# init_db()

class ProxyFix(object):
   def __init__(self, app):
       self.app = app
   def __call__(self, environ, start_response):
       environ['SERVER_NAME'] = ""
       environ['SERVER_PORT'] = "80"
       environ['REQUEST_METHOD'] = "GET"
       environ['SCRIPT_NAME'] = ""
       environ['QUERY_STRING'] = ""
       environ['SERVER_PROTOCOL'] = "HTTP/1.1"
       return self.app(environ, start_response)

if __name__ == '__main__':
    # Bei All-Inkl.com läuft Python oft als CGI
    CGIHandler().run(app)
