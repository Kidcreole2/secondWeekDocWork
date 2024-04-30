from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from core import app

db = SQLAlchemy(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20),nullable=False)
    
    def __init__(self, login: str, password: str, firstname: str, lastname: str, surname: str, role):
        self.login = login
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.surname = surname
        self.role = role
    
    @staticmethod
    def auth_user(login, password) -> str:
        user = Users.query.filter_by(login=login).first()
        print(user)
        if user is not None and user.password == password:
            login_user(user)
            return user.role
        else:
            if user is None:
                return "wrong_login"
            else:
                return "wrong_pass"
    
    @staticmethod
    def register(user):
        new_user = Users.query.filter_by(login=user.login).first()
        if new_user is None:
            db.session.add(user)
            db.session.commit()
            return False
        else:
            return True


with app.app_context():
    db.create_all()