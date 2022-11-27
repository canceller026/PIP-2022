from flask import Flask, render_template, request, session,redirect
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from forms import SignUpForm
from random import randint
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = '7a9097f3b37240fe8dbc99bc'
client = MongoClient("mongodb+srv://dbadmin:H9kGaW0KH3wV1zpi@cluster0.sfcugwr.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=client["WebDB"]
webmaster = db["Webmaster"]
@app.route('/')
@app.route('/home')
def home_page():
    content = db["Content"]
    all_data = content.find({})
    return render_template("homepage.html",info = all_data)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        h_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        authenticate = webmaster.find_one({"username": username, "h_password": h_password})
        if authenticate:
            session['logged_in'] = True
            session['id'] = authenticate['adminID']
            session['username'] = authenticate['username']
            msg = 'Logged in successfully !'
            #return render_template("CMS.html")
        else:
            msg = 'Incorrect username / password !'
    return render_template("login.html", message = msg)

@app.route('/register', methods =['GET', 'POST'])
def register_page():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        user_found = webmaster.find_one({"username": username})
        if user_found:
            msg = "This username has been used, please choose another username"
        elif not username or not password1 or not email or not password2:
            msg = 'Please fill out the form !'
        elif ("@gmail.com" not in email):
            msg = "Invalid Email Address"
        elif password1 != password2:
            msg = "Password not match"
        elif len(password1) < 8:
            msg = "Password too short"
        else:
            adminID = randint(10000000,99999999)
            h_password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
            new_user = {"adminID": adminID, "h_password" : h_password, "password": password1, "username": username, "email": email}
            webmaster.insert_one(new_user)
        
    return render_template("register.html",message =msg)

@app.route('/logout')
def logout_page():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route('/member')
def member_page():
    return render_template("about.html")

@app.route('/cms', methods = ['GET', 'POST'])
def cms_page():
    if request.method == 'POST':
        return render_template("base.html")