from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://peliixtyhsfiuv:092749581c3028c628fbe0b346f2ae624d877dc694c30e2a2e8befb7964c832b@ec2-184-72-237-95.compute-1.amazonaws.com/ddgjcqg98is45a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Client

a = Client.query.filter_by(id=1).first()
print(a)
print(Client.query.filter_by(text='Привет').first())