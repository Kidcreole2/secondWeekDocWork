from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from core import app
import datetime

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
    def create(user):
        new_user = Users.query.filter_by(login=user.login).first()
        if new_user is None:
            db.session.add(user)
            db.session.commit()
            return { "id":user.id, "exists": False}
        else:
            return {"id": new_user.id, "exists": True}
        
    @staticmethod 
    def update(old_user_login, new_user): 
        old_user = Users.query.filter_by(login=old_user_login).first()
        old_user.login = new_user.login
        old_user.password = new_user.password
        old_user.firstname = new_user.firstname
        old_user.lastname = new_user.lastname
        old_user.surname = new_user.surname
        db.session.commit()
                
class Practice(db.Model) :
    __tablename__ = "practice"
    id = db.Column(db.Integer, primary_key = True)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    director_practice_usu_id = db.Column(db.Integer, db.ForeignKey("director_practice_usu.user_id"))
    director_practice_company_id = db.Column(db.Integer, db.ForeignKey("director_practice_company.user_id"))
    recomendations = db.Column(db.Text, nullable = False, default = "нет")
    name = db.Column(db.String(50), nullable = False)
    order = db.Column(db.String(100), nullable = False)
    type_of_practice = db.Column(db.String(100), nullable = False)
    kind_of_practice = db.Column(db.String(100), nullable = False)

    # связи
    director_practice_usu = db.relationship("Director_Practice_USU", back_populates="practice")
    director_practice_company = db.relationship("Director_Practice_Company", back_populates="practice")
    practice_group = db.relationship("Practice_Group", back_populates="practice")
    student_practice = db.relationship("Student_Practice", back_populates="practice")

    def __init__(self, start_date: datetime.date, end_date: datetime.date, recomendations: str, name: str, order: str, type_of_practice: str, kind_of_practice: str):
        self.start_date = start_date
        self.end_date = end_date
        self.recomendations = recomendations
        self.name = name
        self.order = order
        self.type_of_practice = type_of_practice
        self.kind_of_practice = kind_of_practice

    @staticmethod
    def create(practice):
        new_practice = Practice.query.filter_by(name = practice.id).first()
        if new_practice is None:
            db.session.add(practice)
            db.session.commit()
            return Practice.query.filter_by(name=practice.name).first().id
        else: 
            return new_practice.id

    @staticmethod
    def update(old_practice, new_pratice):
        old_practice = Practice.query.filter_by(id=old_practice.id).first()
        old_practice.start_date = new_pratice.start_date
        old_practice.end_date = new_pratice.end_date
        old_practice.director_practice_usu_id = new_pratice.director_practice_usu_id
        old_practice.director_practice_company_id = new_pratice.director_practice_company_id
        old_practice.recomendations = new_pratice.recomendations
        old_practice.name = new_pratice.name
        old_practice.order = new_pratice.order
        old_practice.type_of_practice = new_pratice.type_of_practice
        old_practice.kind_of_practice = new_pratice.kind_of_practice
        db.session.commit()

class Institute(db.Model) :
    __tablename__ = "institute"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique=True, nullable = False)

    # связи
    specialization = db.relationship("Specialization", back_populates="institute")

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def create(institute):
        new_institute = Institute.query.filter_by(name=institute.name).first()
        if new_institute is None:
            db.session.add(institute)
            db.session.commit()
            return Institute.query.filter_by(name=institute.name).first().id
        else:
            return new_institute.id

    @staticmethod
    def update(old_institute, new_institute):
        old_institute = Institute.query.filter_by(id=old_institute.id).first()
        old_institute.name = new_institute.name
        db.session.commit()

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
    def create(director):
        new_director = Director_OPOP.query.filter_by(user_id=director.user_id).first()
        if new_director == None:
            db.session.add(director)
            db.session.commit()
            return {"id": director.id, "exists": False}
        else:
            return {"id": new_director.id, "exists": True}

    @staticmethod
    def update(old_director, new_director):
        old_director = Director_OPOP.query.filter_by(id=old_director.id).first()
        old_director.post = new_director.post
        db.session.commit()

class Director_Practice_USU(db.Model) :
    __tablename__ = "director_practice_usu"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_usu")
    practice = db.relationship("Practice", back_populates="director_practice_usu")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

    @staticmethod
    def create(director):
        new_director = Director_Practice_USU.query.filter_by(user_id=director.user_id).first()
        if new_director == None:
            db.session.add(director)
            db.session.commit()
            return {"id": director.id, "exists": False}
        else:
            return {"id": new_director.id, "exists": True}

    @staticmethod
    def update(old_director, new_director):
        old_director = Director_Practice_USU.query.filter_by(id=old_director.id).first()
        old_director.post = new_director.post
        db.session.commit()

class Director_Practice_Company(db.Model) :
    __tablename__ = "director_practice_company"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    post = db.Column(db.String(100), nullable = False)

    # связи
    user = db.relationship("Users", back_populates="director_practice_company")
    practice = db.relationship("Practice", back_populates="director_practice_company")

    def __init__(self, user_id: int, post: str):
        self.user_id = user_id
        self.post = post

    @staticmethod
    def create(director):
        new_director = Director_Practice_Company.query.filter_by(user_id=director.user_id).first()
        if new_director == None:
            db.session.add(director)
            db.session.commit()
            return {"id": director.id, "exists": False}
        else:
            return {"id": new_director.id, "exists": True}

    @staticmethod
    def update(old_director, new_director):
        old_director = Director_Practice_Company.query.filter_by(id=old_director.id).first()
        old_director.post = new_director.post
        db.session.commit()

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

    @staticmethod
    def create(director):
        new_director = Director_Practice_Organization.query.filter_by(user_id=director.user_id).first()
        if new_director == None:
            db.session.add(director)
            db.session.commit()
            return {"id": director.id, "exists": False}
        else:
            return {"id": new_director.id, "exists": True}

    @staticmethod
    def update(old_director, new_director):
        old_director = Director_Practice_Organization.query.filter_by(id=old_director.id).first()
        old_director.post = new_director.post
        db.session.commit()

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
    def create(spec):
        new_spec = Specialization.query.filter_by(name=spec.name).first()
        if new_spec == None:
            db.session.add(spec)
            db.session.commit()
            return spec.id
        else:
            return new_spec.id

    @staticmethod
    def update(old_specialization, new_specialization):
        old_specialization = Specialization.query.filter_by(id=old_specialization.id).first()
        old_specialization.institute_id = new_specialization.institute_id
        old_specialization.director_opop_id = new_specialization.director.opop.id
        old_specialization.name - new_specialization.name
        old_specialization.specialization_code = new_specialization.specialization_code
        db.session.commit()

class Group(db.Model) :
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key = True)
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
    def create(group):
        new_group = Group.query.filter_by(name=group.name).first()
        if new_group is None:
            db.session.add(group)
            db.session.commit()
            return Group.query.filter_by(name=group.name).first().id
        else:
            return new_group.id

    @staticmethod
    def update(old_group, new_group):
        old_group = Group.query.filter_by(id=old_group.id).first()
        old_group.specialization_id = new_group.specialization_id
        old_group.name = new_group.name
        old_group.course = new_group.course
        db.session.commit()

class Student(db.Model) :
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    name_pr = db.Column(db.String(100), nullable=False)
    # связи
    user = db.relationship("Users", back_populates="student")
    group = db.relationship("Group", back_populates="student")
    student_practice = db.relationship("Student_Practice", back_populates="student")

    def __init__(self, user_id: int, group_id: int):
        self.user_id = user_id
        self.group_id = group_id

    @staticmethod
    def create(student):
        new_student = Student.query.filter(user_id=student.user_id).first()
        if new_student == None:
            db.session.add(student)
            db.session.commit()
            return Student.query.filter_by(user_id=student.user_id).first().id
        else:
            return new_student.id

    @staticmethod
    def update(old_student, new_student):
        old_student = Student.query.filter_by(id=old_student.id).first()
        old_student.group_id = new_student.group_id
        old_student.name_pr = new_student.name_pr
        db.session.commit()

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
    reason = db.Column(db.Text, nullable = True)
    remarks = db.Column(db.Text, nullable = False)
    place_city = db.Column(db.String(50), nullable = False)
    place_address = db.Column(db.String(100), nullable = False)
    place_name = db.Column(db.String(100), nullable = False)
    place_name_short = db.Column(db.String(100), nullable = False)
    
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

    @staticmethod
    def create(task):
        new_task = Task.query.filter_by(name=task.name).first()
        if new_task is None:
            db.session.add(task)
            db.session.commit()
            return Task.query.filter_by(name=task.name).first().id
        else: 
            return new_task.id
        
    @staticmethod
    def update(old_task, new_task):
        old_task = Task.query.filter_by(id=old_task.id).first()
        old_task.name = new_task.name
        old_task.date = new_task.date
        old_task.student_practice_id = new_task.student_practice_id
        db.session.commit()

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

    