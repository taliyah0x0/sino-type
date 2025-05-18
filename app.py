from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "89t%ygbh76jnbh8gty6791#NKsadf"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sYL0tss$aaaa@localhost/bobaway"
db = SQLAlchemy(app)
encryption = Bcrypt(app) 