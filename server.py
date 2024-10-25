from flask import Flask, render_template, redirect, url_for,session
from flask_socketio import join_room, leave_room, send, SocketIO
import os, datetime
from extension import db
from models import users, message
from auth.auth import auth
from messaging.mainapp import mainapp
import socket

def create_app():
    app = Flask(__name__)
    app.secret_key = "Secret Key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Chats.db"
    db.init_app(app)
    if not os.path.exists("instance\Chats.db"):
        with app.app_context():
            db.create_all()
            print("database created") 
    else:
        print("database already exists")
    app.register_blueprint(auth,url_prefix="/auth")
    app.register_blueprint(mainapp,url_prefix="/")
    return app
   
   
app = create_app()
socketio = SocketIO(app=app)

@app.route("/")
def index():
    return redirect("/auth")

@app.route("/logout")
def logout():
    if session.get("id") or session.get("name") :
        session.clear()
        print("session cleared")
        return redirect(url_for("auth.index"))
    else:
        print("session didnt exist")
        return redirect(url_for("auth.index"))
        
socketio = SocketIO(app)

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("user")
    print(session.get("room"))
    print("connected")
    join_room(room)
    print({"name":name,"message":"has entered the room"})
        
        
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    print(f"{name} has left the room {room}")


@socketio.on('message_from_client')
def handle_message(message_context):
    print("Message received from client:", message_context["message_context"])
    sender = db.session.query(users).filter(users.username == session.get("user")).first().id
    receiver = db.session.query(users).filter(users.username == session.get("room").replace(session.get("user"),"").replace("+","")).first().id
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.date()
    formatted_time = current_datetime.time()
    new_message = message(context=message_context["message_context"],sender=sender,receiver=receiver,time=formatted_time,date=formatted_date)
    db.session.add(new_message)
    db.session.commit()
    package = {"message" : message_context["message_context"], "sender" : sender, "receiver" : receiver}
    send(package,to=session.get("room"))

if __name__ == "__main__":
    # getting the IPv4 address no matter how it changes
    hostname = socket.gethostname()
    ipv4_address = socket.gethostbyname(hostname)
    
    socketio.run(app=app,debug=True,host=ipv4_address,port=5500)

