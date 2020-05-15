from app import db

# Initializing basic user info


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

# Printing out which user is current
def __repr__(self):
    return '<User {}>'.format(self.username)