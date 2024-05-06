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

