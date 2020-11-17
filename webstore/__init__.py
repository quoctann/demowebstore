from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin



app = Flask(__name__)
app.secret_key = "qou3rhkjsafbi327y12$U@$JK@BKANOEIDQ"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Abc1234%^&@localhost/phonestoredb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)