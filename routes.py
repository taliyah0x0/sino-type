from flask import Flask, render_template, request, session, flash 
from app import app, db
from models import Shanghainese, Korean, Taiwanese, Vietnamese

@app.route("/admin-login")
def adminloginpage():
    return render_template("adminlogin.html")

@app.route("/admin-portal", methods=["POST", "GET"])
def updatepage():
    # TODO: once the page is finalized, check if the admin has actually logged in using the session 
    # if "user" in session:

        # This is if the user is simply being redirected after logging in 
        if request.method == "GET":
            session["database_entries"] = dict() 
            return render_template("adminportal.html")

        # This is if the user has submitted the database update form 
        if request.method == "POST":

            # Obtain the language to update, the hanzi, and the romanization
            language = request.form["language"]
            hanzi = request.form["hanzi"] 
            roman = request.form["romanization"] 

            # TODO: check and clean the user input to ensure consistency 
            # Check that hanzi is actually hanzi, somehow 
            # Check roman is all English letters, somehow 
            # Prevent SQL injections 
            roman = roman.lower() 

            # Checks if the entry already exists in the database. If so, let the admin know. 
            if (checkEntryExistence(language, hanzi, roman)):
                flash(f"You have already added ({hanzi}, {roman}) to the {language} database.", "info")
            else:
                # Update the corresponding table in database 
                session["database_entries"][(hanzi, roman)] = language 
                if language == "Shanghainese":
                    db.session.add(Shanghainese(hanzi, roman)) 
                    db.session.commit()
                elif language == "Korean":
                    db.session.add(Korean(hanzi, roman))
                    db.session.commit()
                elif language == "Taiwanese":
                    db.session.add(Taiwanese(hanzi, roman)) 
                    db.session.commit()
                elif language == "Vietnamese":
                    db.session.add(Vietnamese(hanzi, roman)) 
                    db.session.commit()

            # Refresh the page 
            # TODO: replace the inputs with "session["database_entries"]"
            return render_template("adminportal.html", language=language, hanzi=hanzi, roman=roman)
    
    # User is not in session 
    # return "Access denied - You are not logged in."
    
# Returns true if the entry has already been added. 
def checkEntryExistence(language, h, r):
    found = False 
    if language == "Shanghainese":
        found = Shanghainese.query.filter_by(hanzi=h, roman=r).first()
    elif language == "Korean":
        found = Korean.query.filter_by(hanzi=h, roman=r).first()
    elif language == "Taiwanese":
        found = Taiwanese.query.filter_by(hanzi=h, roman=r).first()
    elif language == "Vietnamese":
        found = Vietnamese.query.filter_by(hanzi=h, roman=r).first()
    return found 
    

@app.route("/sino-type")
def sinopage():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run() 