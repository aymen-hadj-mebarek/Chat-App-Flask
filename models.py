from extension import db

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    picture = db.Column(db.LargeBinary)
    
class message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.String(200),nullable=False)
    sender = db.Column(db.Integer)
    receiver = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    type = db.Column(db.String(10))
    
    def __repr__(self):
        return (f"Message : {self.context} from {self.sender} to {self.receiver}")
        
    