import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

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
            return "Registered Successfully"
        except:
            return "Username already exists or error occurred."
        
    return render_template("registration.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        
        if user:
            return "Login Successful"
        else:
            return "Invalid username or password."
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)