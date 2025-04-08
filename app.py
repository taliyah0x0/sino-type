from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://yaotong:sYL0tss$aaaa@127.0.0.1/world"
db = SQLAlchemy(app)

@app.route("/admin-login")
def adminportal():
    return render_template("adminlogin.html")

@app.route("/admin-portal", methods=["POST", "GET"])
def updatepage():
    if request.method == "POST":
        language = request.form["language"]
        hanzi = request.form["hanzi"] 
        roman = request.form["romanization"] 
        return render_template("adminportal.html", language=language, hanzi=hanzi, roman=roman)
    else: 
        return render_template("adminportal.html")

@app.route("/sino-type")
def sinopage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run() 