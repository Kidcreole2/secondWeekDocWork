from flask import request, render_template, send_from_directory, redirect, url_for, flash, current_app, get_flashed_messages
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from datetime import datetime as date
from models import *
from file_manager import allowed_file, save_file
from document_generator import StudentDocument
import os

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
                    reg_check = Users.create(user)
                    match request.form['userType']:
                        case "directorOPOP":
                            director = Director_OPOP(
                                user_id=reg_check["id"],
                                post=request.form['post']
                            )
                            Director_OPOP.create(director)
                        case "directorCompany":
                            director = Director_Practice_Company(
                                user_id=reg_check["id"],
                                post=request.form['post']
                            )
                            Director_Practice_Company.create(director)
                        case "directonOrganization":
                            director = Director_Practice_Organization(
                                user_id=reg_check["id"],
                                post=request.form['post']
                            )
                            Director_Practice_Organization.create(director)
                        case "directorUSU":
                            director = Director_Practice_USU(
                                user_id=reg_check["id"],
                                post=request.form['post']
                            )
                            Director_Practice_USU.create(director)
                    if reg_check["exists"]:
                        return redirect(url_for("admin_user_index"))
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
        Users.update(login,new_user)
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
    print("test_2")
    if request.method == "POST":
        print("test_3")
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
        return redirect(url_for("admin_institute_index"))
    specializations = Specialization.query.order_by(Specialization.name).all()
    return render_template("pages/admin/institute/update.html",institute=old_institute, specializations=specializations)

# --specialization functions--

@app.route("/admin_specialization_create/<institute_id>", methods=["GET","POST"])
@login_required
def admin_specialization_create(institute_id):
    opop_director_users = []
    if request.method == "POST":
        new_specialization = Specialization(
            name=request.form['name'],
            specialization_code=request.form['specialization_code'],
            institute_id=institute_id,
            director_opop_id=request.form['director_opop_id']
        )
        Specialization.create(new_specialization)
        return redirect(url_for("admin_institute_index"))
    opop_directors = Director_OPOP.query.order_by(Director_OPOP.id).all()
    # for opop_director in opop_directors:
    #     opop_director_user = Users.query.filter_by(id=opop_director.user_id).first()
    #     opop_director_users = opop_director_users.append(opop_director_user)
    return render_template("pages/admin/institute/specialization/create.html",opop_directors=opop_directors)

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
    # TODO Сделать фильтр по ОПОП руководителю
    groups = Group.query.order_by(Group.name).all()
    return render_template("pages/opop/group/index.html", groups=groups)


@app.route("/opop_group_create", methods=["GET","POST"])
@login_required
def opop_group_create():
    opop_director = Director_OPOP.query.filter_by(user_id=current_user.id).first()
    spezializations = Specialization.query.filter_by(id=opop_director.id).all()
    if request.method == "POST":
        new_group = Group(
            name=request.form['name'],
            specialization_id=request.form['specialization_id'],
            course=request.form['course'],
            form=request.form['form']
        )
        Group.create(new_group)
        return redirect(url_for("opop_group_index"))
    return render_template("pages/opop/group/create.html", spezializations=spezializations)

@app.route("/opop_group_update/<group_id>", methods=["GET","POST"])
@login_required
def opop_group_update(group_id):
    old_group = Group.query.filter_by(id=group_id).first()
    if request.method == "POST":
        new_group = Group(
            name=request.form['name'],
            specialization_id=request.form['specialization_id'],
            course=request.form['course'],
            form=request.form['form']
        )
        Group.update(old_group,new_group)
        return redirect(url_for("opop_group_index"))
    student_users = Student.query.order_by(Student.id).all()
    return render_template("pages/opop/group/update.html", student_users=student_users,group=old_group)

# --student functions--

@app.route("/opop_student_create/<group_id>", methods=["GET","POST"])
@login_required
def opop_student_create(group_id):
    if request.method == "POST":
        new_student_user = Users(
            login=Users.login_generation(), 
            password=Users.password_generation(), 
            firstname=request.form['firstname'], 
            lastname=request.form['lastname'], 
            surname=request.form['surname'], 
            role="student"
        )   
        user_id = Users.create(new_student_user)
        new_student = Student(
            group_id=group_id,
            user_id=user_id["id"]
        )
        Student.create(new_student)
        return redirect(url_for("opop_group_index"))
    return render_template("pages/opop/group/student/create.html")

@app.route("/opop_student_update/<group_name>/<student_id>", methods=["GET","POST"])
@login_required
def opop_student_update(group_name,student_user_id):
    if request.method == "POST":
        new_group = Group.query.filter_by(name=group_name).first()
        old_student_user = Users.query.filter_by(id=student_user_id).first()
        old_student = Student.query.filter_by(user_id=student_user_id).first()
        new_student_user = Users(
            login=request.form['login'], 
            password=request.form['password'], 
            firstname=request.form['firstname'], 
            lastname=request.form['lastname'], 
            surname=request.form['surname'], 
            role=request.form["role"]
        )
        Users.update(old_student_user,new_student_user)
        new_student = Student(
            group_id=new_group.id,
            user_id=student_user_id
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
            start_date=date.strptime(request.form['start_date'], "%Y-%m-%d"),
            end_date=date.strptime(request.form['end_date'], "%Y-%m-%d"),
            type_of_practice=request.form['type_of_practice'],
            kind_of_practice=request.form['kind_of_practice'],
            order=request.form['order'],
            recomendations=request.form['recomendations']
        )
        print(request.form)
        practice_id = Practice.create(new_practice)
        data = request.form.to_dict()
        data_keys = data.keys()
        for checkbox in data_keys:
            if "check_" in checkbox and request.form[checkbox]:
                group_id = int(checkbox.split("_")[1])
                practice_group = Practice_Group(
                    practice_id=practice_id,
                    group_id=group_id
                )
                Practice_Group.create(practice_group)
        return redirect(url_for("opop_practice_index"))
    groups = Group.query.order_by(Group.name).all()
    return render_template("pages/opop/practice/create.html",groups=groups)

@app.route("/opop_practice_update/<practice_id>", methods=["GET","POST"])
@login_required
def opop_practice_update(practice_id):
    if request.method == "POST":
        old_practice = Practice.query.filter_by(id=practice_id).first()
        new_practice = Practice(
            name=request.form['name'],
            start_date=date.strptime(request.form['start_date'], "%Y-%m-%d"),
            end_date=date.strptime(request.form['end_date'], "%Y-%m-%d"),
            type_of_practice=request.form['type_of_practice'],
            kind_of_practice=request.form['kind_of_practice'],
            order=request.form['order'],
            recomendations=request.form['recomendations']
        )
        Practice.update(old_practice,new_practice)
        data = request.form.to_dict()
        data_keys = data.keys()
        for checkbox in data_keys:
            if "check_" in checkbox and request.form[checkbox]:
                practice_id = Practice.create(new_practice)
                group_id = int(checkbox.split("_")[1])
                new_practice_group = Practice_Group(
                    practice_id=practice_id,
                    group_id=group_id
                )
                Practice_Group.create(new_practice_group)
        return redirect(url_for(request.url))
    return render_template("pages/opop/practice/update.html", practice_id=practice_id)



@app.route("/opop_practice_start/<practice_id>", methods=["GET","POST"])
@login_required
def opop_practice_start(practice_id):
    if request.method == "POST":
        groups = Practice_Group.query.filter_by(practice_id=practice_id).all()
        for group in groups:
            students = Student.query.filter_by(group_id=group.id).all()
            for student in students:
                practice = Student_Practice(student_id=student.user_id, 
                                            practice_id=practice_id, 
                                            director_practice_organization_id=request.form["director_of_practice_organization"], 
                                            kind_of_contract=request.form["kind_of_contract"], 
                                            paid=bool(request.form["paid"]))
                Student_Practice.create(practice)
        return redirect(url_for("opop_practice_index"))
    directors = Director_Practice_Company.query.all()
    
    
    return render_template("pages/opop/practice/start.html", directors=directors)


# ==student practice functions folder==

@app.route("/studentPractice_student")
@login_required
def studentPractice_student():
    student = Student.query.filter_by(user_id=current_user.id).first()
    print(student)
    student_practice = Student_Practice.query.filter_by(student_id=student.user_id  ).all()
    print(student)
    return render_template("pages/studentPactice/student.html", student_practices=student_practice)

@app.route("/studentPractice_supervisor")
@login_required
def studentPractice_supervisor():
    roles = current_user.roles.split()
    if "director" in roles:
        director_practice_organization = Director_Practice_Organization.query.filter_by(user_id=current_user.id).first()
        student_practice_dpo = Student_Practice.query.filter_by(director_practice_organization_id=director_practice_organization.id).all()
    if "director" in roles:
        director_practice_usu = Director_Practice_USU.query.filter_by(user_id=current_user.id).first()
        student_practice_dpu = Practice.query.filter_by(director_practice_usu_id=director_practice_usu.id).all()
    if "director" in roles:
        director_practice_company = Director_Practice_Company.query.filter_by(user_id=current_user.id).first()
        student_practice_dpc = Practice.query.filter_by(director_practice_company_id=director_practice_company.id).all()
    student_practice = set(student_practice_dpo,student_practice_dpu,student_practice_dpc)
    return render_template("pages/studentPractice/supervisor.html", student_practice=student_practice)

@app.route("/student_practice_dpu_task_update/<student_practice_id>", methods=["GET","POST"])
@login_required
def studentPractice_update(student_practice_id):
    if request.method == "POST":
        old_student_practice = Student_Practice.query.filter_by(id=student_practice_id).first()
        new_student_practice = Student_Practice(
            place_city=request.form['place_city'],
            place_address=request.form['place_address'],
            place_name=request.form['place_name'],
            place_name_short=request.form['place_name_short'],
        )
        Student.update(old_student_practice,new_student_practice)
        return redirect(url_for(f"opop_practice_index/{student_practice_id}"))
    return render_template("pages/studentPactice/update_diary.html")

@app.route("/student_practice_dpc_task_update/<student_practice_id>", methods=["GET","POST"])
@login_required
def student_practice_dpc_task_update(student_practice_id):
    if request.method == "POST":
        old_student_practice = Student_Practice.query.filter_by(id=student_practice_id).first()
        new_student_practice = Student_Practice(
            passed=request.form['passed'],
            overcoming_difficulties=request.form['overcoming_difficulties'],
            demonstrated_qualities=request.form['demonstrated_qualities'],
            work_volume=request.form['work_volume'],
            reason=request.form['reason'],
            remarks=request.form['remarks']
        )
        Student.update(old_student_practice,new_student_practice)
        return redirect(url_for(f"opop_practice_index/{student_practice_id}"))
    return render_template("pages/studentPactice/update_characteristics.html")

@app.route("/student_practice_dpo_task_index/<student_practice_id>", methods=["GET","POST"])
@login_required
def student_practice_dpo_task_index(student_practice_id):
    tasks= Task.query.filter_by(student_practice_id=student_practice_id).all()
    return render_template("pages/studentPactice/tasks/index.html", tasks=tasks, student_practice_id = student_practice_id)

@app.route("/student_practice_dpo_task_create/<student_practice_id>", methods=["GET","POST"])
@login_required
def student_practice_dpo_task_create(student_practice_id):
    if request.method == "POST":
        new_Task = Task(
        name=request.form['name'],
        date=date.strptime(request.form['date'], "%Y-%m-%d"),
        student_practice_id=student_practice_id
        )
        Task.create(new_Task)
        return render_template("pages/studentPactice/tasks/index.html",student_practice_id=student_practice_id)
    return render_template("pages/studentPactice/tasks/create.html")

@app.route("/student_practice_dpo_task_update/<student_practice_id>/<task_id>", methods=["GET","POST"])
@login_required
def student_practice_dpo_task_update(student_practice_id,task_id):
    if request.method == "POST":
        old_task = Task.query.filter_by(id=task_id).first()
        new_Task = Task(
        name=request.form['name'],
        date=date.strptime(request.form['date'], "%Y-%m-%d"),
        student_practice_id=student_practice_id
        )
        Task.update(old_task, new_Task)
        return redirect(url_for(f"opop_practice_index/{student_practice_id}"))
    return render_template("pages/studentPactice/tasks/update.html")

# ==utilite functions folder==

# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = os.path.join(current_app.root_path, 'outputs')
#     return send_from_directory(uploads, filename)

# @app.route('/uploads/', methods=['GET', 'POST'])
# def download():
#     uploads = os.path.join(current_app.root_path, 'outputs')
#     student_doc = StudentDocument()
#     student_docs = student_doc.getDocuments()
#     return send_from_directory(uploads, student_docs)

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
