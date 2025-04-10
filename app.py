from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sYL0tss$aaaa@localhost/bobaway"
db = SQLAlchemy(app)
