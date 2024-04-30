from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from models import Users
from file_manager import allowed_file, save_file

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id) 

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        print(type(request.files["file"]))
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            save_file(file)
            # flash("Заебись")
            return redirect(request.url)

    messages = get_flashed_messages()
    return render_template("test/file_upload.html",  messages=messages)

@app.route('/register', methods=["GET","POST"])
def register():
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
    
    return render_template("pages/Admin/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #TODO make password check
        login = request.form["login"]
        print(login)
        password = request.form.get("password")
        role = Users.auth_user(login, password)
    
        if role == "student":
            return render_template("pages/student/index.html")
        
        return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/opop")
@login_required
def opop_page():
    return render_template("pages/opop/index.html")

@app.route("/admin")
@login_required
def admin_page():
    return render_template("pages/admin/index.html")

@app.route("/teacher")
@login_required
def teacher_page():
    return render_template("pages/teacher/index.html")

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return render_template("login.html")