from flask import Flask, render_template
from flask.globals import request
import requests
import json
from flask_sqlalchemy import SQLAlchemy


# init 
app = Flask(__name__)

# env
ENV = 'dev'
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost/library'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# model of archive
class Archive(db.Model):
    __tablename__ = "archive"
    id = db.Column(db.Integer, primary_key=True)
    bookID = db.Column(db.Integer, unique=True)
    fee = db.Column(db.Integer) 
    imported = db.Column(db.Integer) 

def __init__(self, bookID, fee, imported):
    self.bookID = bookID
    self.fee = fee
    self.imported = imported 

    # model of user
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    open = db.Column(db.DateTime, nullable=False)
    close = db.Column(db.DateTime, nullable=False)
    bookID = db.Column(db.Integer, unique=True)
    due = db.Column(db.Integer)

def __init__(self, name, open, close, bookID, due):
    self.name = name
    self.open = open
    self.close = close 
    self.bookID = bookID
    self.due = due

@app.get("/")
def hello_world():
    req = requests.get('https://frappe.io/api/method/frappe-library')
    data = req.content
    # print(req.json())
    jsonData = json.loads(data)
    return render_template('index.html', data=jsonData['message'])

@app.post("/add")
def adding():
    bookID = request.form['bookID']
    imported = request.form['imported']
    fee = request.form['fee']
    print(bookID, imported, fee)
    arc = Archive(bookID=bookID, fee=fee, imported=imported)
    db.session.add(arc)
    db.session.commit()
    return render_template('add.html')
