from dotenv import load_dotenv
import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, make_response

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securebank"  
)
cursor = db.cursor()

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

@app.route('/transactions')
def transactions():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
    else:
        return "User not found", 404
    
    cursor.execute("SELECT amount, type, timestamp FROM transactions WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
    data = cursor.fetchall()

    return render_template("transactions.html", username=username, transactions=data)

@app.route('/add-form')
def add_form():
    if 'username' not in session:
        return redirect('/login')
    return render_template('add-form.html', action='add')

@app.route('/add', methods=['POST'])
def add_money():
    if 'username' not in session:
        return redirect('/login')
    
    amount_str = request.form['amount']
    if not amount_str.replace('.', '', 1).isdigit() or float(amount_str) <= 0:
        return "Invalid amount", 400
    amount = float(amount_str)
    description = request.form.get('description', '')
    username = session['username']

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
    else:
        return "User not found", 404

    try:
        cursor.execute("INSERT INTO transactions (user_id, amount, type, description) VALUES (%s, %s, 'credit', %s)", (user_id, amount, description))
        db.commit()
        return redirect('/transactions')
    except Exception as e:
        return f"Error while adding money: {e}"
    
@app.route('/withdraw-form')
def withdraw_form():
    if 'username' not in session:
        return redirect('/login')
    return render_template('withdraw-form.html', action='withdraw')

@app.route('/withdraw', methods=['POST'])
def withdraw_money():
    if 'username' not in session:
        return redirect('/login')
    
    
    amount_str = request.form['amount']
    if not amount_str.replace('.', '', 1).isdigit or float(amount_str) <= 0:
        return "Invalid amount", 404
    amount = float(amount_str)
    description = request.form.get('desription', '')
    username = session['username']

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
    else:
        return "User not found", 404

    try:
        cursor.execute("INSERT INTO transactions (user_id, amount, type, description) VALUES (%s, %s, 'debit', %s)", (user_id, amount, description))
        db.commit()
        return redirect('/transactions')
    except:
        return "Error while withdrawing money."

if __name__ == '__main__':
    app.run(debug=True)