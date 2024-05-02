from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from models import *
from file_manager import allowed_file, save_file

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id) 

# ==admin folder functions==

# --admin functions--

@app.route("/admin_index")
@login_required
def admin_index():
    return render_template("pages/admin/index.html")

# --user functions--

@app.route("/admin_user_index")
@login_required
def admin_user_index():
    users = Users.query.order_by(Users.firstname).all()
    return render_template("pages/admin/users/index.html", users=users)

@app.route("/admin_user_create", methods=["GET","POST"])
# @login_required
def admin_user_create():
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
    return render_template("pages/admin/users/create.html", messages=messages)

@app.route("/admin_user_update/<login>", methods=["GET","POST"])
@login_required
def admin_user_update(login):
    old_user = Users.query.filter_by(login=login).first()
    if request.method == "POST":
        new_user = Users(login=request.form['login'], 
                    password=request.form['password'], 
                    firstname=request.form['firstname'], 
                    lastname=request.form['lastname'], 
                    surname=request.form['surname'], 
                    role=request.form["role"]
                    )
        Users.update(old_user,new_user)
    return render_template("pages/admin/users/update.html",old_user=old_user)

# --institute functions--

@app.route("/admin_institute_index")
@login_required
def admin_institute_index():
    institutes = Institute.query.order_by(Institute.name).all()
    return render_template("pages/admin/institute/index.html", institutes=institutes)


@app.route("/admin_institute_create", methods=["GET","POST"])
@login_required
def admin_institute_create():
    if request.method == "POST":
        new_institute = Institute(
            name=request.form['name'],
        )
        Institute.create(new_institute)
        return redirect(url_for("admin_institute_index"))
    return render_template("pages/admin/institute/create.html")

@app.route("/admin_institute_update/<institute_id>", methods=["GET","POST"])
@login_required
def admin_institute_update(institute_id):
    old_institute = Institute.query.filter_by(id=institute_id).first()
    if request.method == "POST":
        new_institute = Institute(
            name=request.form['name'],
        )
        Institute.update(old_institute,new_institute)
        return redirect(url_for("admin_index"))
    specializations = Specialization.query.order_by(Specialization.name).all()
    return render_template("pages/admin/institute/update.html",old_institute=old_institute, specializations=specializations)

# --specialization functions--

@app.route("/admin_specialization_create/<institute_id>", methods=["GET","POST"])
@login_required
def admin_specialization_create(institute_id):
    if request.method == "POST":
        new_specialization = Specialization(
            name=request.form['name'],
            specialization_code=request.form['specialization_code'],
            institute_id=institute_id,
            director_opop_id=request.form['director_opop_id']
        )
        Specialization.create(new_specialization)
        return redirect(url_for("admin_institute_index"))
    return render_template("pages/admin/institute/specialization/create.html")

@app.route("/admin_specialization_update/<institute_id>/<specialization_id>", methods=["GET","POST"])
@login_required
def admin_specialization_update(institute_id,specialization_id):
    if request.method == "POST":
        old_specialization = Specialization.query.filter_by(id=specialization_id).first()
        new_specialization = Specialization(
            name=request.form['name'],
            specialization_code=request.form['specialization_code'],
            institute_id=institute_id,
            director_opop_id=request.form['director_opop_id']
        )
        Specialization.update(old_specialization,new_specialization)
        return redirect(url_for("admin_institute_index"))
    return render_template("pages/admin/institute/specialization/update.html")


# ==opop functions folder==

# --opop functions--

@app.route("/opop_index")
@login_required
def opop_index():
    return render_template("pages/opop/index.html")

# --group functions--

@app.route("/opop_group_index")
@login_required
def opop_group_index():
    groups = Group.query.order_by(Group.name).all()
    return render_template("pages/opop/group/index.html", groups=groups)


@app.route("/opop_group_create", methods=["GET","POST"])
@login_required
def opop_group_create():
    if request.method == "POST":
        new_group = Group(
            name=request.form['name'],
            specialization_id=request.form['specialization_id'],
            course=request.form['course']
        )
        Group.create(new_group)
        return redirect(url_for("opop_group_index"))
    return render_template("pages/opop/group/create.html")

@app.route("/opop_group_update/<group_id>", methods=["GET","POST"])
@login_required
def opop_group_update(group_id):
    old_group = Group.query.filter_by(id=group_id).first()
    if request.method == "POST":
        new_group = Group(
            name=request.form['name'],
            specialization_id=request.form['specialization_id'],
            course=request.form['course']
        )
        Group.update(old_group,new_group)
        return redirect(url_for("opop_group_index"))
    students = Student.query.order_by(Student.name).all()
    return render_template("pages/opop/group/update.html", students=students)

# --student functions--

@app.route("/opop_student_create", methods=["GET","POST"])
@login_required
def opop_student_create():
    if request.method == "POST":
        new_student = Student(
            group_id=request.form['group_id'],
            user_id=request.form['user_id']
        )
        Student.create(new_student)
        return redirect(url_for("opop_group_update"))
    return render_template("pages/opop/group/student/create.html")

@app.route("/opop_student_update/student_id", methods=["GET","POST"])
@login_required
def opop_student_update(student_id):
    if request.method == "POST":
        old_student = Student.query.filter_by(id=student_id).first()
        new_student = Student(
            group_id=request.form['group_id'],
            user_id=request.form['user_id']
        )
        Student.update(old_student,new_student)
        return redirect(url_for("opop_group_update"))
    return render_template("pages/opop/group/student/update.html")

# --practice functions--

@app.route("/opop_practice_index")
@login_required
def opop_practice_index():
    practices = Practice.query.order_by(Practice.name).all()
    return render_template("pages/opop/practice/index.html", practices=practices)


@app.route("/opop_practice_create", methods=["GET","POST"])
@login_required
def opop_practice_create():
    if request.method == "POST":
        new_practice = Practice(
            name=request.form['name'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            type_of_practice=request.form['type_of_practice'],
            kind_of_practice=request.form['kind_of_practice'],
            order=request.form['order'],
            recomendations=request.form['recomendations']
        )
        Practice.create(new_practice)
        return redirect(url_for("opop_practice_index"))
    return render_template("pages/opop/practice/create.html")

@app.route("/opop_practice_update/<practice_id>", methods=["GET","POST"])
@login_required
def opop_practice_update(practice_id):
    if request.method == "POST":
        old_practice = Practice.query.filter_by(id=practice_id).first()
        new_practice = Practice(
            name=request.form['name'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            type_of_practice=request.form['type_of_practice'],
            kind_of_practice=request.form['kind_of_practice'],
            order=request.form['order'],
            recomendations=request.form['recomendations']
        )
        Student.update(old_practice,new_practice)
        return redirect(url_for("opop_practice_index"))
    return render_template("pages/opop/practice/update.html")

@app.route("/opop_practice_start")
@login_required
def opop_practice_start():
    return render_template("pages/opop/practice/start.html")

# ==student practice functions folder==

@app.route("/studentPractice_student")
@login_required
def studentPractice_student():
    return render_template("pages/studentPractice/student.html")

@app.route("/studentPractice_supervisor")
@login_required
def studentPractice_supervisor():
    students = Student.query.order_by(Student.name).all()
    return render_template("pages/studentPractice/supervisor.html", students=students)

@app.route("/studentPractice_update/<student_id>", methods=["GET","POST"])
@login_required
def studentPractice_update(student_id):
    # if request.method == "POST":
    #     old_studentPractice = Practice.query.filter_by(id=practice_id).first()
    #     new_practice = Practice(
    #         name=request.form['name'],
    #         start_date=request.form['start_date'],
    #         end_date=request.form['end_date'],
    #         type_of_practice=request.form['type_of_practice'],
    #         kind_of_practice=request.form['kind_of_practice'],
    #         order=request.form['order'],
    #         recomendations=request.form['recomendations']
    #     )
    #     Student.update(old_practice,new_practice)
    #     return redirect(url_for("opop_practice_index"))
    return render_template("pages/studentPractice/update.html")

# ==utilite functions folder==

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


# ==Basic functions==


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/home")
@login_required
def home():
    roles = current_user.role.split()
    return render_template("index.html",roles=roles)

# --login function--

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