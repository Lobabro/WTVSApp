from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Base de données vulnérable
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
conn.commit()

# Clé secrète exposée
SECRET_KEY = "supersecretkey"

@app.route('/')
def home():
    return "<h1>Bienvenue sur l'application vulnérable !</h1>"

# Injection SQL
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return "Bienvenue, " + user[1]
        return "Échec de l'authentification"
    return '<form method="post">Nom: <input name="username"><br>Mot de passe: <input name="password" type="password"><br><input type="submit" value="Login"></form>'

# XSS
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', '')
    return render_template_string("<h1>Bonjour, {}!</h1>".format(name))

if __name__ == '__main__':
    app.run(debug=True)