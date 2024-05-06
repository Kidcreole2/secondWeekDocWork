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
    return render_template("pages/studentPactice/update.html")

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
    return render_template("pages/studentPactice/update.html")

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
        date=request.form['date'],
        student_practice_id=student_practice_id
        )
        Student.create(new_Task)
        return redirect(url_for(f"opop_practice_index/{student_practice_id}"))
    return render_template("pages/studentPactice/update.html")

@app.route("/student_practice_dpo_task_update/<student_practice_id>/<task_id>", methods=["GET","POST"])
@login_required
def student_practice_dpo_task_update(student_practice_id,task_id):
    if request.method == "POST":
        old_task = Task.query.filter_by(id=task_id).first()
        new_Task = Task(
        name=request.form['name'],
        date=request.form['date'],
        student_practice_id=student_practice_id
        )
        Student.update(old_task, new_Task)
        return redirect(url_for(f"opop_practice_index/{student_practice_id}"))
    return render_template("pages/studentPactice/update.html")
