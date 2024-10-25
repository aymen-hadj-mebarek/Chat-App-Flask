from flask import render_template, redirect, request,flash,session, url_for
from flask import Blueprint
from extension import db
from models import users

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("auth.html",value="login")
    else:
        Login = request.form.get("loginBtn",default=False)
        Signup = request.form.get("signupBtn",default=False)
        if Login != False:
            login_name = request.form.get("emailadL")
            login_password = request.form.get("mdpsL")
            if "@" in login_name:
                user_name = db.session.query(users).filter(users.email == login_name).first()
            else:
                user_name = db.session.query(users).filter(users.username == login_name).first()
            if user_name:
                user = users.query.filter(users.id == user_name.id).first()
                if user.password == login_password :
                    session["user"] = user.username
                    session["id"] = user.id
                    return redirect(url_for("mainapp.profile"))
                else:
                    flash("Password incorrect")
                    return render_template("auth.html",value="login")
            flash("email or username does not exist, please create an account")
            return render_template("auth.html",value="signup")
        if Signup != False:
            signup_name = request.form.get("name")
            signup_email = request.form.get("emailadSU")
            signup_password = request.form.get("mdpsSU")
            confirm_password = request.form.get("mdps_check")
            if not db.session.query(users).filter(users.email == signup_email).first() and not db.session.query(users).filter(users.username == signup_name).first():
                if signup_password == confirm_password:
                    new_user = users(username=signup_name,email=signup_email,password=signup_password)
                    db.session.add(new_user)
                    db.session.commit()
                    user = users.query.filter(users.id == new_user.id).first()
                    session["user"] = user.username
                    session["id"] = user.id
                    return redirect(url_for("mainapp.profile"))
                else:
                    flash_message = "Password is not the same as the confirm password."
                    flash(flash_message)
                    return render_template("auth.html",value="signup")
            else:
                flash_message = ""
                if db.session.query(users).filter(users.email == signup_email).first():
                    flash_message += "This email is already used, try logging in."
                if db.session.query(users).filter(users.username == signup_name).first():
                    flash_message += "\nThis username is already taken, try changing the username, or logging in if you have an account."
                if flash_message != "":
                    flash(flash_message)
                return render_template("auth.html",value="signup")
            
