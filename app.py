from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        return "Registered Successfully"
    return render_template("register.html")

@app.route('/register', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return "Logged In"
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
