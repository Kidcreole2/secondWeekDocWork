

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(30),nullable=False)
    role_id = db.Column(db.Integer, foreign_key=True)