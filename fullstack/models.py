from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from core import app

db = SQLAlchemy(app)

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20),nullable=False)

    # связи
    student = db.relationship("Student", back_populates="user")
    director_opop = db.relationship("Director_OPOP", back_populates="user")
    director_practice_usu = db.relationship("Director_Practice_USU", back_populates="user")
    director_practice_company = db.relationship("Director_Practice_Company", back_populates="user")
    director_practice_organization = db.relationship("Director_Practice_Organization", back_populates="user")
    
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
        
class Practice(db.Model) :
    __tablename__ = "practice"
    practice_id = db.Column(db.Integer, primary_key = True)
    year = db.Column(db.Integer, nullable = False)
    period_practice = db.Column(db.String(20), nullable = False)
    name = db.Column(db.String(50), nullable = False)
    order = db.Column(db.String(100), nullable = False)
    type_of_practice = db.Column(db.String(100), nullable = False)
    kind_of_practice = db.Column(db.String(100), nullable = False)

    # связи
    practice_place = db.relationship("Practice_Place", back_populates="practice")
    director_usu_practice = db.relationship("Director_USU_Practice", back_populates="practice")
    director_company_practice = db.relationship("Director_Company_Practice", back_populates="practice")
    practice_group = db.relationship("Practice_Group", back_populates="practice")
    student_practice = db.relationship("Student_Practice", back_populates="practice")

    def __init__(self, year: int, period_practice: str, name: str, order: str, type_of_practice: str, kind_of_practice: str):
        self.year = year
        self.period_practice = period_practice
        self.name = name
        self.order = order
        self.type_of_practice = type_of_practice
        self.kind_of_practice = kind_of_practice
        
class Insitute(db.Model) :
    __tablename__ = "institute"
    insistute_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable = False)

    # связи
    specialization = db.relationship("Specialization", back_populates="institute")

    def __init__(self, name: str):
        self.name = name

class Place(db.Model) :
    __tablename__ = "place"
    place_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

    # связи
    practice_place = db.relationship("Practice_Place", back_populates="place")
    
    def __init__(self, name: str):
        self.name = name


class Director_OPOP(db.Model) :
    __tablename__ = "director_opop"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_opop")
    specialization = db.relationship("Specialization", back_populates="director_opop")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

class Director_Practice_USU(db.Model) :
    __tablename__ = "director_practice_usu"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_usu")
    director_usu_practice = db.relationship("Director_USU_Practice", back_populates="director_practice_usu")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

class Director_Practice_Company(db.Model) :
    __tablename__ = "director_practice_company"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_company")
    director_company_practice = db.relationship("Director_Company_Practice", back_populates="director_practice_company")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

class Director_Practice_Organization(db.Model) :
    __tablename__ = "director_practice_organization"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_organization")
    student_practice = db.relationship("Student_Practice", back_populates="director_practice_organization")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

class Specialization(db.Model) :
    __tablename__ = "specialization"
    specialization_id = db.Column(db.Integer, primary_key = True)
    institute_id = db.Column(db.Integer, db.ForeignKey("insistute.insistute_id"))
    director_opop_id = db.Column(db.Integer,  db.ForeignKey("director_opop.user_id"))
    name = db.Column(db.String(100), nullable = False)
    specialization_code = db.Column(db.String(20), nullable = False)

    # связи
    institute = db.relationship("Institute", back_populates="specialization")
    director_opop = db.relationship("Director_OPOP", back_populates="specialization")
    group = db.relationship("Group", back_populates="specialization")

    def __init__(self, institute_id: int, director_opop_id: int, name: str, specialization_code: str):
        self.institute_id = institute_id
        self.director_opop_id = director_opop_id
        self.name = name
        self.specialization_code = specialization_code

class Group(db.Model) :
    __tablename__ = "group"
    group_id = db.Column(db.Integer, primary_key = True)
    specialization_id = db.Column(db.Integer, db.ForeignKey("specialization.specialization_id"))
    name = db.Column(db.String(10), nullable = False, unique = True)
    course = db.Column(db.String(15), nullable = False)

    # связи
    specialization = db.relationship("Specialization", back_populates="group")
    student = db.relationship("Student", back_populates="group")
    practice_group = db.relationship("Practice_Group", back_populates="group")

    def __init__(self, specialization_id: int, name: str, course: str):
        self.specialization_id = specialization_id
        self.name = name
        self.course = course

class Stuent(db.Model) :
    __tablename__ = "student"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.group_id"))

    # связи
    user = db.relationship("Users", back_populates="student")
    group = db.relationship("Group", back_populates="student")
    student_practice = db.relationship("Student_Practice", back_populates="student")

    def __init__(self, user_id: int, group_id: int):
        self.user_id = user_id
        self.group_id = group_id
    
class Practice_Group(db.Model) :
    __tablename__ = "practice_group"
    group_id = db.Column(db.Integer, db.ForeignKey("group.group_id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.practice_id"))

    # связи
    practice = db.relationship("Practice", back_populates="practice_group")
    group = db.relationship("Group", back_populates="practice_group")

    def __init__(self, group_id: int, practice_id: int):
        self.group_id = group_id
        self.practice_id = practice_id

class Practice_Place(db.Model) :
    __tablename__ = "practice_place"
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.practice_id"))
    place_id = db.Column(db.Integer, db.ForeignKey("place.place_id"))
    
    # связи
    place = db.relationship("Place", back_populates="practice_place")
    practice = db.relationship("Practice", back_populates="practice_place")

    def __init__(self, practice_id: int, place_id: int):
        self.practice_id = practice_id
        self.place_id = place_id

class Director_USU_Practice(db.Model) :
    __tablename__ = "director_usu_practice"
    director_practice_usu_id = db.Column(db.Integer, db.ForeignKey("director_practice_usu.user_id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.practice_id"))

    # связи
    practice = db.relationship("Practice", back_populates="director_usu_practice")
    director_practice_usu = db.relationship("Director_Practice_USU", back_populates="director_usu_practice")

    def __init__(self, director_practice_usu_id: int, practice_id: int):
        self.director_practice_usu_id = director_practice_usu_id
        self.practice_id = practice_id

class Director_Company_Practice(db.Model) :
    __tablename__ = "director_company_practice"
    director_practice_company_id = db.Column(db.Integer, db.ForeignKey("director_practice_company.user_id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.practice_id"))

    # связи
    practice = db.relationship("Practice", back_populates="director_company_practice")
    director_practice_company = db.relationship("Director_Practice_Company", back_populates="director_company_practice")

    def __init__(self, director_practice_company_id: int, practice_id: int):
        self.director_practice_company_id = director_practice_company_id
        self.practice_id = practice_id

class Student_Practice(db.Model) :
    __tablename__ = "student_practice"
    student_id = db.Column(db.Integer, db.ForeignKey("student.user_id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.practice_id"))
    director_practice_organization_id = db.Column(db.Integer, db.ForeignKey("director_practice_organization.user_id"))
    kind_of_contract = db.Column(db.String(100), nullable = False)
    paid = db.Colomn(db.Bool, nullable = False)
    overcoming_difficulties = db.Column(db.Text, nullable = False)
    production_tasks = db.Column(db.Text, nullable = False)
    demonstrated_qualities = db.Column(db.Text, nullable = False)
    work_volume = db.Column(db.Text, nullable = False)
    remarks = db.Column(db.Text, nullable = False)
    
    # связи
    practice = db.relationship("Practice", back_populates="student_practice")
    director_practice_organization = db.relationship("Director_Practice_Organization", back_populates="student_practice")
    student = db.relationship("Student", back_populates="student_practice")

    def __init__(self, student_id: int, practice_id: int, director_practice_organization_id: int, kind_of_contract: str, paid: bool, overcoming_difficulties: str, production_tasks: str, demonstrated_qualities: str, work_volume: str, remarks: str):
        self.student_id = student_id
        self.practice_id = practice_id
        self.director_practice_organization_id = director_practice_organization_id
        self.kind_of_contract = kind_of_contract
        self.paid = paid
        self.overcoming_difficulties = overcoming_difficulties
        self.production_tasks = production_tasks
        self.demonstrated_qualities = demonstrated_qualities
        self.work_volume = work_volume
        self.remarks = remarks
    

with app.app_context():
    db.create_all()