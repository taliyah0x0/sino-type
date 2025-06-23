from flask import Flask, render_template, request, session, flash, redirect, url_for
from app import app, db, encryption
from models import Shanghainese, Korean, Taiwanese, Vietnamese, Admin
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
import re

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'adminloginpage'

@login_manager.user_loader
def load_user(user_id): 
    return Admin.query.get(int(user_id))

class LoginForm(FlaskForm): 
    username = StringField(validators=[InputRequired(), Length(max=20)], 
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(max=20)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

@app.route("/admin-login", methods=['GET', 'POST'])
def adminloginpage():
    form = LoginForm()

    # If user submits the form: 
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user: 
            if encryption.check_password_hash(user.password, form.password.data):
                session["database_entries"] = list() 
                login_user(user)
                return redirect(url_for("adminportal"))
        else: 
            flash(f"Username or password is incorrect. Please try again.")
    
    # If form has not been submitted yet: 
    return render_template("adminlogin.html", form=form)

@app.route("/admin-portal", methods=["POST", "GET"])
@login_required
def adminportal():
    
    # This is if the user has submitted the database update form 
    if request.method == "POST":

        # Obtain the language to update, the hanzi, and the romanization
        language = request.form["language"]
        hanzi = request.form["hanzi"] 
        roman = request.form["romanization"] 

        # Checks that the romanji input is all English characters 
        roman = roman.lower() 
        if (not checkRoman(roman)):
            flash(f"The romanji must consist entirely of Latin characters, no punctuation.")

        # Checks that the hanzi is actually hanzi 
        elif (not checkHanzi(hanzi)):
            flash(f"The hanzi you have entered is not a valid hanzi character.")

        # Checks if the entry already exists in the database. If so, let the admin know. 
        elif (checkEntryExistence(language, hanzi, roman)):
            flash(f"You have already added ({hanzi}, {roman}) to the {language} database.", "info")

        else:
            session["database_entries"].append((hanzi, roman, language)) 
            session.modified = True 
            
            # Update the corresponding table in database 
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

    return render_template("adminportal.html", recents=session["database_entries"])
    
# Returns true if the given string is a hanzi character. Otherwise, false. 
def checkHanzi(hanzi):
    return re.search(u'[\u4e00-\u9fff]', hanzi)

# Returns true if the given string consists entirely of Latin alphabet. Otherwise, false. 
def checkRoman(roman):
    char_set = "abcdefghijklmnopqrstuvwxyz"
    return all((True if x in char_set else False for x in roman))

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
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('adminloginpage'))

@app.route("/sino-type")
def sinopage():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 