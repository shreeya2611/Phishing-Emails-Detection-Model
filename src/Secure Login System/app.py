from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "secret123"

# -----------------------------
# 🔧 DATABASE SETUP
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# 🔐 PASSWORD FUNCTIONS
# -----------------------------
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# -----------------------------
# 🏠 HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return '''
    <h1>Welcome 🚀</h1>
    <a href="/register">Register</a><br><br>
    <a href="/login">Login</a>
    '''

# -----------------------------
# 📝 REGISTER
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        hashed_pw = hash_password(password)

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_pw)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:
            return "Username or Email already exists ❌"

    return render_template("register.html")

# -----------------------------
# 🔑 LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? OR email=?",
            (login_input, login_input)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user[3]

            if check_password(stored_password, password):
                session["user"] = user[1]
                return redirect("/dashboard")
            else:
                return "Wrong password ❌"
        else:
            return "User not found ❌"

    return '''
    <h2>Login</h2>
    <form method="POST">
        Username or Email: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Login</button>
    </form>
    '''

# -----------------------------
# 📊 DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"<h1>Welcome {session['user']} 🎉</h1><a href='/logout'>Logout</a>"
    return redirect("/login")

# -----------------------------
# 🚪 LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# -----------------------------
# ▶ RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)