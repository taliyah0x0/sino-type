# from flask import Flask, render_template, request
# from app import app, db
# from models import Shanghainese, Korean, Taiwanese, Vietnamese

# @app.route("/admin-login")
# def adminportal():
#     return render_template("adminlogin.html")

# @app.route("/admin-portal", methods=["POST", "GET"])
# def updatepage():
#     if request.method == "POST":
#         # Obtain the language to update, the hanzi, and the romanization
#         language = request.form["language"]
#         hanzi = request.form["hanzi"] 
#         roman = request.form["romanization"] 

#         # Update the corresponding table in database 
#         if language == "Shanghainese":
#             db.session.add(Shanghainese(hanzi, roman))   
#         elif language == "Korean":
#             db.session.add(Korean(hanzi, roman)) 
#         elif language == "Taiwanese":
#             db.session.add(Taiwanese(hanzi, roman)) 
#         elif language == "Vietnamese":
#             db.session.add(Vietnamese(hanzi, roman)) 
#         db.commit() 

#         # Refresh the page 
#         return render_template("adminportal.html", language=language, hanzi=hanzi, roman=roman)
#     else: 
#         return render_template("adminportal.html")

# @app.route("/sino-type")
# def sinopage():
#     return render_template("index.html")
