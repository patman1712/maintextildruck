from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import sqlite3
import os
import resend
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this in production

# Configuration for Persistent Storage (Railway Volume)
DATA_FOLDER = 'data'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DB_NAME = os.path.join(DATA_FOLDER, 'database.db')
UPLOAD_FOLDER = os.path.join(DATA_FOLDER, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            id TEXT PRIMARY KEY,
            content TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS customer_logos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT
        )
    ''')
    
    # Initial data based on user request
    initial_data = [
        ('gude', '<h2>Gude!</h2><p>Willkommen!</p>'),
        ('about', '<h2>Über uns</h2><p>Wir sind...</p>'),
        ('services', '<h2>Services</h2><p>Deine Services...</p>'),
        ('references', '<h2>Referenzen</h2><p>Unsere zufriedenen Kunden...</p>'),
        ('contact', '<h2>Kontakt</h2><p>Ruf uns an!</p>'),
        ('catalog', '<h2>Katalog</h2><p>Hier findest du unsere Produkte.</p>'),
        ('header_image', 'static/assets/cropped-f_frame-scaled-1.jpg'),
        ('company_name', 'Dein Shop'),
        ('page_title', 'Textildruck & Merchandise'),
        ('meta_description', 'Dein Spezialist für Textildruck & Merchandise.')
    ]
    c.executemany('INSERT OR IGNORE INTO sections (id, content) VALUES (?, ?)', initial_data)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/data/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    conn = get_db_connection()
    sections = conn.execute('SELECT * FROM sections').fetchall()
    
    # Check if customer_logos table exists before querying
    try:
        logos = conn.execute('SELECT * FROM customer_logos').fetchall()
    except sqlite3.OperationalError:
        logos = []
        
    conn.close()
    
    # Convert list of rows to dictionary for easy access in template
    content = {row['id']: row['content'] for row in sections}
    return render_template('index.html', content=content, customer_logos=logos)

@app.route('/send_email', methods=['POST'])
def send_email():
    conn = get_db_connection()
    resend_api_key = conn.execute("SELECT content FROM sections WHERE id = 'resend_api_key'").fetchone()
    recipient_email = conn.execute("SELECT content FROM sections WHERE id = 'recipient_email'").fetchone()
    sender_email = conn.execute("SELECT content FROM sections WHERE id = 'sender_email'").fetchone()
    conn.close()

    if not resend_api_key or not resend_api_key['content']:
        flash('E-Mail Versand nicht konfiguriert (API Key fehlt).')
        return redirect(url_for('index', _anchor='kontakt'))

    resend.api_key = resend_api_key['content']
    
    # Default sender if not configured (Resend requires a verified domain or onboarding@resend.dev)
    from_email = sender_email['content'] if sender_email and sender_email['content'] else "onboarding@resend.dev"
    to_email = recipient_email['content'] if recipient_email and recipient_email['content'] else "info@example.com"

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
        email_data = {
            "from": from_email,
            "to": to_email,
            "subject": f"Neue Kontaktanfrage von {name}",
            "html": f"<p><strong>Name:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p><strong>Nachricht:</strong><br>{message}</p>"
        }
        
        if email:
            email_data["reply_to"] = email

        r = resend.Emails.send(email_data)
        flash('Nachricht erfolgreich gesendet!')
    except Exception as e:
        print(f"Error sending email: {e}")
        flash(f'Fehler beim Senden der Nachricht: {e}')

    return redirect(url_for('index', _anchor='kontakt'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    
    if request.method == 'POST':
        active_tab = request.form.get('active_tab')
        # Handle customer logo upload
        if 'new_customer_logo' in request.files:
            file = request.files['new_customer_logo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                db_path = f"data/uploads/{filename}"
                conn.execute('INSERT INTO customer_logos (filepath) VALUES (?)', (db_path,))
        
        # Handle logo deletion
        if 'delete_logo_id' in request.form:
            logo_id = request.form['delete_logo_id']
            conn.execute('DELETE FROM customer_logos WHERE id = ?', (logo_id,))

        # Handle file upload for images (existing logic)
        for key in request.files:
            if key == 'new_customer_logo': continue # Skip as handled above
            file = request.files[key]
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                # Update database with new path
                db_path = f"data/uploads/{filename}"
                conn.execute('INSERT OR REPLACE INTO sections (id, content) VALUES (?, ?)', (key, db_path))
        
        for key in request.form:
            if key == 'delete_logo_id': continue # Skip
            if key.startswith('content_'):
                section_id = key.replace('content_', '')
                new_content = request.form[key]
                conn.execute('INSERT OR REPLACE INTO sections (id, content) VALUES (?, ?)', (section_id, new_content))
        conn.commit()
        flash('Änderungen gespeichert!')
        return redirect(url_for('admin', active_tab=active_tab))

    sections = conn.execute('SELECT * FROM sections').fetchall()
    content_dict = {row['id']: row['content'] for row in sections}
    try:
        logos = conn.execute('SELECT * FROM customer_logos').fetchall()
    except sqlite3.OperationalError:
        logos = []
    conn.close()
    
    # Structure sections for the admin menu
    menu_structure = {
        'HOME': ['page_title', 'company_name', 'meta_description', 'home_text', 'home_button_text', 'home_button_link', 'header_image'],
        'ÜBER UNS': ['about'],
        'SERVICES': ['services', 'service_intro_image', 'service_intro_text', 'service_step_1', 'service_step_2', 'service_step_3'],
        'TEXTILVEREDELUNG': ['textile_headline', 'textile_text', 'textile_image_1', 'textile_image_2'],
        'REFERENZEN': ['references_title', 'instagram_widget'],
        'KUNDEN': ['slider_headline', 'slider_text'],
        'KONTAKT': ['contact_title', 'contact_text', 'contact_label_name', 'contact_label_email', 'contact_label_message', 'contact_button_text', 'contact_privacy_note', 'contact_text_color'],
        'WHATSAPP': ['whatsapp_number', 'whatsapp_initial_text', 'whatsapp_label', 'whatsapp_url'],
        'KATALOG': ['catalog'],
        'EMAIL SETTINGS': ['resend_api_key', 'recipient_email', 'sender_email'],
        'RECHTLICHES': ['impressum_button_text', 'impressum_button_link', 'datenschutz_button_text', 'datenschutz_button_link'],
        'FOOTER': ['footer_1_title', 'footer_1_content', 'footer_2_title', 'footer_2_content', 'footer_copyright'],
        'NAVIGATION': [
            'menu_home_label', 'menu_home_link',
            'menu_about_label', 'menu_about_link',
            'menu_services_label', 'menu_services_link',
            'menu_references_label', 'menu_references_link',
            'menu_contact_label', 'menu_contact_link',
            'menu_catalog_label', 'menu_catalog_link',
            'social_1_icon', 'social_1_link', 'social_1_color',
            'social_2_icon', 'social_2_link', 'social_2_color'
        ],
        'SIDEBAR': ['sidebar_contact_title', 'sidebar_contact_content', 'sidebar_about_text'],
        'DESIGN': ['site_logo', 'primary_color']
    }
    
    active_tab = request.args.get('active_tab')
    return render_template('admin.html', sections=sections, content=content_dict, menu_structure=menu_structure, customer_logos=logos, active_tab=active_tab)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        active_tab = request.form.get('active_tab')
        password = request.form['password']
        if password == 'admin123':  # Simple password for now
            session['logged_in'] = True
            return redirect(url_for('admin', active_tab=active_tab))
        else:
            flash('Falsches Passwort!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=True)
else:
    # Initialize DB when running with Gunicorn
    init_db()
