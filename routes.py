from flask import Flask, render_template, request, session, flash, redirect, url_for
from app import app, db, encryption
from models import Shanghainese, Korean, Taiwanese, Vietnamese, Admin
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

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
        # TODO: Check that the correct password has been entered 
                login_user(user)
                return redirect(url_for("adminportal"))
        else: 
            flash(f"Username or password is incorrect. Please try again.")
    
    # If form has not been submitted yet: 
    return render_template("adminlogin.html", form=form)

@app.route("/admin-portal", methods=["POST", "GET"])
@login_required
def adminportal():
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