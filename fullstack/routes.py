from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from models import *
from file_manager import allowed_file, save_file

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id) 

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/opop_index")
@login_required
def opop_index():
    return render_template("pages/opop/index.html")

@app.route("/opop_add_practice", methods=["GET","POST"])
@login_required
def opop_add_practice():
    if request.method == "POST":
        practice = Practice(
            year=request.form['year'],
            period_practice=request.form['periodPractice'],
            name=request.form['namePractice'],
            order=request.form['order'],
            type_of_practice=request.form['typeOfPractice'],
            kind_of_practice=request.form['kindOfPractice']
        )
        practice_id = Practice.add(practice)
        specialization = request.form['specialization']
        specialization_id = Specialization.query.filter_by(specialization=Specialization.name).first()
        group = Group(
            specialization_id=specialization_id,
            name=request.form['nameGroup'],
            course=request.form['course']
        )
        group_id = Group.add(group)
        practice_group = Practice_Group(
            practice_id=practice_id,
            group_id=group_id
        )
        practice_group_id = Practice_Group.add(practice_group)
    
    messages = get_flashed_messages()
    return render_template("pages/opop/add.html", messages=messages)

@app.route("/opop_add_group", methods=["GET","POST"])
@login_required
def opop_add_practice():
    if request.method == "POST":
        specialization = request.form['specialization']
        specialization = Specialization.query.filter_by(specialization=Specialization.name).first()
        specialization_id = specialization.id
        group = Group(
            specialization_id=specialization_id,
            name=request.form['nameGroup'],
            course=request.form['course']
        )
    
    messages = get_flashed_messages()
    return render_template("pages/opop/add.html", messages=messages)

@app.route("/opop_add_student", methods=["GET","POST"])
@login_required
def opop_add_student():
    if request.method == "POST":
        user_student = Users(
            login=request.form['login'], 
            password=request.form['password'], 
            firstname=request.form['firstname'], 
            lastname=request.form['lastname'], 
            surname=request.form['surname'], 
            role=request.form["role"]
        )
        user_student_id=Users.add(user_student)
        group = request.form['group']
        group = Group.query.filter_by(group=Group.name).first()
        group_id = group.id
        student = Student(
            user_id=user_student_id,
            group_id=group_id,
            name_rp = request.form['nameRp']
        )
        student_id = Student.add(student)
    
    messages = get_flashed_messages()
    return render_template("pages/opop/add.html", messages=messages)

@app.route("/admin_index")
@login_required
def admin_index():
    users = db.session.execute(db.select(Users)
            .order_by(Users.firstname)).scalars()
    return render_template("pages/admin/index.html", users = users)

@app.route("/admin_add_user", methods=["GET","POST"])
def admin_add_data():
    if request.method == "POST":
        institute = Institute(
            name=request.form['nameInstitute']
        )
        institute_id = Institute.add(institute)
        user_opop = Users(
            login=request.form['login'], 
            password=request.form['password'], 
            firstname=request.form['firstname'], 
            lastname=request.form['lastname'], 
            surname=request.form['surname'], 
            role=request.form["role"]
        )
        user_opop_id = Users.add(user_opop)
        opop = Director_OPOP(
            user_id=user_opop_id,
            post=request.form['post']
        )
        opop_id = Director_OPOP.add(opop)
        specialization = Specialization(
            institute_id=institute_id,
            director_opop_id=opop_id,
            name=request.form['nameSpecialization']
        )
        specialization_id = Specialization.add(specialization)
    messages = get_flashed_messages()
    return render_template("pages/admin/add.html", messages=messages)

@app.route("/admin_add_user", methods=["GET","POST"])
# @login_required
def admin_add_user():
    if request.method == "POST":
        if request.form['password'] == request.form['passwordConfirm'] :
            user = Users(login=request.form['login'], 
                        password=request.form['password'], 
                        firstname=request.form['firstname'], 
                        lastname=request.form['lastname'], 
                        surname=request.form['surname'], 
                        role=request.form["role"]
                        )
            reg_check = Users.add(user)
            if reg_check["exists"]:
                return redirect(url_for("admin_add"))
            return redirect(url_for("home"))
        else:
            flash("Пароли не совпадают")
    messages = get_flashed_messages()
    return render_template("pages/admin/add.html", messages=messages)

@app.route("/upload_specs", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            save_file(file, "specs")
            flash("Файл успешно загружен")
            return redirect(request.url)
        else:
            flash("неверный тип файла")
    messages = get_flashed_messages()
    print(messages)
    return render_template("test/file_upload.html",  messages=messages)

@app.route("/supervisorCompany_index")
@login_required
def supervisorCompany_index():
    return render_template("pages/supervisorCompany/index.html")

@app.route("/supervisorCompany_add")
@login_required
def supervisorCompany_add():
    return render_template("pages/supervisorCompany/add.html")

@app.route("/supervisorPracticeOrg_index")
@login_required
def supervisorPracticeOrg_index():
    return render_template("pages/supervisorPracticeOrg/index.html")

@app.route("/supervisorPracticeOrg_add")
@login_required
def supervisorPracticeOrg_add():
    return render_template("pages/supervisorPracticeOrg/add.html")

@app.route("/supervisorUgrasu_index")
@login_required
def supervisorUgrasu_index():
    return render_template("pages/supervisorUgrasu/index.html")

@app.route("/supervisorUgrasu_add")
@login_required
def supervisorUgrasu_add():
    return render_template("pages/supervisorUgrasu/add.html")

@app.route("/home")
@login_required
def home():
    roles = current_user.role.split()
    return render_template("index.html",roles=roles)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #TODO make password check
        login = request.form["login"]
        print(login)
        password = request.form.get("password")
        roles = Users.auth_user(login, password)
        roles = roles.split()
        return render_template("index.html",roles=roles)
    return render_template("login.html")