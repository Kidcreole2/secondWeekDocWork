from flask import request, render_template, redirect, url_for
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from models import Users


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

@app.route("/opop_add")
@login_required
def opop_add():
    return render_template("pages/opop/add.html")

@app.route("/admin_index")
@login_required
def admin_index():
    return render_template("pages/admin/index.html")

@app.route("/admin_add", methods=["GET","POST"])
# @login_required
def admin_add():
    if request.method == "POST":
        user = Users(login=request.form['login'], 
                     password=request.form['password'], 
                     firstname=request.form['firstname'], 
                     lastname=request.form['lastname'], 
                     surname=request.form['surname'], 
                     role=request.form["role"]
                     )
        reg_check = Users.register(user)
        if reg_check:
            return redirect(url_for("register"))
        return redirect(url_for("home"))
    
    return render_template("pages/admin/add.html")


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
    roles = current_user.role.split(',')
    return render_template("index.html",roles=roles)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #TODO make password check
        login = request.form["login"]
        print(login)
        password = request.form.get("password")
        roles = Users.auth_user(login, password)
        roles = roles.split(',')
        return render_template("index.html",roles=roles)
    return render_template("login.html")