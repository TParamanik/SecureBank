import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securebank"  # exact name you created
)
cursor = db.cursor()

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        return "Registered Successfully"
    return render_template("registration.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return "Logged In"
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)