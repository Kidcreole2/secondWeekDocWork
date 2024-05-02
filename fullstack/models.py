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
    student = db.relationship("Student", uselist=False, back_populates="user")
    director_opop = db.relationship("Director_OPOP", uselist=False, back_populates="user")
    director_practice_usu = db.relationship("Director_Practice_USU", uselist=False, back_populates="user")
    director_practice_company = db.relationship("Director_Practice_Company", uselist=False, back_populates="user")
    director_practice_organization = db.relationship("Director_Practice_Organization", uselist=False, back_populates="user")
    
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
            return { "id":user.id, "exists": False} 
        else:
            return {"id": new_user.id, "exists": True}
        
class Practice(db.Model) :
    __tablename__ = "practice"
    id = db.Column(db.Integer, primary_key = True)
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

class Institute(db.Model) :
    __tablename__ = "institute"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique=True, nullable = False)

    # связи
    specialization = db.relationship("Specialization", back_populates="institute")

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def add_institute(institute):
        new_institute = Institute.query.filter_by(name=institute.name).first()
        if new_institute is None:
            db.session.add(institute)
            db.session.commit()
            return Institute.query.filter_by(name=institute.name).first().id
        else:
            return new_institute.id

class Place(db.Model) :
    __tablename__ = "place"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(100), nullable=False)
    # связи
    practice_place = db.relationship("Practice_Place", back_populates="place")
    
    def __init__(self, name: str):
        self.name = name

class Director_OPOP(db.Model) :
    __tablename__ = "director_opop"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_opop")
    specialization = db.relationship("Specialization", back_populates="director_opop")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

    @staticmethod
    def add_director_opop(directior):
        new_director = Director_OPOP.query.filter_by(user_id=directior.user_id).first()
        if new_director == None:
            db.session.add(directior)
            db.session.commit()
            return {"id": directior.id, "exists": False}
        else:
            return {"id": new_director.id, "exists": True}

class Director_Practice_USU(db.Model) :
    __tablename__ = "director_practice_usu"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_usu")
    director_usu_practice = db.relationship("Director_USU_Practice", back_populates="director_practice_usu")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

class Director_Practice_Company(db.Model) :
    __tablename__ = "director_practice_company"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_company")
    director_company_practice = db.relationship("Director_Company_Practice", back_populates="director_practice_company")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

class Director_Practice_Organization(db.Model) :
    __tablename__ = "director_practice_organization"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_organization")
    student_practice = db.relationship("Student_Practice", back_populates="director_practice_organization")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

class Specialization(db.Model) :
    __tablename__ = "specialization"
    id = db.Column(db.Integer, primary_key = True)
    institute_id = db.Column(db.Integer, db.ForeignKey("institute.id"))
    director_opop_id = db.Column(db.Integer, db.ForeignKey("director_opop.user_id"))
    name = db.Column(db.String(100), unique=True, nullable = False)
    specialization_code = db.Column(db.String(20), unique=True, nullable = False)

    # связи
    institute = db.relationship("Institute", back_populates="specialization")
    director_opop = db.relationship("Director_OPOP", back_populates="specialization")
    group = db.relationship("Group", back_populates="specialization")

    def __init__(self, institute_id: int, director_opop_id: int, name: str, specialization_code: str):
        self.institute_id = institute_id
        self.director_opop_id = director_opop_id
        self.name = name
        self.specialization_code = specialization_code

    @staticmethod
    def add_specialisation(spec):
        new_spec = Specialization.query.filter_by(name=spec.name).first()
        if new_spec == None:
            db.session.add(spec)
            db.session.commit()
            return spec.id
        else:
            return new_spec.id

class Group(db.Model) :
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.Integer, primary_key = True)
    specialization_id = db.Column(db.Integer, db.ForeignKey("specialization.id"))
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

    @staticmethod
    def add_group(group):
        new_group = Group.query.filter_by(name=group.name).first()
        if new_group is None:
            db.session.add(group)
            db.session.commit()
            return Group.query.filter_by(name=group.name).first().id
        else:
            return new_group.id

class Student(db.Model) :
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    # связи
    user = db.relationship("Users", back_populates="student")
    group = db.relationship("Group", back_populates="student")
    student_practice = db.relationship("Student_Practice", back_populates="student")

    def __init__(self, user_id: int, group_id: int):
        self.user_id = user_id
        self.group_id = group_id

    @staticmethod
    def add_student(student):
        new_student = Student.query.filter(user_id=student.user_id).first()
        if new_student == None:
            db.session.add(student)
            db.session.commit()
            return Student.query.filter_by(user_id=student.user_id).first().id
        else:
            return new_student.id

class Practice_Group(db.Model) :
    __tablename__ = "practice_group"
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.id"))

    # связи
    practice = db.relationship("Practice", back_populates="practice_group")
    group = db.relationship("Group", back_populates="practice_group")

    def __init__(self, group_id: int, practice_id: int):
        self.group_id = group_id
        self.practice_id = practice_id

class Practice_Place(db.Model) :
    __tablename__ = "practice_place"
    id = db.Column(db.Integer, primary_key = True)
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))
    
    # связи
    place = db.relationship("Place", back_populates="practice_place")
    practice = db.relationship("Practice", back_populates="practice_place")

    def __init__(self, practice_id: int, place_id: int):
        self.practice_id = practice_id
        self.place_id = place_id

class Director_USU_Practice(db.Model) :
    __tablename__ = "director_usu_practice"
    id = db.Column(db.Integer, primary_key = True)
    director_practice_usu_id = db.Column(db.Integer, db.ForeignKey("director_practice_usu.user_id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.id"))

    # связи
    practice = db.relationship("Practice", back_populates="director_usu_practice")
    director_practice_usu = db.relationship("Director_Practice_USU", back_populates="director_usu_practice")

    def __init__(self, director_practice_usu_id: int, practice_id: int):
        self.director_practice_usu_id = director_practice_usu_id
        self.practice_id = practice_id

class Director_Company_Practice(db.Model) :
    __tablename__ = "director_company_practice"
    id = db.Column(db.Integer, primary_key = True)
    director_practice_company_id = db.Column(db.Integer, db.ForeignKey("director_practice_company.user_id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.id"))

    # связи
    practice = db.relationship("Practice", back_populates="director_company_practice")
    director_practice_company = db.relationship("Director_Practice_Company", back_populates="director_company_practice")

    def __init__(self, director_practice_company_id: int, practice_id: int):
        self.director_practice_company_id = director_practice_company_id
        self.practice_id = practice_id

class Student_Practice(db.Model) :
    __tablename__ = "student_practice"
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.user_id"))
    practice_id = db.Column(db.Integer, db.ForeignKey("practice.id"))
    director_practice_organization_id = db.Column(db.Integer, db.ForeignKey("director_practice_organization.user_id"))
    passed = db.Column(db.Boolean, nullable=False)
    kind_of_contract = db.Column(db.String(100), nullable = False)
    paid = db.Column(db.Boolean, nullable = False)
    overcoming_difficulties = db.Column(db.Text, nullable = False)
    demonstrated_qualities = db.Column(db.Text, nullable = False)
    work_volume = db.Column(db.Text, nullable = False)
    remarks = db.Column(db.Text, nullable = False)
    
    # связи
    practice = db.relationship("Practice", back_populates="student_practice")
    director_practice_organization = db.relationship("Director_Practice_Organization", back_populates="student_practice")
    student = db.relationship("Student", back_populates="student_practice")
    task = db.relationship("Task", back_populates="student_practice")

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

class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    student_practice_id = db.Column(db.Integer, db.ForeignKey("student_practice.id"))

    student_practice = db.relationship("Student_Practice", back_populates="task")
    def __init__(self, name, date, student_practice_id):
        self.name = name
        self.date = date
        self.student_practice_id = student_practice_id


with app.app_context():
    db.create_all()

def load_specialisation_data(opops:dict, institutes:dict, specialisations:dict):
    """ Эта функция заполняяет таблицу специализаций базы данных 

    на вход передаются 3 массива словарей словар opops, institutes, specialisations
    содержащие поля

    opops = {
        "name" - массив из фамилии, имени и отчества,
    
        "login" - логин для директора ОПОП,
    
        "password" - пароль для директора ОПОП,
    
        "role" - роль для директора ОПОП ,
    
        "post" - должность директора ОПОП
    } 
    
    institutes = {
        "name" - имя института
    }
    
    specialisations = {
        "opop" - строка состоящая из фамилии имени и отчества,
    
        "name" - название специальности,
    
        "code" - код специальности,
    
        "institute" - имя института
    }
    """
    for institute in institutes:
        inst = Institute(institute["name"])
        Institute.add_institute(inst)

    for opop in opops:
        user = Users(login=opop["login"],password=opop["password"], firstname=opop["name"][1], lastname=opop["name"][0], surname=opop["name"][2],role=opop["role"])
        user_id = Users.register(user)["id"]
        
        opop_id = Director_OPOP.add_director_opop(Director_OPOP(user_id=user_id, post=opop["post"][0]))["id"]
        filtered_specs = list(filter(lambda x: x["opop"] == " ".join(opop["name"]), specialisations))
        print(filtered_specs)
        for filtered_spec in filtered_specs:
            institute = Institute.query.filter_by(name=filtered_spec["institute"]).first()
            spec = Specialization(institute_id=institute.id, director_opop_id=opop_id, name=filtered_spec["name"], specialization_code=filtered_spec["code"])
            Specialization.add_specialisation(spec)

    