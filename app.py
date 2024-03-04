import random
from flask import jsonify, Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import secrets
from chatbot_logic import process_user_message

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "m4xpl0it"
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

# Function to generate session token
def make_token():
    return secrets.token_urlsafe(16)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        login = User.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            session['user_session_id'] = make_token()  # Generate and store session ID
            return redirect(url_for("index_auth"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = User(username=uname, email=mail, password=passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/user")
def index_auth():
    session_id = session.get('user_session_id')
    if session_id is None:
        return redirect(url_for("login"))
    return render_template("index_auth.html", sessionId=session_id)

@app.route("/upload")
def bmi():
    return render_template("bmi.html")

@app.route("/diseases")
def diseases():
    return render_template("diseases.html")

# Route to handle chatbot messages
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json.get("message")
    response = process_user_message(user_input)
    return jsonify({"response": response})

@app.route("/get_location", methods=["POST"])
def get_location():
    # Get the location data from the request
    location_data = request.json.get("location")
    session['location'] = location_data
    return "Location received successfully"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, port=3000)
