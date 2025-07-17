import mysql.connector
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = '9f3aG8pV2xBqL6zT1eR7WcY5mN0HuJXd'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securebank"  
)
cursor = db.cursor()
cursor.execute("SHOW TABLES")
print("Tables:", cursor.fetchall())


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            return redirect('/login')
        except:
            return "Username already exists or error occurred."
        
    return render_template("registration.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
        
            if user:
                session['username'] = username
                return redirect('/dashboard')
            else:
                return "Invalid username or password."
        except:
            return "Error during login"

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)