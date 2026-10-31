from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = "database.db"

# -------------------------
# DATABASE INITIALIZATION
# -------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # create contacts table if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    # ensure phone column exists (migration)
    cursor.execute("PRAGMA table_info(contacts)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'phone' not in cols:
        try:
            cursor.execute("ALTER TABLE contacts ADD COLUMN phone TEXT")
        except sqlite3.OperationalError:
            pass  # column may already exist in concurrent run

    # create careers table if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            qualification TEXT,
            experience TEXT
        )
    """)
    # ensure phone column exists in careers
    cursor.execute("PRAGMA table_info(careers)")
    cols2 = [row[1] for row in cursor.fetchall()]
    if 'phone' not in cols2:
        try:
            cursor.execute("ALTER TABLE careers ADD COLUMN phone TEXT")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()

init_db()

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name,email,phone,message) VALUES (?,?,?,?)",
                       (name,email,phone,message))
        conn.commit()
        # log new contact to console
        print(f"New contact saved: {name}, {email}, {phone}")
        conn.close()

        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/careers", methods=["GET", "POST"])
def careers():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        qualification = request.form["qualification"]
        experience = request.form["experience"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO careers (name,email,phone,qualification,experience) VALUES (?,?,?,?,?)",
                       (name,email,phone,qualification,experience))
        conn.commit()
        # log new career application
        print(f"New career application: {name}, {email}, {phone}")
        conn.close()

        return redirect(url_for("careers"))

    return render_template("careers.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

# -------------------------
# ADMIN/DEBUG ROUTES (for development)
# -------------------------

@app.route('/admin/contacts')
def admin_contacts():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id,name,email,phone,message FROM contacts ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    # simple HTML listing
    html = '<h1>Contact Submissions</h1><ul>'
    for r in rows:
        html += f'<li>{r[0]}: {r[1]} ({r[2]} / {r[3]}) - {r[4]}</li>'
    html += '</ul>'
    return html

@app.route('/admin/careers')
def admin_careers():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id,name,email,phone,qualification,experience FROM careers ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    html = '<h1>Career Applications</h1><ul>'
    for r in rows:
        html += f'<li>{r[0]}: {r[1]} ({r[2]} / {r[3]}) - {r[4]}, {r[5]}</li>'
    html += '</ul>'
    return html

# -------------------------
# SERVICE SUBPAGES
# -------------------------

@app.route("/services/<service_name>")
def service_page(service_name):
    return render_template(f"services/{service_name}.html")

# -------------------------
if __name__ == "__main__":
    app.run(debug=True)