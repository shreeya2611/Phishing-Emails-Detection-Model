from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
import re
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"

bcrypt = Bcrypt(app)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT,
        otp TEXT
    )
    ''')

    conn.commit()
    conn.close()


# ---------------- VALIDATION ----------------
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    return len(password) >= 6


# ---------------- PASSWORD HASHING ----------------
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed, password):
    return bcrypt.check_password_hash(hashed, password)


# ---------------- OTP ----------------
def generate_otp():
    return str(random.randint(100000, 999999))


# ---------------- ROUTES ----------------

# Home (Login Page)
@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # your existing logic
        pass
    return render_template("register.html", title="Register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # your existing logic
        pass
    return render_template("login.html", title="Login")  # or index.html


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if not validate_email(email):
            return "❌ Invalid Email"

        if not validate_password(password):
            return "❌ Password must be at least 6 characters"

        hashed_pw = hash_password(password)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_pw)
            )
            conn.commit()
        except:
            return "❌ Username already exists"

        conn.close()

        return redirect("/")

    return render_template("register.html")


# OTP Verification
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        entered_otp = request.form["otp"]
        username = session.get("temp_user")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT otp FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if result and entered_otp == result[0]:
            session["user"] = username
            return redirect("/dashboard")

        return "❌ Invalid OTP"

    return render_template("verify_otp.html")


# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/")


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)