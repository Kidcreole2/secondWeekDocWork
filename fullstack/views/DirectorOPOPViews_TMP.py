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

