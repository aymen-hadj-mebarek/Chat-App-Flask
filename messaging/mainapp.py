from flask import render_template, redirect, request,flash,session, url_for
from flask import Blueprint
from extension import db
from models import users,message
from flask_socketio import join_room, leave_room, send, SocketIO
from base64 import b64encode

mainapp = Blueprint("mainapp", __name__)

@mainapp.route("/profile/")
@mainapp.route("/profile")
def profile():
    if session.get("name") or session.get("id"):
        user = db.session.query(users).filter(users.id == session.get("id")).first()
        contacts = db.session.query(users).filter(users.id != session.get("id")).all()
        contacts_images = []
        try:
            pdp = b64encode(user.picture).decode("utf-8")
        except:
            pdp = None
            
        for i in contacts:
            try:
                contacts_images.append(b64encode(i.picture).decode("utf-8"))
            except:
                contacts_images.append(None)
        return render_template("profile.html",name=user,contacts=contacts, pdp=pdp,contacts_images=contacts_images)
    else:
        return redirect(url_for("auth.index"))
 
@mainapp.route("/settings/")
@mainapp.route("/settings")
def settings():
    if session.get("name") or session.get("id"):
        contacts_images = []
        contacts = db.session.query(users).filter(users.id != session.get("id")).all()
        user = db.session.query(users).filter(users.id == session.get("id")).first()
        try:
            pdp = b64encode(user.picture).decode("utf-8")
        except:
            pdp = None
            
        for i in contacts:
            try:
                contacts_images.append(b64encode(i.picture).decode("utf-8"))
            except:
                contacts_images.append(None)
                
        return render_template("settings.html", contacts=contacts, user=user, pdp=pdp, contacts_images=contacts_images)
    else:
        return redirect(url_for("mainapp.profile"))
  
@mainapp.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        picture = request.files["image"].read()
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        id = session.get("id")
        other_users = db.session.query(users).filter(users.id != session.get("id"))
        if len(other_users.filter(users.username == name).all()) > 0 or len(other_users.filter(users.email == email).all()) > 0:
            flash("This name or email is already taken !")
            return redirect(url_for("mainapp.settings"))
        user = users.query.get_or_404(id)
        if user:
            print("user found")
            user.username = name
            user.email = email
            user.password = password
            if picture != b"":
                user.picture = picture
            db.session.commit()
        return redirect(url_for("mainapp.profile"))
        
    else:
        return redirect(url_for("mainapp.profile"))

@mainapp.route("/deletepdp")
def delete_pdp():
    id = session.get("id")
    user = users.query.get_or_404(id)
    if user:
        print("user found")
        user.picture = None
        db.session.commit()
    return redirect(url_for("mainapp.profile"))

@mainapp.route("/contacts/<id>")
def contact(id):
    if session.get("name") or session.get("id"):
        session["room"] = order(id)
        contacts = db.session.query(users).filter(users.id != session.get("id")).filter(users.id != id).all()
        contact = db.session.query(users).filter(users.id == id).first()
        contacts_images = []
        for i in contacts:
            try:
                contacts_images.append(b64encode(i.picture).decode("utf-8"))
            except:
                contacts_images.append(None)
                
        messages = db.session.query(message).order_by(message.date,message.time).all()
        sender = db.session.query(users).filter(users.username == session.get("user")).first().id
        return render_template("messages.html",name=contact,contacts=contacts,messages=messages,sender=sender, contacts_images=contacts_images)
    
def order(id):
    List = [str(session.get("user")),str(db.session.query(users).filter(users.id == id).first().username)]
    List.sort()
    return List[0]+"+"+List[-1]

