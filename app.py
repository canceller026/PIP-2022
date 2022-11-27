from flask import Flask, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi
app = Flask(__name__)

client = MongoClient("mongodb+srv://dbadmin:H9kGaW0KH3wV1zpi@cluster0.sfcugwr.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=client.test
user_pwd = db.get_collection

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("homepage.html")

@app.route('/login')
def login_page():
    return render_template("login.html")