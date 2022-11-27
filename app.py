from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from forms import SignUpForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7a9097f3b37240fe8dbc99bc'
client = MongoClient("mongodb+srv://dbadmin:H9kGaW0KH3wV1zpi@cluster0.sfcugwr.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=client["WebDB"]
user_pwd = db["Webmaster"]

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("homepage.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/register', methods =['GET', 'POST'])
def register_page():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        user_found = user_pwd.find_one({"username": username})
        if user_found:
            msg = "This username has been used, please choose another username"
    return render_template("register.html",message =msg)