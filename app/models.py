from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_first = db.Column(db.String(150))
    name_last = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    # created_on = db.Column(db.DateTime, default = dt.utcnow)

    # created_on = db.Column(db.timestamp, nullable=False)
    
    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
    
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.name_first = data['name_first']
        self.name_last = data['name_last']
        self.email = data['email'] 
        self.password = self.hash_password(data['password'])

    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database
        
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???